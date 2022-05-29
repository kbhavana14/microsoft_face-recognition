''' This file gets executed when Take attendance button is pressed
    Opens camera and detects the face and checks if it is a fake or real image by using eyeblinking
    if the detected face is real, it checks with the student images and if image is found attendance is marked in csv file
    if image is not found in student images it shows the detected image as Unknown
'''

import imp
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime, date
import dlib
from math import hypot

# this function is called when user clicks on Take Attendance button
def takeAttendance():
    # Path setting to the directory containing the image database.
    # Read each image and the images array. 
    # Append the filenames into a list called classNames and remove the extension.
    path = 'studentImages'
    images = []
    classNames = []
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)

    # Finding face encodings of images in the database and 
    # keeping them in a list to use later with incoming frames. 
    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    # Attendance of a student is marked along with roll number, Time and date in csv file
    # multiple attendace of same student in the same day are not recorded
    def markAttendance(name):
        with open('Attendance.csv','r+') as f:
            myDataList = f.readlines()
            nameList = []
            dateList = []
            nddict = {}
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
                if entry[2] not in dateList:
                    dateList.append(entry[2])
            for nam in nameList:
                nddict[nam] = []
            for line in myDataList:
                entry = line.split(',')
                print(nddict)
                if entry[2] not in nddict[entry[0]]:
                    nddict[entry[0]].append(entry[2].rstrip('\n'))
            print(nddict)
            if name not in nameList:
                now = datetime.now()
                nowDate = date.today()
                dString = nowDate.strftime("%d/%m/%Y")
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString},{dString}')
            elif date.today().strftime("%d/%m/%Y") not in nddict[name]:
                now = datetime.now()
                nowDate = date.today()
                dString = nowDate.strftime("%d/%m/%Y")
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString},{dString}')


    encodeListKnown = findEncodings(images)
    print('Encoding Complete.')
    # Capturing video frames
    cap = cv2.VideoCapture(0)

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    def midpoint(p1 ,p2):
        return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)
    

    font = cv2.FONT_HERSHEY_PLAIN

    # returns the blinking ratio of the face detected in camera
    def get_blinking_ratio(eye_points, facial_landmarks):
        left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
        right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
        center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
        center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
    
        hor_line = cv2.line(img, left_point, right_point, (0, 255, 0), 2)
        ver_line = cv2.line(img, center_top, center_bottom, (0, 255, 0), 2)
    
        hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
        ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
    
        ratio = hor_line_lenght / ver_line_lenght
        return ratio

    success = True
    # Iterating through frames
    while success:
        success, img = cap.read()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blinking_ratio = 0
        faces = detector(gray)
        for face in faces:
            #x, y = face.left(), face.top()
            #x1, y1 = face.right(), face.bottom()
            #cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
    
            landmarks = predictor(gray, face)
    
            left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
            right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
            blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

        # The same process is followed by the first detection face location then getting the face encoding values.
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
    
        # Now the incoming images are tested against the previously-stored encodings.
        # Then the face distance is also computed. 
        # Lastly, we call the Attendance function along with the person name who is identified.
        for encodeFace, faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            matchIndex = np.argmin(faceDis)
            # if a encodings are matches with an student image 
            # then it checks if the detected image is real or fake using blinking ratio
            # else it detects the detected imagge as unknown
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                
                if blinking_ratio > 4.5:
                     cv2.putText(img, "Attendance marked", (50, 150),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                     y1,x2,y2,x1 = faceLoc
                     y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                     cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                     cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                     cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                     markAttendance(name)
                     success = False
                else:
                     y1,x2,y2,x1 = faceLoc
                     y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                     cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
                     cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,0,255),cv2.FILLED)
                     cv2.putText(img,'Fake',(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            else:
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,0,255),cv2.FILLED)
                cv2.putText(img,'Unknown',(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                
        cv2.imshow('Webcam',img)
        if(cv2.waitKey(1) & 0xFF==ord('q')):
            break


    
    
    