#======================
# imports
#======================
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as msg
from tkinter import Spinbox
from time import  sleep         # careful - this can freeze the GUI
from tkcalendar import Calendar, DateEntry
from tkinter import filedialog as fd
import os
import sys
from datetime import date
import time
import requests
import dill
import pandas as pd
from io import StringIO
import sqlite3
import math
import vocal_ch_analyzer

# define the file extension type to process
ext_list = [".mpg", ".mpeg", ".vob", ".mkv"]


# define appending string for [VCD vocal, VCD kara, DVD vocal, DVD kara], default is 4
VL_STR=[['_vL', '_vR', '_vL', '_vR'],
        ['_VL', '_VR', '_vL', '_vR'],
        ['_vR', '_vL', '_vL', '_vR'],
        ['_VR', '_VL', '_vL', '_vR'],
        ['_vL', '_vR', '_VL', '_VR'],
        ['_VL', '_VR', '_VL', '_VR'],
        ['_vR', '_vL', '_VL', '_VR'],
        ['_VR', '_VL', '_VL', '_VR'],
        ['_vL', '_vR', '_vR', '_vL'],
        ['_VL', '_VR', '_vR', '_vL'],
        ['_vR', '_vL', '_vR', '_vL'],
        ['_VR', '_VL', '_vR', '_vL'],
        ['_vL', '_vR', '_VR', '_VL'],
        ['_VL', '_VR', '_VR', '_VL'],
        ['_vR', '_vL', '_VR', '_VL'],
        ['_VR', '_VL', '_VR', '_VL']]


# Create instance
win = tk.Tk()   

# Add a title       
win.title("Vocal Channel Determination")  

tabControl = ttk.Notebook(win)          # Create Tab Control

tab1 = ttk.Frame(tabControl)            # Create a tab 
tabControl.add(tab1, text='環境設定')      # Add the tab
tab2 = ttk.Frame(tabControl)            # Add a second tab
tabControl.add(tab2, text='輸出')
tabControl.pack(expand=1, fill="both")  # Pack to make visible

#
# setting area
#
area_config = ttk.LabelFrame(tab1, text=' 目錄設定 ')
area_config.grid(column=0, row=0, padx=8, pady=4, sticky=tk.W)

def getDirName():
    fDir = os.path.dirname(os.path.abspath('__file__'))
    fName = fd.askdirectory(parent=win, title='choose stock data dir', initialdir=fDir)
    if fName :
        filedir.set(fName)
    
ttk.Button(area_config, text="來源目錄", command=getDirName).grid(column=0, row=0, sticky=tk.W)
filedir = tk.StringVar()
filedir.set((os.path.dirname(os.path.abspath('__file__'))).replace('\\','/'))
filedirLen = 60
filedirEntry = ttk.Entry(area_config, width=filedirLen,textvariable=filedir)
filedirEntry.grid(column=1, row=0, sticky=tk.W)

def gettempDirName():
    fDir = os.path.dirname(os.path.abspath('__file__'))
    fName = fd.askdirectory(parent=win, title='choose stock data dir', initialdir=fDir)
    if fName :
        tempdir.set(fName)
    
ttk.Button(area_config, text="暫存檔目錄", command=gettempDirName).grid(column=0, row=1, sticky=tk.W)
tempdir = tk.StringVar()
tempdir.set((os.path.dirname(os.path.abspath('__file__'))).replace('\\','/'))
tempdirLen = 60
tempdirEntry = ttk.Entry(area_config, width=tempdirLen,textvariable=tempdir)
tempdirEntry.grid(column=1, row=1, sticky=tk.W)

# vocal string setting part
area_vocalstr = ttk.LabelFrame(tab1, text=' 人聲字串指定 ')
area_vocalstr.grid(column=0, row=2, padx=8, pady=4, sticky=tk.W)

vocal_strs=["_vL", "_VL", "_vR", "_VR"]
mono_str=vocal_strs[0]
multi_str=vocal_strs[1]

def radCallmono():
    mono_Sel=monoVar.get()
    mono_str=vocal_strs[mono_Sel]
    monoR_Label.configure(text='  |  右聲道人聲: '+VL_STR[monoVar.get()+multiVar.get()*4][1])
    multiR_Label.configure(text='  |  第二軌人聲: '+VL_STR[monoVar.get()+multiVar.get()*4][3])
def radCallmulti():
    multi_Sel=multiVar.get()
    multi_str=vocal_strs[multi_Sel]
    monoR_Label.configure(text='  |  右聲道人聲: '+VL_STR[monoVar.get()+multiVar.get()*4][1])
    multiR_Label.configure(text='  |  第二軌人聲: '+VL_STR[monoVar.get()+multiVar.get()*4][3])
    
ttk.Label(area_vocalstr, text="單音軌左聲道人聲:").grid(column=0, row=2, sticky=tk.W)
monoVar = tk.IntVar()
monoVar.set(0)
for col in range(4):                             
    curRad = tk.Radiobutton(area_vocalstr, text=vocal_strs[col], variable=monoVar, 
                            value=col, command=radCallmono)          
    curRad.grid(column=col+1, row=2, sticky=tk.W) 
monoR_Label=ttk.Label(area_vocalstr)
monoR_Label.grid(column=5, row=2, sticky=tk.W)

    
ttk.Label(area_vocalstr, text="多音軌第一軌人聲:").grid(column=0, row=3, sticky=tk.W)
multiVar = tk.IntVar()
multiVar.set(1)
for col in range(4):                             
    curRad = tk.Radiobutton(area_vocalstr, text=vocal_strs[col], variable=multiVar, 
                            value=col, command=radCallmulti, state='normal')          
    curRad.grid(column=col+1, row=3, sticky=tk.W)
multiR_Label=ttk.Label(area_vocalstr)
multiR_Label.grid(column=5, row=3, sticky=tk.W)
monoR_Label.configure(text='  |  右聲道人聲: '+VL_STR[monoVar.get()+multiVar.get()*4][1])
multiR_Label.configure(text='  |  第二軌人聲: '+VL_STR[monoVar.get()+multiVar.get()*4][3])

# output setting
area_output = ttk.LabelFrame(tab1, text=' 輸出設定 ')
area_output.grid(column=0, row=3, padx=8, pady=4, sticky=tk.W)

SkipFileEn = tk.IntVar()
SkipFilecb = tk.Checkbutton(area_output, text="不處理已有_vL_vR檔案", variable=SkipFileEn)
SkipFilecb.deselect()
SkipFilecb.grid(column=0, row=0, sticky=tk.W)

ModFileEn = tk.IntVar()
checkbox = tk.Checkbutton(area_output, text="判斷的結果直接修改檔名", variable=ModFileEn)
checkbox.deselect()
checkbox.grid(column=0, row=1, sticky=tk.W)                     

def getOutFileName():
    fDir = os.path.dirname(os.path.abspath('__file__'))
    print("fdir=",fDir)
    fName = fd.asksaveasfilename(parent=win, title='指定BAT檔名', filetypes=(('BAT', '*.bat'), ('All Files', '*')), initialdir=fDir)
    if fName :
        outfilename.set(fName)

outfilebtn=ttk.Button(area_output, text="判斷結果改輸出到BAT檔", command=getOutFileName)
outfilebtn.grid(column=0, row=2, stick=tk.W)
outfilename = tk.StringVar()
outfilename.set((os.path.dirname(os.path.abspath('__file__'))+'/result.bat').replace('\\', '/'))
outfilenameLen=60
outfilenameEntry = ttk.Entry(area_output, width=outfilenameLen, textvariable=outfilename)
outfilenameEntry.grid(column=1, row=2, sticky=tk.W)

# GUI Callback function 
def checkCallback(*ignoredArgs):
    # either modfileen or output file selection enabled
    if ModFileEn.get(): 
        outfilebtn.configure(state='disabled')
        outfilenameEntry.configure(state='disabled')
    else:             
        outfilebtn.configure(state='normal')
        outfilenameEntry.configure(state='normal')

# trace the state of the two checkbuttons
ModFileEn.trace('w', lambda unused0, unused1, unused2 : checkCallback())

#############################
### ------- tab2 output 
#############################
area_execute = ttk.LabelFrame(tab2, text='啟動')
area_execute.grid(column=0, row=0, padx=8, pady=4, sticky=tk.W)

def progressbar_update(status_text, percentage):
    status_line_l.configure(text=status_text)
    progress_b["value"]=int(percentage)
    progress_b.update()
    
def progressbar_reset():
    status_line_l.configure(text='idle')
    progress_b["value"]=0
    progress_b.update()

def Run_Analyze(dirpath, fileitem, tmpdir, outf_hd, vl_str):
    return vocal_ch_analyzer.vocal_analyze(dirpath, fileitem, tmpdir, outf_hd, vl_str)

    
def StartCMD():
    startbtn.configure(state='disabled')
    run_state.set(STATE_RUN)
    stopbtn.configure(state='normal')
    pausebtn.configure(state='normal')
    # freeze the current setting, so the value will not be changed if users change UI 
    Fsrcdir=filedir.get()
    Ftmpdir=tempdir.get()
    Fbatfilename=outfilename.get()
    FSkipFileEn=SkipFileEn.get()
    Fvl_str=VL_STR[monoVar.get()+multiVar.get()*4]
    FModFileEn=ModFileEn.get()
    if FModFileEn:
        Foutf_hd=None
    else:
        Foutf_hd=open(Fbatfilename, "wt", encoding="utf8")
        print("chcp 65001\n", file=Foutf_hd)
        
    print(filedir.get(), tempdir.get(), outfilename.get(), SkipFileEn.get(), VL_STR[monoVar.get()+multiVar.get()*4])
    total_items=0
    logarea.delete('1.0', tk.END)   # clear text area
    for dirpath, dirlist, filelist in os.walk(Fsrcdir):
        for fileitem in filelist:
            fullpath=os.path.join(dirpath, fileitem)
            filename, fileext = os.path.splitext(fileitem)
            for ext_name in ext_list:
                if fileext.lower()==ext_name: 
                    total_items=total_items+1
                    
    cur_item=0
    for dirpath, dirlist, filelist in os.walk(Fsrcdir):
        for fileitem in filelist:
            fullpath=os.path.join(dirpath, fileitem)
            filename, fileext = os.path.splitext(fileitem)
            for ext_name in ext_list:
                if fileext.lower()==ext_name:
                    if (run_state.get()==STATE_PAUSE):
                        pausebtn.configure(state='normal')
                        startbtn.wait_variable(run_state)   # wait until run_state change value
                        pausebtn.configure(state='normal')
                    if (run_state.get()==STATE_STOP):
                        startbtn.configure(state='normal')
                        stopbtn.configure(state='disabled')
                        pausebtn.configure(state='disabled')
                        logarea.insert(tk.END, 'user stopped\n')
                        progressbar_reset()
                        if Foutf_hd != None:
                            Foutf_hd.close()
                        return

                    cur_item=cur_item+1
                    if (FSkipFileEn>0):  
                        if ((fileitem.lower().find('_vl')>=0) or (fileitem.lower().find('_vr')>=0)):
                            # skip enabled and filename has _vl or _vr
                            progressbar_update('skipping '+fileitem, cur_item*100/total_items)
                            logarea.insert(tk.END, 'skipping '+filename+'\n')
                            if Foutf_hd!=None:
                                print("REM skipping "+filename+'\n', file=Foutf_hd)
                            continue
                    progressbar_update('processing '+fileitem, cur_item*100/total_items)
                    logarea.insert(tk.END, 'processing '+fileitem+'\n')
                    if (Run_Analyze(dirpath, fileitem, Ftmpdir, Foutf_hd, Fvl_str)!=0):
                        logarea.insert(tk.END, 'error on '+filename+'\n')
                
    startbtn.configure(state='normal')
    stopbtn.configure(state='disabled')
    pausebtn.configure(state='disabled')
    run_state.set(STATE_STOP)
    progressbar_reset()
    if Foutf_hd != None:
        Foutf_hd.close()

def StopCMD():
    run_state.set(STATE_STOP)
    
def PauseCMD():
    if (pausebtn.cget("text")=="暫停"):
        pausebtn.configure(text="繼續")
        run_state.set(STATE_PAUSE)
        pausebtn.configure(state='disabled')
    else:
        pausebtn.configure(text="暫停")
        run_state.set(STATE_RUN)
        pausebtn.configure(state='disabled')

STATE_STOP=0
STATE_PAUSE=1
STATE_RUN=2
run_state=tk.IntVar()
run_state.set(STATE_STOP)
        
startbtn=ttk.Button(area_execute, text="開始", command=StartCMD)
startbtn.grid(column=0, row=0, sticky=tk.W)
pausebtn=ttk.Button(area_execute, text="暫停", command=PauseCMD)
pausebtn.grid(column=1, row=0, sticky=tk.W)
pausebtn.configure(state='disabled')
stopbtn=ttk.Button(area_execute, text="停止", command=StopCMD)
stopbtn.grid(column=2, row=0, sticky=tk.W)
stopbtn.configure(state='disabled')

area_log = ttk.LabelFrame(tab2, text='結果')
area_log.grid(column=0, row=1, padx=8, pady=4, sticky=tk.W)
logarea = scrolledtext.ScrolledText(area_log,width=80,height=10)
logarea.grid(column=0, row=0, sticky=tk.W)


#
# status area
#
area_status = ttk.LabelFrame(tab2, text=' 進度 ')
area_status.grid(column=0, row=2, padx=8, pady=4, sticky=tk.W)

ttk.Label(area_status, text="狀態 :").grid(column=0, row=0, sticky=tk.W)
status_line_l=ttk.Label(area_status, text='idle')
status_line_l.grid(column=1, row=0, sticky=tk.W)
ttk.Label(area_status, text="進度 :").grid(column=0, row=1, sticky=tk.W)
progress_b = ttk.Progressbar(area_status, orient='horizontal', length=300, mode='determinate')
progress_b.grid(column=1, row=1)

#######################################
# main menu part
#######################################
# Exit GUI cleanly
def _quit():
    win.quit()
    win.destroy()
    exit() 
    
# Creating a Menu Bar
menu_bar = Menu(win)
win.config(menu=menu_bar)

# Add menu items
file_menu = Menu(menu_bar, tearoff=0)
#file_menu.add_command(label="New")
#file_menu.add_separator()
file_menu.add_command(label="Exit", command=_quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Display a Message Box
def _msgBox():
    msg.showinfo('Vocal Channel determination', 'This program will determine the vocal channel\nof the audio file')  

def help_Box():
    msg.showinfo('使用說明',\
                 '   +----------+\n'+\
                 '     環境設定 \n'+\
                 '   +----------+\n'+\
                 '[來源目錄]: 指定待處理影片所在目錄\n'+\
                 '[暫存檔目錄]: 指定處理影片時,暫存檔使用的目錄\n'+\
                 '              若指定於 ramdisk, 至少要有 500MB 可使用空間\n\n'+\
                 '   +--------------+\n'+\
                 '     人聲字串指定  \n'+\
                 '   +--------------+\n'+\
                 '  針對單音軌(左右聲道)與多重音軌(第一第二音軌)\n'+\
                 '  偵測出人聲的聲道後,加入檔名的字串定義\n'+\
                 '  通常單音軌左聲道為人聲, 使用字串 _vL, 多重音軌第一軌人聲, 使用 _VL\n'+\
                 '  若有特殊原因需要更改定義, 再自行勾選不同字串\n\n'+\
                 '   +----------+\n'+\
                 '     輸出設定 \n'+\
                 '   +----------+\n'+\
                 '[不處理已有_vL_vR檔案]: 若檔名已經有 _vL 或 _vR 的識別字串\n'+\
                 '                        就不再處理這檔案\n'+\
                 '[判斷的結果直接修改檔名]:若選擇此選項,處理後的結果會將_vL _vR 字串\n'+\
                 '                        直接更新到檔案.\n'+\
                 '[判斷結果改輸出到BAT檔案]:若上方選項不選,則可以指定一個 .bat 檔案當輸出\n')
                 
# Add another Menu to the Menu Bar and an item
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Help", command=help_Box)
help_menu.add_command(label="About", command=_msgBox)   # display messagebox when clicked
menu_bar.add_cascade(label="Help", menu=help_menu)

#======================
# Start GUI
#======================

win.mainloop()