''''
Capture multiple Faces from multiple users to be stored on a DataBase (dataset directory)
	==> Faces will be stored on a directory: dataset/ (if does not exist, pls create one)
	==> Each face will have a unique numeric integer ID as 1, 2, 3, etc                       

Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18    

'''

import cv2
import os

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# For each person, enter one numeric face id
face_id = input('\n enter user id end press <return> ==>  ')
bbb=[]
ccc=''
f = open('Class_Number.txt','r')
k = f.readlines()
f.close()
print("讀取成功....")
a=k[0].split(',')

for i in range(len(a)):
    bbb.append(a[i])

f = open('Class_Number.txt', 'w')
bbb.append(face_id)

for i in range(len(bbb)):
    if i == len(bbb)-1:ccc=ccc+bbb[i]
    else:ccc=ccc+bbb[i]+','
print(len(bbb))
f.write(ccc)
print("寫入成功....")
f.close() 
print("離開學號登記....")

print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count
count = 0

while(True):

    ret, img = cam.read()
    img = cv2.flip(img, 1) # flip video image vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    cv2.imshow('image', img)
    for (x,y,w,h) in faces:
        
        if w>100 and h>100:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1

            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + str(len(bbb)) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

            
            print(str(count) + ".jpg Done")

    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 5: # Take 30 face sample and stop video
         break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()


