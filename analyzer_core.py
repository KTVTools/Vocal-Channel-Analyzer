#
# analyzer_core.py
# This module provide the analysis core of the voice channel
# 
# version : 1.0.0  2020/09/15

import os
import subprocess
from math import log10

# put ffmpeg.exe, mediainfo.exe in the same directory for the
# program to find. Spleeter package must be installed properly too.

ffmpegcmd="ffmpeg.exe"
mediainfocmd="mediainfo.exe"
spleetercmd="python\python.exe -m spleeter separate "

def read_mediainfo(filename):
    cmdlist=mediainfocmd+' "'+filename+'"'
    try:
        result = subprocess.check_output(cmdlist, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return [0, "", ""]
    
    result=str(result).replace('\\n','\n').replace('\\r','\r')
    
    s_pos = str(result).find('\r\nVideo')
    n_pos = str(result).find('Format', s_pos)
    m_pos = str(result).find(':', n_pos)
    p_pos = str(result).find('\n', m_pos)
    try:
        vid_format = str(result)[m_pos+1:p_pos].strip()
    except:
        return[0, '', 0, '', 0]     # error condition
    
    if vid_format=='MPEG Video':
        n_pos = str(result).find('Format version', s_pos)
        m_pos = str(result).find(':', n_pos)
        p_pos = str(result).find('\n', m_pos)
        ver_format = str(result)[m_pos+1:p_pos].strip()
        if ver_format=='Version 1':
            mpeg_format=1   # MPEG1
        else:
            mpeg_format=2   # MPEG2
    else:
        mpeg_format=0    # not MPEG format

    s_pos = str(result).find('Scan type')
    n_pos = str(result).find(':', s_pos)
    m_pos = str(result).find('\n',n_pos+1)
    try:
        scan_type=str(result)[n_pos+1:m_pos].strip()
    except:
        return[0, '', 0, '', 0]     # error condition
    
    audio_no = str(result).count('\r\nAudio')
    
    s_pos = str(result).find('Audio', m_pos)
    n_pos = str(result).find('Format', s_pos)
    m_pos = str(result).find(':', n_pos)
    p_pos = str(result).find('\n', m_pos)
    try:
        audio_format=str(result)[m_pos+1:p_pos].strip()
    except:
        return[0, '', 0, '', 0]     # error condition
    
    s_pos = str(result).find('Channel', p_pos)
    n_pos = str(result).find(':', s_pos)
    m_pos = str(result).find('ch', n_pos)
    try:
        channel_no=int(str(result)[n_pos+1:m_pos-1].strip())
    except:
        return[0, '', 0, '', 0]    # error condition
    # return parameters :
    # scan_type : "Progressive" or "Interlaced"
    # audio_no : audio streams in the file
    # audio_format : "AC-3" "mp2" "mp3" or "PCM"
    # channel_no : audio channel number in audio stream
    return [mpeg_format, scan_type, audio_no, audio_format, channel_no]


def generate_audio_files(infile, audio_no, tmp_dir):
    if (audio_no==1):  # has only 1 audio
        cmdlist=ffmpegcmd+' -i "'+infile+\
            '" -filter_complex "[0:a]pan=stereo|c0=c0|c1=c0[out]" -map "[out]" -y "'+\
            tmp_dir+'/ch0.wav"'
        run_cmd(cmdlist, "error on generate ch0.wav :"+cmdlist)
        cmdlist=ffmpegcmd+' -i "'+infile+\
            '" -filter_complex "[0:a]pan=stereo|c0=c1|c1=c1[out]" -map "[out]" -y "'+\
            tmp_dir+'/ch1.wav"'
        run_cmd(cmdlist, "error on generate ch1.wav :"+cmdlist)
    else:
        cmdlist=ffmpegcmd+' -i "'+infile+\
            '" -filter_complex "[0:a:0]pan=stereo|c0=FL|c1=FR[out]" -map "[out]" -y "'+\
            tmp_dir+'/ch0.wav"'
        run_cmd(cmdlist, "error on generate ch0.wav :"+cmdlist)
        cmdlist=ffmpegcmd+' -i "'+infile+\
            '" -filter_complex "[0:a:1]pan=stereo|c0=FL|c1=FR[out]" -map "[out]" -y "'+\
            tmp_dir+'/ch1.wav"'
        run_cmd(cmdlist, "error on generate ch1.wav :"+cmdlist)

def run_cmd(cmdstr, errorstr):
    try:
        result = subprocess.check_output(cmdstr, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(errorstr)
        return False
    return True

# calculate vocal gain in tmp_dir/ch0.wav and ch1.wav
def calculate_vocal_gain(tmp_dir):
    # generate vocal files of channel by Spleeter
    cmdlist=spleetercmd+' -i "'+tmp_dir+'/ch0.wav"'+\
        ' -o "'+tmp_dir+'/output"'
    if run_cmd(cmdlist, 'error on L vocal:'+cmdlist)==False:
        return[0.0, 0.0]

    #  using ffmpeg to get replaygain of vocal files
    cmdlist=ffmpegcmd+' -i "'+tmp_dir+'/output/ch0/vocals.wav"'+\
        ' -af replaygain -f null nul'
    try:
        result = subprocess.check_output(cmdlist, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print("error on ch0 replaygain")
        remove_file(tmp_dir+'/output/ch0/accompaniment.wav')
        remove_file(tmp_dir+'/output/ch0/vocals.wav')
        return [0.0, 0.0]
    gain_str = str(result).find('track_gain')
    db_str = str(result).find('dB', gain_str)
    ch0_db = float(str(result)[gain_str+13:db_str-1])
    remove_file(tmp_dir+'/output/ch0/accompaniment.wav')
    remove_file(tmp_dir+'/output/ch0/vocals.wav')
    
    # process ch1
    cmdlist=spleetercmd+' -i "'+tmp_dir+'/ch1.wav"'+\
        ' -o "'+tmp_dir+'/output"'
    if run_cmd(cmdlist, 'error on R vocal:'+cmdlist)==False:
        return[0.0, 0.0]
    
    cmdlist=ffmpegcmd+' -i "'+tmp_dir+'/output/ch1/vocals.wav"'+\
        ' -af replaygain -f null nul'
    try:
        result = subprocess.check_output(cmdlist, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print("error on ch1 replaygain")
        remove_file(tmp_dir+'/output/ch1/accompaniment.wav')
        remove_file(tmp_dir+'/output/ch1/vocals.wav')
        return [0.0, 0.0]
    gain_str = str(result).find('track_gain')
    db_str = str(result).find('dB', gain_str)
    ch1_db = float(str(result)[gain_str+13:db_str-1])
    remove_file(tmp_dir+'/output/ch1/accompaniment.wav')
    remove_file(tmp_dir+'/output/ch1/vocals.wav')
    return [ch0_db, ch1_db]

def remove_tmp_dir_audiofiles(tmp_dir):
    remove_file(tmp_dir+'/ch0.wav')
    remove_file(tmp_dir+'/ch1.wav')
    
def rename_file(orgfile, newfile):
    tmplist='ren "'+orgfile+'" "'+newfile+'"'
    cmdlist=tmplist.replace('/','\\')
    run_cmd(cmdlist, "error on rename file:"+cmdlist)

def remove_file(infile):
    tmplist='del "'+infile+'"'
    cmdlist=tmplist.replace('/','\\')
    run_cmd(cmdlist, "error on remove file:"+cmdlist)

# analyze the vocal channel
# fullpath : the source file path
# tmpdir : directory for audio temp files during analysis
# vl_str : _VL_VR string 
# output : '' when error, _VL_VR string if analysis ok
def vocal_analyze(fullpath, tmpdir, vl_str):
#    fullpath=os.path.join(dirpath, fileitem)
#    filename, fileext = os.path.splitext(fileitem)
    [mpeg_format, interlace_str, audio_no, audio_format, audio_ch]=read_mediainfo(fullpath)
    if audio_no==0:
        print("no audio stream in ",fullpath)
        return ''
    generate_audio_files(fullpath, audio_no, tmpdir)
    [ch0_v_gn, ch1_v_gn] = calculate_vocal_gain(tmpdir)
    remove_tmp_dir_audiofiles(tmpdir)
    if (ch0_v_gn==0.0) or (ch1_v_gn==0.0):
        print("error on getting vocal replaygain", fullpath)
        return ''
    if (ch0_v_gn>ch1_v_gn):  # vl_str contains [VCD_VL, VCD_VR, DVD_VL, DVD_VR] string
        if (audio_no==1):  #  channel 1 voice is louder, _VR
            ch_str=vl_str[1]  # VCD_VR
        else:
            ch_str=vl_str[3]  # DVD_VR
    else:
        if (audio_no==1):  #  channel 0 voice is louder, _VL
            ch_str=vl_str[0]  # VCD_VL
        else:
            ch_str=vl_str[2]  # DVD_VL
    return ch_str
