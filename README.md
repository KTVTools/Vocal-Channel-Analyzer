### Vocal Channel Analyzer

本程式利用 Spleeter 分離出人聲之後,
幫忙分析出 KTV 檔案中人聲所在的聲道.


整合包的製作步驟 :
1. 下載 portable python 3.7 (https://sourceforge.net/projects/portable-python/)
2. 解壓後, 執行 Console-Launcher.exe 來安裝需要的模組
3. 在 console 畫面中執行 "python -m pip install --upgrade pip" 更新 pip
4. 接著執行 "python -m pip install spleeter" 安裝 spleeter
5. 到 App 目錄下, copy mediainfo.exe, ffmpeg.exe, ffprobe.exe 這三個執行檔到此目錄
      mediainfo 從 https://mediaarea.net/en/MediaInfo/Download/Windows 下載 CLI 版本
      ffmpeg/ffprobe 從  https://ffmpeg.org/download.html 下載 windows 版本
6. 從本計畫中 copy main_ui.py, vocal_ch_analyzer.py 到 App 目錄下

如果是在比較舊的 CPU(Intel Sandybridge 之前的版本),將沒有 AVX support,
需要再找只有 SSE support 的 tensorflow 版本, 取代掉
Python/Libs/site-packages 下 tensor 開頭的幾個目錄
