#-*- coding: utf-8 -*-

# Author:       Fatih Mert DOĞANCAN
# Github:       fatihmert
# Name:         Youtube MP3 Downloader
# API:          http://youtubeinmp3.com/api/

from bs4 import BeautifulSoup
import requests, re, os, urllib, sys

sys.setrecursionlimit(10000)

API = "http://YouTubeInMP3.com/fetch/?video="

#STAT
#0 = HATA
#10 = Tek video
#20 = Playlist

P_YT_ID = ".*youtube.*\?v=(.*)&?"
P_IDX_PATH = "\+(.*)"
EXT = "pytmp3"

pwd = os.getcwd()



ornek_link = "http://www.youtube.com/watch?v=3x2ABSAMVno"

def get_isim(ornek_link):
    if re.search("youtube",ornek_link):
        ryt = requests.get(ornek_link)
        dom = BeautifulSoup(ryt.text)
        dom.prettify()
        return dom.find('span','watch-title',id='eow-title')['title']

def get_id(ornek_link):
    if re.search(P_YT_ID,ornek_link):
        return re.search(P_YT_ID,ornek_link).group(1)

def get_stat(ornek_link):
    if re.search("list",ornek_link):
        if re.search("list",ornek_link) != None:
            return 20
    elif re.search(P_YT_ID,ornek_link):
        if re.search(P_YT_ID,ornek_link).group(1) != None:
            return 10
    else:
        return 0

def del_gereksiz(strg):
    gereksiz = ["lyrics","lyric","video","official","music","+","hd","hq","uhq","uhd",
    "ultra hd","ultra hq",u"şarkı sözü","\"","!","(",")","[","]"]
    for i in gereksiz:
        strg = strg.replace(i,"")
        strg = strg.replace(i.upper(),"")
        strg = strg.replace(i.lower(),"")
        strg = strg.replace(i.title(),"")
    #OLMASADA OLUR
    strg = strg.replace('feat.','ft.')
    return strg


def download_mp3(link,cur_path,dosya_adi=0,rapor=1):
    """
    dosya_adi = 0
        Video'nun adinda kaydet.
    dosya_adi = 1
        Video'nun id'si adinda kaydet.
    """
    fname = ""
    if cur_path[2:] == "":
        fname = "%s.mp3"%(del_gereksiz(get_isim(link)))
    else:
        fname = "%s/%s.mp3"%(cur_path[2:],del_gereksiz(get_isim(link)))
    if re.search("youtube",link):
        binary = None
        #stt = "" #geliştirici için
        rq = requests.get("%s%s"%(API,link))
        if re.search("fetch",rq.url):
            binary = rq.content
            #stt = "request"  #geliştirici için
        else:
            rq = urllib.urlopen("%s%s"%(API,link))
            #stt = "urllib"  #geliştirici için
            binary = rq.read()
        with open(fname,"wb") as mp3:
            mp3.write(binary)
        if rapor != 0:
            print del_gereksiz(get_isim(link)) + " KAYDEDILDI!" #%s"%stt

def is_dir(dirAdi):
    if os.path.isdir(dirAdi):
        return True
    else:
        return False


print get_isim(ornek_link)
print get_id(ornek_link)
print get_stat(ornek_link)
#playlist-video clearfix  spf-link
playlist_test = "http://www.youtube.com/watch?v=3x2ABSAMVno&list=RD3x2ABSAMVno"

def get_playlist(playlist_test):
    playlist = []
    if get_stat(playlist_test) == 20:
        rq = requests.get(playlist_test)
        dom = BeautifulSoup(rq.text)
        dom.prettify()
        for video in dom.find_all('a','playlist-video',href=True):
            if re.search("watch\?v=(.*)&li",video['href']):
                playlist.append("http://www.youtube.com/watch?v=%s"%re.search("watch\?v=(.*)&li",video['href']).group(1))
    playlist = set(playlist)
    playlist = list(playlist)
    return playlist

with open("index.pytmp3") as pytmp3:
    if pytmp3.readline() == "#-*- PYTMP3 -*-\n":
        cur_path = ""
        for satir in pytmp3.readlines()[0:]:
            if re.search(P_IDX_PATH,satir):
                cur_path = re.search(P_IDX_PATH,satir).group(1).decode('utf-8')
                #print re.search(P_IDX_PATH,satir).group()
                if is_dir(cur_path[2:]) == False and cur_path != "./":
                    os.mkdir(u"%s"%cur_path[2:])
            else:
                if get_stat(satir) == 10:
                    download_mp3(satir,cur_path)
                elif get_stat(satir) == 20:
                    for link in get_playlist(satir):
                        download_mp3(satir,cur_path)
                else:
                    print "BİLİNMEDİK LINK"


