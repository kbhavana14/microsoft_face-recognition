'''Captures Image of the student when clicked on capture image button
   To capture image press 'S' key.
'''

import cv2
import os
from time import sleep

def capImg(fname):
    key = cv2. waitKey(1)
    webcam = cv2.VideoCapture(0)
    sleep(2)
    path = 'studentImages'
    while True:
    
        try:
            check, frame = webcam.read()
            #cv2.putText(frame, "press 'S' to capture image", (50, 150),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            #cv2.putText(frame, "press 'Q' to quit", (50, 200),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            #print(check)  # prints true as long as the webcam is running
            #print(frame)  # prints matrix values of each framecd
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('s'):
                cv2.imwrite(os.path.join(path,fname+'.jpg'), img=frame)
                webcam.release()
                print("Processing image...")
                img_ = cv2.imread(os.path.join(path,fname+'.jpg'), cv2.IMREAD_ANYCOLOR)    
                break
    
            elif key == ord('q'):
                webcam.release()
                #cv2.destroyAllWindows()
                break
    
        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break

    
    