# Vocal Channel Analyzer
------------------------------

本程式最主要利用 Spleeter 分離人聲的功能,  
幫忙分析出 KTV 檔案中人聲所在的聲道,  
再將分析結果, 把 _vL, _vR 的字串加到檔名最後,  
讓 KTV 加歌程式可以透過檔名判斷出人聲的音軌  


### 安裝說明
----------------------------

本程式需要的環境 :
- python 執行環境
- spleeter 與其所需的套裝軟體
- MediaInfo 程式與 ffmpeg/ffprobe 程式幫忙分析與處理 audio 檔案
    
安裝的方式有幾種 :
1. 若在 Windows 7/10 的環境中,  
  可以下載 [安裝包](https://github.com/ericpeng1968/Vocal-Channel-Analyzer/releases/download/v1.1.1/vocal_ch_analyzer.zip)       
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
        
3. 如果電腦沒有 python 執行環境, 可以參考底下
   *整合包的製作步驟* 自行產生執行環境,
   並且替換自己想用的軟體版本.
   
### 使用說明
----------------------------

執行程式之後, 設定的畫面如下 :  
![image](https://github.com/ericpeng1968/Vocal-Channel-Analyzer/blob/master/screenshot-1.png)

***[來源目錄]***: 指定待處理影片所在目錄  

***[暫存檔目錄]***: 指定處理影片時,暫存檔使用的目錄,若指定於 ramdisk,可以避免硬碟存取, 但空間要夠.
                若可使用空間為 500MB, 且處理整首歌曲, 大概可以處理長度 6 分鐘內歌曲, 超過空間可能會爆掉  
                建議可以選擇分析 1/2 或 1/3 首歌, 省時間也省暫存空間  

***[人聲字串指定]*** : 指定判斷出人聲的聲道後, 要加到檔名後的辨識字串, 一般左聲道(第一音軌)是指定 _vL(_VL),   
                右聲道(第二音軌)是指定 _vR(_VR), 若有其他原因, 請自行更改選項   
                
***[分析區間設定]*** : 人聲分離過程耗比較多時間, 實際上不需要分析整首歌, 只要分析一段有人聲部分的歌曲,  
                應該就可以區分出人聲與伴唱音軌, 這個設定讓使用者自行指定要分析的歌曲區段, 以節省整體分析時間,  
                一般大概分析 1/2 首歌就可以判斷出正確結果

***[略過已有_vL_vR檔案]***: 若檔名已經有 _vL 或 _vR 的識別字串, 就不再處理這檔案  
***[輸出選擇]*** : 分析完的 _vL, _vR 字串結果, 可以選擇輸出到 :
 - 只做分析, 分析結果可看輸出中的*結果*視窗, 不影響檔名或輸出到 .BAT 檔案
 - 直接將結果的 _vL, _vR 字串加到歌曲檔名的最後
 - 將改檔名的動作,儲存到一個 .BAT 的批次檔, 讓使用者先審閱過之後, 再自行開個命令視窗, 執行 .BAT 檔案  

啟動分析的畫面如下 :
![image](https://github.com/ericpeng1968/Vocal-Channel-Analyzer/blob/master/screenshot-2.png)

按了 ***[開始]*** 按鈕之後, 就開始分析來源目錄下,所有附加檔名符合定義的檔案, 分析的結果,  
根據設定中的選擇, 直接修改檔案檔名, 或者將改檔名的指令都匯集到 .bat 的輸出檔中

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
##### 整合包的製作步驟 :

    1. 下載 portable python 3.7 (https://sourceforge.net/projects/portable-python/)
    2. 解壓後, 執行 Console-Launcher.exe 來安裝需要的模組
    3. 在 console 畫面中執行 "python -m pip install --upgrade pip" 更新 pip
    4. 接著執行 "python -m pip install spleeter" 安裝 spleeter(若需要 GPU 支援,請裝 spleeter-gpu)
       然後還需要安裝 dill 與 tkcalendar
    5. 到 App 目錄下, copy mediainfo.exe, ffmpeg.exe, ffprobe.exe 這三個執行檔到此目錄
        mediainfo 從 https://mediaarea.net/en/MediaInfo/Download/Windows 下載 CLI 版本
        ffmpeg/ffprobe 從  https://ffmpeg.org/download.html 下載 windows 版本
    6. 從本計畫中 copy main_ui.py, vocal_ch_analyzer.py 到 App 目錄下
    7. 如果執行時, tensorflow 失敗, 無法載到 msvcp140.dll, 或 msvcp140_1.dll,
       請到網站下載 MS Visual C++ library, 挑選 x86 or x64 版本(看安裝的 python 版本)
       https://support.microsoft.com/zh-tw/help/2977003/the-latest-supported-visual-c-downloads

目前安裝包裏頭, 安裝的是支援 AVX 版本的 tensorflow,  
如果是在比較舊的 CPU(Intel Sandybridge 之前的版本),沒有 AVX support, 跑起來會有錯誤.  
需要再找只有 SSE support 的 tensorflow 版本, 取代掉  
Python/Libs/site-packages 下 tensor 開頭的幾個目錄,  
若是有顯示卡加速, 也可以安裝支援 spleeter-gpu 版本, 應該可以加速許多  

可以到 https://github.com/fo40225/tensorflow-windows-wheel 其他版本的 tensorflow,  
基本上使用 Spleeter 需要用比較快的 CPU 與較大的記憶體(最好有 8GB)

在 AMD Ryzen 5-3600 上執行, 處理一首歌曲大概需 35 秒   
在 Intel i3-540(第一代 Core CPU, 只有支援 SSE), 處理一首歌曲大概需要 230 秒 

---------------------------------------
##### 理論與方法 :

    以理想狀況來講 :
       伴唱的音軌 = 伴唱的音量 + 和聲的音量
       人聲的音軌 = 伴唱的音量 + 和聲的音量 + 主唱的音量
    所以有人聲的音軌, 總"能量"要比伴唱的音軌還高, 用兩音軌的 replaygain(RMS)
    來比較大小, 應該就可以分辨出人聲/伴唱音軌.
    
    但是現實狀況並非如此, 用此方法的錯誤率滿高的, 原因就是在檔案中的音軌,
    實際上音量並非都是一致的, 有可能伴唱音軌的伴唱音量比人聲音軌的伴唱音量高,  
    用 replaygain(RMS) 來判斷, 誤判情況滿多的
    
    有了 spleeter 做分離人聲之後
       伴唱的音軌 -----> 分離出來的聲音幾乎為零(應該就只剩下和聲的聲音)
       人聲的音軌 -----> 分離出來主唱+和聲
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
    這種情況挑任一邊當人聲或伴奏都沒差別.  
    目前的程式沒打算將這種情況另外判斷出來, 但應該有機會可以判斷出.
    
----------------------
#### 後記 :
本程式只是將我在使用中的 KTV 檔工具程式中, 判斷人聲的部分整理出來, 希望可以幫助到有些需要此功能的同好.  
我學習 Python 的時間不長, 目前大概只是用來取代其他 script language 的程度,  
並沒有充分的利用 Python 的特性. 歡迎有興趣的朋友將程式的 idea 改 implement  
在其他的語言與程式中, 讓大家有更多方便的 tools 來使用.
    
       
