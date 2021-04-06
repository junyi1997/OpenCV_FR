''''
Real Time Face Recogition
	==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc                       
	==> LBPH computed model (trained faces) should be on trainer/ dir
Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18  

'''

import cv2
import numpy as np
import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import pickle
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

REAL_THRESHOLD = 0.8 #will return fake if pred of real doesnt exceed threshold
std_correct_time=0


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = [] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

f = open('Class_Number.txt','r')
k = f.readlines()
f.close()
a=k[0].split(',')

for i in range(len(a)):
    names.append(a[i])   
#########V新增防止闖關V#########

model = load_model("./livenet/liveness.model")
le = pickle.loads(open("./livenet/le.pickle", "rb").read())
net = cv2.dnn.readNetFromCaffe("./livenet/detector/deploy.prototxt.txt", "./livenet/detector/res10_300x300_ssd_iter_140000.caffemodel")
label = ""
pred = ""

observed_resual=''
correct_count=5
def getLiveLabelfromImgandCoords(img, startX, startY, endX, endY, cw, ch):
    global model,le,net,label,pred
    lsy = startY
    lsx = startX
    ley = endY
    lex = endX
    fw = lex - lsx
    fh = ley - lsy
    rw = 1.3
    rh = 0
    if lsx - rw*fw > 0:
	    lsx = int(lsx - rw*fw)
    else:
	    lsx = 0
    if lsy - rh*fh > 0:
	    lsy = int(lsy - rh*fh)
    else:
	    lsy = 0
    if lex + rw*fw < cw:
	    lex = int(lex + rw*fw)
    else:
	    lex = cw
    if ley + rh*fh < ch:
	    ley = int(ley + rh*fh)
    else:
	    ley = ch
    liveFace = img[lsy:ley, lsx:lex]
    liveFace = cv2.resize(liveFace, (32, 32))

    liveFace = liveFace.astype("float") / 255.0
    liveFace = img_to_array(liveFace)
    liveFace = np.expand_dims(liveFace, axis=0)
    preds = model.predict(liveFace)[0]

    j = np.argmax(preds)

    label = le.classes_[j]
    pred = str(round(preds[j],2))

    if le.classes_[j] == "real" :
        if preds[j] > REAL_THRESHOLD:
            pass
        else:
            label = "false"

    return label
#########^0215新增防止闖關^#########  
import os
import time
def UnKnow_process(frame):
  Y=time.strftime("%Y", time.localtime()) 
  M=time.strftime("%m", time.localtime()) 
  D=time.strftime("%d", time.localtime()) 
  H=time.strftime("%H", time.localtime()) 
  Min=time.strftime("%M", time.localtime()) 
  Sec=time.strftime("%S", time.localtime()) 

  #a="{:}-{:}-{:} {:}:{:}:{:}".format(Y,M,D,H,Min,Sec)
  path="./UnKnow/{:}-{:}-{:}".format(Y,M,D)
  folder = os.path.exists(path)
  #判斷結果
  if not folder:
      #如果不存在，則建立新目錄
      os.makedirs(path)
      print('-----建立成功-----')

  savepath="./UnKnow/{:}-{:}-{:}/{:}h{:}m{:}s.jpg".format(Y,M,D,H,Min,Sec)
  cv2.imwrite(savepath, frame)

# 引入 requests 模組
import requests
IP="192.168.100.11"
def SendURL(sendword):
  #print(sendword)
  if sendword == "real":
    a="http://{:}/gpio/R_off".format(IP)
    r = requests.get(a)
    a="http://{:}/gpio/Y_off".format(IP)
    r = requests.get(a)
    a="http://{:}/gpio/G_on".format(IP)
    r = requests.get(a)
  elif sendword == "wait":
    a="http://{:}/gpio/R_off".format(IP)
    r = requests.get(a)
    a="http://{:}/gpio/Y_on".format(IP)
    r = requests.get(a)
    a="http://{:}/gpio/G_off".format(IP)
    r = requests.get(a)
  elif sendword == "false":
    a="http://{:}/gpio/R_on".format(IP)
    r = requests.get(a)
    a="http://{:}/gpio/Y_off".format(IP)
    r = requests.get(a)
    a="http://{:}/gpio/G_off".format(IP)
    r = requests.get(a)
  elif sendword == "UnKnow":
    a="http://{:}/gpio/R_on".format(IP)
    r = requests.get(a)
    a="http://{:}/gpio/Y_off".format(IP)
    r = requests.get(a)
    a="http://{:}/gpio/G_off".format(IP)
    r = requests.get(a)
  elif sendword == "off":
    a="http://{:}/gpio/R_off".format(IP)
    r = requests.get(a)
    a="http://{:}/gpio/Y_off".format(IP)
    r = requests.get(a)
    a="http://{:}/gpio/G_off".format(IP)
    r = requests.get(a)
  elif sendword == "stay":
    a="http://{:}/gpio/R_off".format(IP)
    r = requests.get(a)
    a="http://{:}/gpio/Y_off".format(IP)
    r = requests.get(a)
    a="http://{:}/gpio/G_off".format(IP)
    r = requests.get(a)
    a="http://{:}/gpio/stay".format(IP)
    r = requests.get(a)

while True:

    ret, img =cam.read()
    img = cv2.flip(img, 1) # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )
    range_min = 150
    range_max = 200
    
    for(x,y,w,h) in faces:
        x1,y1,x2,y2=x,y,x+w,y+h
        #if w>range_max and h>range_max:print("請再遠離一點......")
        #if w<range_min and h<range_min:print("請再靠近一點......")
        if w>range_min and h>range_min and w<range_max and h<range_max:
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            h1,w1,l = np.shape(img)
            #print("confidence = {:}".format(confidence))
            
            
            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 60):
                #id = names[id]
                color=(255,255,0)
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                color=(0,0,255)
                confidence = "  {0}%".format(round(100 - confidence))
            
            if id!="unknown":
                observed_resual_singal=getLiveLabelfromImgandCoords(img,x1,y1,x2,y2,w1,h1)
                #print("x = {:} y = {:} w = {:} h = {:} w1 = {:} h1 = {:}".format(x1,y1,x2,y2,h1,h1))
            else:
                observed_resual_singal="unknown"
            #print("observed_resual = {:}".format(observed_resual))
            if observed_resual_singal == "real":
                std_correct_time+=1 
            else:                                
                std_correct_time=0
            #print("std_correct_time = {:}".format(std_correct_time))
            if id=="unknown":
                if observed_resual!="unknown":
                    #SendURL("UnKnow") 
                    UnKnow_process(img)
                observed_resual="unknown"
                color=(0,0,255)#blue  
            if abs(x1-x2)>100 and abs(y1-y2)>100 and observed_resual!="real":
                if std_correct_time>=correct_count:
                    #if observed_resual!="real":SendURL("real")
                    observed_resual="real"
                    color=(128,255,0)#green
                
                elif std_correct_time>0 and std_correct_time<correct_count:
                    #if observed_resual!="wait":SendURL("wait")
                    observed_resual="wait"
                    color=(0,255,255)#yellow
                
                elif std_correct_time==0 and id!="unknown":
                    #if observed_resual!="false":SendURL("false")
                    observed_resual="false"
                    color=(255,0,0)#red

 
 
            elif abs(x1-x2)<100 and abs(y1-y2)<100:
                #清除辨識結果
                observed_resual=""
                std_correct_time=0
                #SendURL("stay")


            cv2.rectangle(img, (x,y), (x+w,y+h), color, 2)
            if id == "unknown" : cv2.putText(img, str(id), (x+5,y-5), font, 1, color, 2)
            else : cv2.putText(img, str(names[id]), (x+5,y-5), font, 1, color, 2)
            #cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, color, 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
