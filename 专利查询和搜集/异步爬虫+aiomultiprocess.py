import aiohttp
import aiomultiprocess
import asyncio
import multiprocessing
import nest_asyncio
nest_asyncio.apply()
import pandas as pd
import os
from bs4 import BeautifulSoup
import time

class aiospider:
    def __init__(self,url1,url2,timesacle,keywords,donewords):
        self.url1 = url1
        self.url2 = url2
        self.timesacle = timesacle
        self.donewords = donewords
        self.keywords = [key for key in keywords if key not in self.donewords]
        if not os.path.exists("原始数据"):
            os.mkdir("原始数据")
        if len(self.keywords)==0:
            print("关键词为空")
        self.key_urls = {}
        for key in self.keywords:
            if "&" in key:
                term_1 = key.split("&")[0]
                term_2 = key.split("&")[1]
                tmp_url = SURL_2
                tmp_url = tmp_url.replace("search_change",str(term_1)).replace("term2_change",str(term_2)).replace("page_change","1")
                self.key_urls[key]=tmp_url
            else:
                tmp_url = SURL
                tmp_url = tmp_url.replace("search_change",str(key)).replace("page_change","1")
                self.key_urls[key]=tmp_url
    async def get_page(session,key_urls):
        
    async def deal_key_urls(self,key_urls):
        async with aiohttp.ClientSession() as session:
            html,key = await self.get_page(session,key_urls)
            await self.parser(html,key)
            await asyncio.sleep(int(time_sacle))
    async def deal_frist(self,key_urls):
        async with aiomultiprocess.Pool() as pool:
            results = await pool.map(self.deal_key_urls,key_urls)
            return results
    async def deal_frist_result(self,loop):
        result = loop.run_until_complete(self.deal_frist(self.key_urls))
        return result
    def run(self):
        multiprocessing.freeze_support()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        first = self.deal_frist_result(loop)


if __name__ == '__main__':
    time_sacle = "5"
    SURL = "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=page_change&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=search_change&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PTXT"
    SURL_2 = "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=page_change&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=search_change&FIELD1=&co1=AND&TERM2=term2_change&FIELD2=&d=PTXT"
    key_words,done_words = [],[]
    for_key_words = [key for key in key_words if key not in done_words]
    key_urls = {}
    if not os.path.exists("原始数据"):
        os.mkdir("原始数据")
    if len(key_words)==0:
        print("提示","关键词为空")
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
    pages_key_urls = {}
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
            print(key+"---没有找到匹配专利")
            done_words.append(key)
        else:
            page_num = int(float(total_len)/50.5)+2
            print(key+"一共"+str(total_len)+"个专利，共"+str(page_num-1)+"页")
            if page_num >= 2:
                for i in range(2,page_num):
                    key_words_url = SURL
                    key_words_url = key_words_url.replace("search_change",str(key))
                    url_i = key_words_url
                    url_i = url_i.replace("page_change",str(i))
                    if key not in pages_key_urls:
                        pages_key_urls[key] = [url_i]
                    else:
                        pages_key_urls[key].append(url_i)
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
            print("导出"+key+"第一页")
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
        print(key+" +1")
    async def download(key):
        async with aiohttp.ClientSession() as session:
            html,key = await get_page(session,key)
            await parser(html,key)
            await asyncio.sleep(int(time_sacle))
    async def download_s(key,url):
        async with aiohttp.ClientSession() as session:
            html,key = await get_page_s(session,key,url)
            await parser_s(html,key)
            await asyncio.sleep(int(time_sacle))

    multiprocessing.freeze_support()
    start = time.time()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [asyncio.ensure_future(download(key)) for key in key_urls]
    if len(tasks) != 0:
        loop.run_until_complete(asyncio.wait(tasks))
    print("[ tip ]---所有第一页已经爬取完成")
    tasks_s = []
    loop_s = asyncio.new_event_loop()
    asyncio.set_event_loop(loop_s)
    for key in pages_key_urls:
        for url in pages_key_urls[key]:
            tasks_s.append(asyncio.ensure_future(download_s(key,url)))
    if len(tasks_s) !=0:
        loop_s.run_until_complete(asyncio.wait(tasks_s))
    print("#"*40)
    end = time.time()
    print('总共耗时{}秒'.format(end-start))
    print("[ ok ]---全部导出完毕，保存在“原始数据”文件夹中")