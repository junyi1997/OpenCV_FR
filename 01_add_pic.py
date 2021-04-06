import cv2
import os
import numpy as np
from PIL import Image

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
a=k[0].split(',')

for i in range(len(a)):
    bbb.append(a[i])

f = open('Class_Number.txt', 'w')
bbb.append(face_id)

for i in range(len(bbb)):
    if i == len(bbb)-1:ccc=ccc+bbb[i]
    else:ccc=ccc+bbb[i]+','

f.write(ccc)
f.close() 
print("新增資料：學號 = {:} / 編號 = {:}".format(face_id,len(bbb)-1))


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
            cv2.imwrite("dataset/" + str(len(bbb)-1) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

            
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


# Path for face image database
path = './dataset'

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# function to get the images and label data
def getImagesAndLabels(path):

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        
        #id = int(str(os.path.split(imagePath)[-1].split(".")[1]))

        idddd=str(os.path.split(imagePath)[-1])
        id=int(idddd.split(".")[0])
        
        faces = detector.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)

    return faceSamples,ids

print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces,ids = getImagesAndLabels(path)
#print("ids = ".format(ids))
recognizer.train(faces, np.array(ids))

# Save the model into trainer/trainer.yml
recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi

# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))