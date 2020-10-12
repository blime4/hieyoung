from tkinter import *
import os
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from contextlib import closing
import threading
# from pdf2image import convert_from_path
from PIL import Image, ImageEnhance,ImageTk
from tkinter.ttk import Treeview
import xlsxwriter
import xlrd
import aiohttp
import asyncio
import nest_asyncio
nest_asyncio.apply()
import fitz

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
}
df = pd.read_excel("cleaned/df_all.xlsx")
def down_search(df):
    pdf_dir = "tmp/pdf/"
    png_dir = "tmp/png/"
    png_time = "tmp/png_time/"
    png_get = "tmp/png_get/"
    thread_num = 50
    timeout = 30
    len_to_download = 0
    failurls = []
    print("[ run ]---正在进行pdf下载")
    print("[ tip ]---这一步需要很长时间，请耐心等待。")
    def download(img_url,img_name):
        img_name = img_name +".pdf"
        if os.path.isfile(os.path.join(pdf_dir,img_name)):
            return
        with closing(requests.get(img_url,stream=True,headers=headers,timeout=timeout)) as r:
            rc = r.status_code
            if 299 < rc or rc < 200:
                print ('returnCode%s\t%s' % (rc, img_url))
                return
            content_length = int(r.headers.get('content-length', '0'))
            if content_length == 0:
                print ('size0\t%s' % img_url)
                return
            try:
                with open(os.path.join(pdf_dir,img_name),"wb") as f:
                    for data in r.iter_content(8192):
                        f.write(data)
            except:
                print('savefail\t%s' % img_url)
    lock = threading.Lock()
    def loop(imgs):
        while True:
            try:
                with lock:
                    img_url,img_name = next(imgs)
    #                 print(img_name)
            except StopIteration:
                break
            try:
                download(img_url,img_name)
            except:
                global failurls
                failurls.append((img_url,img_name))
                print("exceptfail\t%s"%img_url)
    def get_img_url_generate(df):
        imgs = []
        global len_to_download
        len_to_download = len(df)
        df = df[["pdf下载链接","专利号"]]
        for i,j in zip(df.pdf下载链接,df.专利号):
            imgs = []
            img_url = i
            img_name = j
            imgs.append(img_url)
            imgs.append(img_name)
            try:
                if img_url:
                    yield imgs
            except:
                break
    def tryagain_fail(fail_urls):
        global failurls
        failurls = []
        for img_url, img_name in fail_urls:
            img_name = img_name +".pdf"
            if os.path.isfile(os.path.join(pdf_dir,img_name)):
                return
            r = requests.get(img_url,stream=True,headers=headers,timeout=timeout)
            rc = r.status_code
            if 299 < rc or rc < 200:
                print ('returnCode%s\t%s' % (rc, img_url))
                return
            content_length = int(r.headers.get('content-length', '0'))
            if content_length == 0:
                print ('size0\t%s' % img_url)
                return
            try:
                with open(os.path.join(pdf_dir,img_name),"wb") as f:
                    for data in r.iter_content(8192):
                        f.write(data)
            except:
                print('savefail\t%s' % img_url)
                failurls.append((img_url,img_name))
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    tsk = []
    imgs = get_img_url_generate(df)
    for i in range(0,thread_num):
        t = threading.Thread(target=loop,name="LoopThread %s" %i,args=(imgs,))
        t.start()
        tsk.append(t)
    for tt in tsk:
        tt.join()
    print("[ run ]---pdf下载完成，正在检查是否有下载失败的内容")
    if len(failurls) != 0:
        print("[ warning ]---有"+str(len(failurls))+"个下载失败，现在尝试重下")
        flag = 0
        while True:
            if len(failurls)==0:
                print("[ ok ]---全部重下完成")
                break
            if len(os.listdir(pdf_dir)) == len_to_download:
                print("[ ok ]---全部重下完成")
                break
            if flag >= 5:
                print("[ error ]---以下链接多次下载仍然失败")
                print(" 可尝试手动下载，放在image文件夹中")
                for i,j in failurls:
                    print(i+j)
                break
            tryagain_fail(failurls)
            flag += 1
    print("[ run ]---开始pdf转png")
    if not os.path.exists(png_dir):
        os.makedirs(png_dir)
    for j,i in enumerate(os.listdir(pdf_dir)):
        name = i.split(".")[0] + ".png"
        if os.path.isfile(os.path.join(png_dir,name)):
            continue
        try:
            image = fitz.open(os.path.join(pdf_dir,i))
            page = image[0]
            rotate = int(0)
            zoom_x = 1.0
            zoom_y = 1.0
            trans = fitz.Matrix(zoom_x,zoom_y).preRotate(rotate)
            pm = page.getPixmap(matrix=trans,alpha=False)
            pm.writePNG(os.path.join(png_dir,name))
            if j % 50 == 0:
                print("完成了"+str(j)+"个")
        except:
            print("出错 --"+name)

    files = os.listdir(png_dir)
    print("[ run ]---开始图片切割")
    for j,i in enumerate(files):
        img = Image.open(png_dir+i)
        w,h = img.size
        img_get = img.crop((0,int(h/2),w,h))
        tmp = img.crop((3*w/5,0,w,h/7))
        if not os.path.exists(png_time):
            os.makedirs(png_time)
        if not os.path.exists(png_get):
            os.makedirs(png_get)
        tmp.save(png_time+i)
        img_get.save(png_get+i)
        if j%50 == 0:
            print("完成了"+str(j)+"个")
    print("[ ok ]---pdf转png成功，保存在png_get,png_time文件夹中")        


down_search(df)