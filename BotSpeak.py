import os
import pygame
from pygame import mixer    
from gtts import gTTS
import time
a="這是紙類"
b=""
def speak_i():
    mixer.init()    # 初始化
    if not os.path.isfile('tmp.mp3'):    # 不重要的聲音檔產生器
        tts = gTTS(text = '不重要的語音檔', lang = 'zh-tw')
        tts.save('tmp.mp3')
        print('已產生不重要的語音檔 tmp.mp3')
    #-----------------#
def bot_speak(text, lang):    # 建立自訂函式
    try: 
        mixer.music.load('tmp.mp3')    # 讀取不重要的聲音檔
        tts = gTTS(text=text, lang=lang)   
        b='{:}.mp3'
        b=b.format(a)
#        tts.save('歡迎來到智慧分類垃圾桶.mp3')    
#        mixer.music.load('歡迎來到智慧分類垃圾桶.mp3')	  
        tts.save(b)    
        mixer.music.load(b)	
        mixer.music.play()    # 播放重要的聲音檔
#        if input("") =="q":
#            stop()
        while(mixer.music.get_busy()):    
            continue
    
    except:
        print('播放音效失敗')
def stop():
   pygame.mixer.music.stop()         
    #-----------------#
def speak(text):

    speak_i()
    stop()
    #bot_speak(text,'zh-tw')  # 說出text
    bot_speak(text,'zh-tw')  # 說出text
#    bot_speak("歡迎來到智慧分類垃圾桶",'zh-tw')  # 說出text
    

            
        
        
    
def mymain():
    speak('123456789012345678901234567890')

if __name__=="__main__":
    mymain()