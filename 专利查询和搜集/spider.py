from tkinter import *
from tkinter import messagebox
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
from shutil import copyfile
import threading
import webbrowser
import aiomultiprocess
key_words,done_words=[],[]
SURL_2,SURL = "",""
time_sacle = ""

def spider():
    global key_words,done_words
    if len(key_words)==0:
        messagebox.showinfo("提示","关键词为空")
    else:
        showinfo("[ run ]---开始爬取数据")
        showinfo("[ tip ]---这一步需要的时间，和爬取的时间间隔和爬取的内容数量有关，请耐心等待。")
        for_key_words = [key for key in key_words if key not in done_words]
        key_urls = {}
        if not os.path.exists("原始数据"):
            os.mkdir("原始数据")
        if len(key_words)==0:
            messagebox.showinfo("提示","关键词为空")
        for key_word in for_key_words:
            if "&" in key_word:
                term_1 = key_word.split("&")[0]
                term_2 = key_word.split("&")[1]
                key_words_url = SURL_2
                key_words_url = key_words_url.replace("search_change",str(term_1))
                key_words_url = key_words_url.replace("term2_change",str(term_2))
                url_1 = key_words_url
                url_1 = url_1.replace("page_change","1")
                key_urls[key_word]=url_1
            else:
                key_words_url = SURL
                key_words_url = key_words_url.replace("search_change",str(key_word))
                url_1 = key_words_url
                url_1 = url_1.replace("page_change","1")
                key_urls[key_word]=url_1
        url_lst_failed = []
        url_lst_successed = []
        global time_sacle
        async def get_page(session,key):
            async with session.get(key_urls[key], timeout=300) as resp:
                if resp.status != 200:
                    url_lst_failed.append(key_urls[key])
                else:
                    url_lst_successed.append(key_urls[key])
                return await resp.text(),key
        async def parser(html,key):
            page_a = []
            page_img = []
            page_href = []
            soup = BeautifulSoup(html, 'html.parser')
            try:
                total_len = soup.find("body").find_all("i")[1].find_all("strong")[2].get_text()
            except:
                total_len = 0
            if total_len == 0:
                showinfo(key+"---没有找到匹配专利")
                done_words.append(key)
            else:
                page_num = int(float(total_len)/50.5)+2
                showinfo(key+"一共"+str(total_len)+"个专利，共"+str(page_num-1)+"页")
                urls = []
                if page_num >= 2:
                    for i in range(2,page_num):
                        key_words_url = SURL
                        key_words_url = key_words_url.replace("search_change",str(key))
                        url_i = key_words_url
                        url_i = url_i.replace("page_change",str(i))
                        urls.append(url_i)
                soup_tb = soup.find_all("table")
                for tb in soup_tb:
                    for tr in tb.find_all("tr"):
                        valign_top = list(tr.find_all("td",attrs={"valign":"top"}))
                        if len(valign_top)>=2:
                            num = valign_top[1].get_text().replace(",","")
                            img = "https://pdfpiw.uspto.gov/.piw?Docid="+str(num)
                            top = valign_top[2]
                            href = "http://patft.uspto.gov/"+str(top.a.get("href"))
                            a = top.get_text()
                            a = a.replace("\n"," ")
                            page_a.append(a)
                            page_img.append(img)
                            page_href.append(href)
                page_dict = {"标题":page_a,"专利链接":page_href,"图片链接":page_img}
                page_df = pd.DataFrame(page_dict)
                page_df.to_csv("./原始数据/"+key+".csv",index=None,header=False)
                showinfo("导出"+key+"第一页")
                return urls
        async def get_page_s(session,key,url):
            async with session.get(url, timeout=60) as resp:
                if resp.status != 200:
                    url_lst_failed.append(url)
                else:
                    url_lst_successed.append(url)
                return await resp.text(),key
        async def parser_s(html,key):
            page_a = []
            page_img = []
            page_href = []
            soup = BeautifulSoup(html, 'html.parser')
            soup_tb = soup.find_all("table")
            for tb in soup_tb:
                for tr in tb.find_all("tr"):
                    valign_top = list(tr.find_all("td",attrs={"valign":"top"}))
                    if len(valign_top)>=2:
                        num = valign_top[1].get_text().replace(",","")
                        img = "https://pdfpiw.uspto.gov/.piw?Docid="+str(num)
                        top = valign_top[2]
                        href = "http://patft.uspto.gov/"+str(top.a.get("href"))
                        a = top.get_text()
                        a = a.replace("\n"," ")
                        page_a.append(a)
                        page_img.append(img)
                        page_href.append(href)
            page_dict = {"标题":page_a,"专利链接":page_href,"图片链接":page_img}
            page_df = pd.DataFrame(page_dict)
            page_df.to_csv("./原始数据/"+key+".csv",index=None,mode='a',header=False)
            showinfo(key+" +1")
        async def download_s(kurl):
            key,url = kurl
            async with aiohttp.ClientSession() as session:
                html,key = await get_page_s(session,key,url)
                await parser_s(html,key)
                await asyncio.sleep(int(time_sacle))
        async def download(key):
            async with aiohttp.ClientSession() as session:
                html,key = await get_page(session,key)
                urls = await parser(html,key)
                urls = [[key,i] for i in urls]
                async with aiomultiprocess.Pool() as pool:
                    await pool.map(download_s,urls)
                await asyncio.sleep(int(time_sacle))
        
        start = time.time()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [asyncio.ensure_future(download(key)) for key in key_urls]
        if len(tasks) != 0:
            loop.run_until_complete(asyncio.wait(tasks))
            showinfo("[ tip ]---所有第一页已经爬取完成")
        showinfo("#"*40)
        end = time.time()
        showinfo('总共耗时{}秒'.format(end-start))
        showinfo("[ ok ]---全部导出完毕，保存在“原始数据”文件夹中")

