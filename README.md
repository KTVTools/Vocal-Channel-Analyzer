# Vocal Channel Analyzer
------------------------------

本程式最主要利用 Spleeter 分離人聲的功能,  
幫忙分析出 KTV 檔案中人聲所在的聲道, 
再將分析結果, 把 _vL, _vR 的字串到檔名最後,  
讓 KTV 加歌程式可以透過檔名判斷出人聲的音軌  


### 安裝說明
----------------------------

本程式需要的環境 :
- python 執行環境
- spleeter 與其所需的套裝軟體
- MediaInfo 程式與 ffmpeg/ffprobe 程式幫忙分析與處理 audio 檔案
    
安裝的方式有幾種 :
1. 若在 Windows 7/10 的環境中,  
  可以下載 [安裝包](https://github.com/ericpeng1968/Vocal-Channel-Analyzer/releases/download/v1.0.0/vocal_ch_analyzer.zip)       
  解開 vocal_ch_analyzer.zip 之後, 執行裏頭的  
  **vocal_ch_analyzer.wsf** 檔案即可.  
  或者開啟命令視窗, 在解開的目錄中,  
  執行 **python\python.exe main_ui.py**  
    
2. 如果電腦系統中已經有 python 執行環境,  
  請安裝好 Spleeter 套件,  
  並且將 mediainfo 與 ffmpeg/ffprobe 放在執行的目錄中.  
  接下來從本專案將 main_ui.py 與 analyzer_core.py 下載到執行目錄,  
  只要執行 **python main_ui.py** 就可以啟動程式  
  (若 spleeter 無法正確被呼叫, 或者在 Linux 環境執行,  
   請修改 analyzer_core.py 中 spleeter 等命令的執行字串)  
        
     
### 使用說明
----------------------------

執行程式之後, 設定的畫面如下 :  
![image](https://github.com/ericpeng1968/Vocal-Channel-Analyzer/blob/master/screenshot-1.png)

[來源目錄]: 指定待處理影片所在目錄  

[暫存檔目錄]: 指定處理影片時,暫存檔使用的目錄,若指定於 ramdisk,可以避免硬碟存取, 至少要有 500MB 可使用空間  

[人聲字串指定] : 指定判斷出人聲的聲道後, 要加到檔名後的辨識字串, 一般左聲道(第一音軌)是指定 _vL(_VL),   
                右聲道(第二音軌)是指定 _vR(_VR), 若有其他原因, 請自行更改選項   
                
[不處理已有_vL_vR檔案]: 若檔名已經有 _vL 或 _vR 的識別字串, 就不再處理這檔案  

分析人聲過的結果, 可以將 _vL, _vR 的字串  
- 直接修改到硬碟上的檔名,   
- 將改檔名的動作,儲存到一個 .bat 的批次檔, 讓使用者先審閱過之後, 再自行開個命令視窗, 執行 .bat 檔案  

啟動分析的畫面如下 :
![image](https://github.com/ericpeng1968/Vocal-Channel-Analyzer/blob/master/screenshot-2.png)

按了 [開始] 按鈕之後, 就開始分析來源目錄下,所有附加檔名符合定義的檔案

### 支援的檔案類型
目前支援的檔案附加檔名, 有 mpg, mpeg, vob, mkv, avi, dat 幾種.
若是沒有定義到想支援的附加檔名, 請自行修改 ***main_ui.py*** 中的定義,
附加檔名請都用小寫的

```python
  # define the file extension type to process 
  ext_list = [".mpg", ".mpeg", ".vob", ".mkv", ".avi", ".dat"]
```

## 以下為技術相關內容
------------------------------------------
整合包的製作步驟 :

    1. 下載 portable python 3.7 (https://sourceforge.net/projects/portable-python/)
    2. 解壓後, 執行 Console-Launcher.exe 來安裝需要的模組
    3. 在 console 畫面中執行 "python -m pip install --upgrade pip" 更新 pip
    4. 接著執行 "python -m pip install spleeter" 安裝 spleeter
    5. 到 App 目錄下, copy mediainfo.exe, ffmpeg.exe, ffprobe.exe 這三個執行檔到此目錄
        mediainfo 從 https://mediaarea.net/en/MediaInfo/Download/Windows 下載 CLI 版本
        ffmpeg/ffprobe 從  https://ffmpeg.org/download.html 下載 windows 版本
    6. 從本計畫中 copy main_ui.py, vocal_ch_analyzer.py 到 App 目錄下

目前安裝包裏頭, 安裝的是支援 AVX 版本的 tensorflow,
如果是在比較舊的 CPU(Intel Sandybridge 之前的版本),沒有 AVX support, 跑起來會有錯誤.
需要再找只有 SSE support 的 tensorflow 版本, 取代掉
Python/Libs/site-packages 下 tensor 開頭的幾個目錄,
若是有顯示卡加速, 也可以安裝支援 GPU 版本的 tensorflow, 應該可以加速許多

可以到 https://github.com/fo40225/tensorflow-windows-wheel 其他版本的 tensorflow,
基本上使用 Spleeter 需要用比較快的 CPU 與較大的記憶體(最好有 8GB)

在 AMD Ryzen 5-3600 上執行, 處理一首歌曲大概需 35 秒  
在 Intel i3-540(第一代 Core CPU, 只有支援 SSE), 處理一首歌曲大概需要 230 秒 

---------------------------------------
理論與方法 :

    古早以前, 會利用 KTV 檔案中的左右聲道或第一第二音軌的 replaygain 或音量 RMS,
    來判斷人聲的音軌. 因為如果照理論來講 :
       伴唱的音軌 = 伴唱的音量 + 和聲的音量
       人聲的音軌 = 伴唱的音量 + 和聲的音量 + 主唱的音量
    所以有人聲的音軌, 總"能量"要比伴唱的音軌還高, 用兩音軌的 replaygain(RMS)
    來比較大小, 應該就可以分辨出人聲/伴唱音軌.
    但是現實狀況並非如此, 用此方法的錯誤率滿高的, 原因就是在檔案中的音軌,
    實際上音量都是一致的, 用 replaygain(RMS) 來判斷, 誤判情況滿多的
    
    有了 spleeter 做分離人聲之後
       伴唱的音軌 -----> 分離出來的聲音幾乎為零(應該就只剩下和聲的聲音)
       有人聲的音軌 ---> 分離出來純人聲的清唱+和聲
    再來比較分離出來人聲的音量, 兩者的"能量"(replaygain or RMS) 差別就非常大,
    用來判斷人聲的音軌錯誤率應該可以很低,
    目前能想到誤判的情況, 大概只有和聲很多的歌曲(像 RAP 歌曲),而且伴唱音軌音量很大的情況,
    應該還是有可能會發生誤判, 只是實務上, 目前測試過的歌曲還沒發現過誤判.

    本程式判斷的流程 :
    - mediainfo 來判斷有幾個音軌, 若為一個音軌, 則當作是左右聲道有伴唱/人聲兩個獨立聲道
      若有 2 個音軌以上, 則以第一與第二音軌來判斷伴唱/人聲
    - ffmpeg 用來將左右聲道, 或者第一第二音軌分離出來, 產生 ch0 與 ch1 的 wave 檔案到暫存區
    - Spleeter 可以將人聲與伴奏分離, 所以針對暫存區的 ch0, ch1 wave 檔做人聲與伴奏的分離
    - ffmpeg 再來計算 ch0 與 ch1 分離出的人聲部份的 replaygain, replaygain 比較大的,表示聲音小
    
    因此最後利用 replaygain 比較, 值比較小的, 表示音量能量大, 是有人聲的音軌.
    如果是正常有人聲/伴奏的檔案, replaygain 的差別會很大, 很容易判斷.
    如果遇到完全沒人聲的(只有一個音軌的 stereo 伴奏), 左右兩個音軌人聲的 replaygain 差別就會很小,
    這種情況挑任一邊當人聲或伴奏都沒差別.  目前的程式沒打算將這種情況另外判斷出來, 但應該有機會可以判斷出.
    
    
       
