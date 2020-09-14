### Vocal Channel Analyzer
------------------------------

本程式利用 Spleeter 分離出人聲之後,
幫忙分析出 KTV 檔案中人聲所在的聲道.

本程式需要的環境 :
- python 執行環境
- spleeter 與其所需的套裝軟體
- mediainfo 程式與 ffmpeg/ffprobe 程式幫忙分析與處理 audio 檔案

執行主 UI 程式之後, 設定的畫面如下 :
![image](https://github.com/ericpeng1968/Vocal-Channel-Analyzer/blob/master/screenshot-1.png)
[來源目錄]: 指定待處理影片所在目錄

[暫存檔目錄]: 指定處理影片時,暫存檔使用的目錄,若指定於 ramdisk,可以避免硬碟存取, 至少要有 500MB 可使用空間

[不處理已有_vL_vR檔案]: 若檔名已經有 _vL 或 _vR 的識別字串, 就不再處理這檔案

掃描過的結果, 可以將 _vL, _vR 的字串直接修改到硬碟上的檔名, 或者將改檔名的動作,
儲存到一個 .bat 的批次檔, 讓使用者先審閱過之後, 再自行開個命令視窗, 執行 .bat 檔案

執行掃描的畫面如下 :
![image](https://github.com/ericpeng1968/Vocal-Channel-Analyzer/blob/master/screenshot-2.png)

# 支援的檔案類型
目前支援的檔案附加檔名, 有 mpg, mpeg, vob, mkv, avi, dat 幾種.
若是沒有定義到想支援的檔名, 請自行修改 main_ui.py 中的定義 :

```python
  \# define the file extension type to process 
  ext_list = [".mpg", ".mpeg", ".vob", ".mkv", ".avi", ".dat"]
```
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

如果是在比較舊的 CPU(Intel Sandybridge 之前的版本),沒有 AVX support,
需要再找只有 SSE support 的 tensorflow 版本, 取代掉
Python/Libs/site-packages 下 tensor 開頭的幾個目錄,

可以到 https://github.com/fo40225/tensorflow-windows-wheel 下載 SSE 版
還是建議用快一點的 CPU 及較多記憶體來執行,

在 AMD Ryzen 5-3600 上執行, 處理 5 首歌曲大概需 3 分鐘 
