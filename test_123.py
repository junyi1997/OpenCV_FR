import BotSpeak
#threading引用必要套件
from threading import Thread
import threading

def BOT(speaker):
    BotSpeak.speak(speaker)
face_id='M10907324'
bbb=2
aaaa="新增資料：學號 = {:} / 編號 = {:}".format(face_id,bbb)
Thread(target=BOT,args =(aaaa,)).start()