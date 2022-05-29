
# SMART ATTENDANCE SYSTEM USING FACE RECOGNITION
## INTRODUCTION
This is a simple desktop application which captures the attendance of the students using face recognition and liveness detection to avoid fake images. Face recognition library being a high level deep learning library helps in identifying faces accurately.
Here liveness detector is capable of spotting fake faces and performing anti-face spoofing in face recognition systems. One of the ways to detect liveness is eyeblink detection.
This can be use to build a face attendance system which can be helpful in offices, schools or any other place reducing manual labour and automatically updating the attendance records in day-to-day life. This also notes down the time of arrival thus can acquire information about people coming in late after a specified time.
## WORKING
In this face attendance system, webcam captured frames will be matched against the existing database images and if the match is found then it’ll store it in a CSV file called ‘Attendance’ along with name, date and time of capture. Only once the file will store the matched image’s details, if the same image is received again then it’ll not update.
## LIBRARIES USED
1) PyQt5
2) cv2
3) os
4) numpy
5) face_recognition
6) dlib
## SETUP
1)	Install Anaconda
2)	Open anaconda prompt
3)	Go to the project path
4)	Execute this command,  <b>conda install -c conda-forge dlib</b>
5)	Install requirements file by using command,  <b> pip install -r requirements.txt</b>
6)	Now execute the main file.i.e., mainWin.py by using command,   <b>python mainWin.py</b>
## RUNNING THE APPLICATION
1)	After executing the main file, main window of the application opens showing two options namely Add Student and Take Attendance
2)	Add Student captures the student’s image along with the entered roll number
-	Click on add student
-	Enter roll number
-	Click on Capture Image
-	Now, webcam gets opened press ‘S’ to capture image else press ‘Q’ to quit
3)	Take Attendance opens webcam to detect the face and recognize the detected face with the existing student images and marks attendance in a csv file along with roll, time and date.
-	Click on Take Attendance
-	Webcam opens
-	Checks for liveliness of the face using eyeblink detection
-	If eye blink is not detected, it shows the detected face as fake
-	If an eyeblink is detected, it marks the attendance
-	If the detected face has no matchings in the existing student images, then it shows the detected face as unknown
-	Press ‘Q’ to quit the webcam
4)	Open Attendance.csv file to see the students Attendance list.
