import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from pandas.testing import assert_frame_equal

urls = ["https://www.amazon.com/Best-Sellers-Toys-Games-Kids-Lunch-Bags/zgbs/toys-and-games/6498205011/ref=zg_bs_pg_1?_encoding=UTF8&pg=1","https://www.amazon.com/Best-Sellers-Toys-Games-Kids-Lunch-Bags/zgbs/toys-and-games/6498205011/ref=zg_bs_pg_2?_encoding=UTF8&pg=2"]
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}

item_info = []

def get_item_info(urls):
    for u in urls:
        html = requests.get(u, headers=headers)
        soup = BeautifulSoup(html.text,"lxml")
        for i in range(50):
            data = {
                'Rank': soup.select('span.zg-badge-text')[i].text.strip('#'),
                'item_name' : soup.select('#zg-ordered-list > li > span > div > span > a > div')[i].text.strip(),
                'item_link' : 'https://www.amazon.com' + soup.select('#zg-ordered-list > li > span > div > span > a')[i].get('href'),
                # 'img_src' :soup.select('#zg-ordered-list > li> span > div > span > a > span > div > img')[i].get('src')
            }
            item_info.append(data)
    df = pd.DataFrame(item_info)
    df.to_excel("./缓存/"+time.strftime("%Y-%m-%d-%H-%M-%S")+".xlsx",index=None)
    print("finsh!")
    return df

def deal_df(df,df_new):
    try:
        assert_frame_equal(df, df_new)
        print("一样")
    except:
        print("不一样")
        df_list = list(df["item_name"])
        df_new_list = list(df_new["item_name"])

        out_rank = [i for i in df_list if i not in df_new_list]
        in_rank = [i for i in df_new_list if i not in df_list]
        pd.concat([pd.DataFrame(in_rank,columns=["进榜"]),pd.DataFrame(out_rank,columns=["出榜"])], axis=1).to_excel("分析.xlsx",index=None)

        print("出榜了"+str(len(out_rank))+"个")
        print("进榜了"+str(len(in_rank))+"个")

def run():
    if not os.path.exists("./缓存"):
        os.mkdir("./缓存")
    df = pd.DataFrame()
    if len(os.listdir("./缓存"))!= 0:
        df = pd.read_excel("./缓存/"+os.listdir("./缓存")[-1])
    df_new = get_item_info(urls)
    if len(df)==0:
        print("初始化")
        df_new = get_item_info(urls)
    else:
        deal_df(df,df_new)
