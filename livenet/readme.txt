# liveness detection module
developed by AdaChen based on project of Adrian Rosebrock form pyimagesearch
python 3.7.7
last update 2021/02/03

===

# 檔案說明:
livenet
├─__pycache__:cache file
├─detector:人臉偵測模型
├─demo.py:示範活體模型功能之程式
├─le.pickle:活體辨識標籤檔案
├─li.py:活體辨識class module
├─liveness.model:活體辨識模型
├─readme.txt:本文件
└─requirements.txt:環境安裝列表

===

# usage:
## 環境安裝
$ python -m pip install --upgrade pip
$ pip install -r requirements.txt

## 模型示範
目前model能辨識出之種類有真人、證件照、手機畫面三種
$ python demo.py
按q退出程式

## 模組使用
### function說明
* getLiveLabelfromImgandCoords
    * input(攝影機完整畫面、臉部框框左上X座標、臉部框框左上Y座標、臉部框框右下X座標、臉部框框右下Y座標、攝影機完整畫面寬、攝影機完整畫面高)
    * output(標示名稱、信心指數、標示顏色)
    * 說明:外部程式傳入已偵測到之臉部座標，再使用攝影機畫面進行裁切壓縮處理，能減少重複臉部偵測運算
    * 備註:input值中的cw、ch其實能夠直接從img參數讀取，可以把這部分修掉減少兩項參數的傳遞
* getLiveLabelfromImg
    * input(攝影機完整畫面)
    * output(標示名稱、信心指數、標示顏色)
    * 說明:直接傳入完整攝影機畫面，進行臉部偵測、裁切、壓縮、識別，這裡使用opencv內建的resnet10進行偵測，缺點是運算量較大
* getLiveLabel
    * input(裁切好之臉部畫面)
    * output(標示名稱、信心指數、標示顏色)
    * 說明:將外部程式處理好之畫面進行辨識，要注意此處"裁切好之臉部畫面"指的是臉部左右延伸1.3倍畫面再壓縮成32*32大小之畫面

### 注意事項
* 使用時請更改model、le、net存取位置
* 若辨識時雖然為real，但其pred值未超過REAL_THRESHOLD，程式也會return fake
* 若人臉色調偏白、偏黃、旁邊有直條物(窗框、黑板框等)容易被辨識成手機畫面
* 目前尚有部分手機因畫值很好能夠通過辨識，若有需要增強此部分請再聯絡我
* 戴口罩會影響辨識結果
* opencv rgb順序會影響辨識，在傳輸圖片時請注意

