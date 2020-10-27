import numpy as np
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
import pandas as pd
import os
import re
import emoji
from itertools import chain
import threading
import time
from bt import BaiduTrans
paths = ""

stopwords_list = ['i',
 'me',
 'my',
 'myself',
 'we',
 'our',
 'ours',
 'ourselves',
 'you',
 "you're",
 "you've",
 "you'll",
 "you'd",
 'your',
 'yours',
 'yourself',
 'yourselves',
 'he',
 'him',
 'his',
 'himself',
 'she',
 "she's",
 'her',
 'hers',
 'herself',
 'it',
 "it's",
 'its',
 'itself',
 'they',
 'them',
 'their',
 'theirs',
 'themselves',
 'what',
 'which',
 'who',
 'whom',
 'this',
 'that',
 "that'll",
 'these',
 'those',
 'am',
 'is',
 'are',
 'was',
 'were',
 'be',
 'been',
 'being',
 'have',
 'has',
 'had',
 'having',
 'do',
 'does',
 'did',
 'doing',
 'a',
 'an',
 'the',
 'and',
 'but',
 'if',
 'or',
 'because',
 'as',
 'until',
 'while',
 'of',
 'at',
 'by',
 'for',
 'with',
 'about',
 'against',
 'between',
 'into',
 'through',
 'during',
 'before',
 'after',
 'above',
 'below',
 'to',
 'from',
 'up',
 'down',
 'in',
 'out',
 'on',
 'off',
 'over',
 'under',
 'again',
 'further',
 'then',
 'once',
 'here',
 'there',
 'when',
 'where',
 'why',
 'how',
 'all',
 'any',
 'both',
 'each',
 'few',
 'more',
 'most',
 'other',
 'some',
 'such',
 'no',
 'nor',
 'not',
 'only',
 'own',
 'same',
 'so',
 'than',
 'too',
 'very',
 's',
 't',
 'can',
 'will',
 'just',
 'don',
 "don't",
 'should',
 "should've",'now','d','ll','m','o','re','ve','y','ain','aren',"aren't",'couldn',"couldn't",'didn',"didn't",'doesn',"doesn't",'hadn',"hadn't",'hasn',"hasn't",'haven',"haven't",'isn',"isn't",'ma','mightn',"mightn't",'mustn',"mustn't",'needn',"needn't",'shan',"shan't",'shouldn',"shouldn't",'wasn',"wasn't",'weren',"weren't",'won',"won't",'wouldn',"wouldn't"]

def pad_sequence(sequence,n):
    sequence = iter(sequence)
    return sequence

def ngrams(sequence,n):
    sequence = pad_sequence(sequence,n)
    history = []
    while n>1:
        try:
            next_item = next(sequence)
        except StopIteration:
            return
        history.append(next_item)
        n-=1
    for item in sequence:
        history.append(item)
        yield tuple(history)
        del history[0]
def select_dir():
    global paths
    dir_ = askdirectory()
    paths = dir_
    if dir_ !="":
        print(dir_)
        messagebox.showinfo('已选择',dir_)


def output_excel():
    global paths
    if paths is "":
        messagebox.showinfo("提示","未选择文件夹!!!")
    else:
        global CheckVar2
        show_hide_canvas("show")
        fill_line = canvas.create_rectangle(1.5,1.5,0,23,width=0,fill="green")
        if CheckVar2.get():
            messagebox.showinfo('开始处理','已经在后台运行！请耐心等待，处理好会有“提示”的。不要随便关闭，点击确定后开始!!!! 【翻译评论】')
        else:
            messagebox.showinfo('开始处理','已经在后台运行！请耐心等待，处理好会有“提示”的。不要随便关闭，点击确定后开始！')
        def get_one_two_three(selects):
            thgrams_selects = {}
            bigrams_selects = {}
            selects_token ={}
            for select in selects:
                pat = '[a-zA-Z]+'
                tokens = re.findall(pat,select)
                tokens = [i for i in tokens if(i.lower() not in stopwords_list)]
                bigrams_t = ngrams(tokens, 2) 
                thgrams_t = ngrams(tokens, 3)
                tokens = list(set(tokens))
                bigrams_t = list(set(bigrams_t))
                thgrams_t = list(set(thgrams_t))
                for t in thgrams_t:
                    t = str(t).split("'")
                    t = t[1] +" "+ t[3]+" "+t[5]
                    if t not in thgrams_selects:
                        thgrams_selects[t] = 1
                    else:
                        thgrams_selects[t] += 1
                for b in bigrams_t:
                    b = str(b).split("'")
                    b = b[1]+" "+b[3]
                    if b not in bigrams_selects:
                        bigrams_selects[b] = 1
                    else:
                        bigrams_selects[b] += 1
                for token in tokens:
                    if token not in selects_token:
                        selects_token[token] = 1
                    else:
                        selects_token[token] += 1
            df_selects_token = pd.DataFrame.from_dict(selects_token,orient="index",columns=["频率"]).sort_values(by="频率",ascending=False)
            df_selects_token = df_selects_token[df_selects_token["频率"]>=3]
            df_bigrams_selects = pd.DataFrame.from_dict(bigrams_selects,orient="index",columns=["频率"]).sort_values(by="频率",ascending=False)
            df_bigrams_selects = df_bigrams_selects[df_bigrams_selects["频率"]>=2]
            df_thgrams_selects = pd.DataFrame.from_dict(thgrams_selects,orient="index",columns=["频率"]).sort_values(by="频率",ascending=False)
            df_thgrams_selects = df_thgrams_selects[df_thgrams_selects["频率"]>=2]
            return df_selects_token,df_bigrams_selects,df_thgrams_selects
        def get_df_out(titles,comments):
            df_titles_token,df_bigrams_titles,df_thgrams_titles = get_one_two_three(titles)
            df_comments_token,df_bigrams_comments,df_thgrams_comments = get_one_two_three(comments)
            df_titles_token['标题-1字']=df_titles_token.index
            df_titles_token = df_titles_token.reset_index(drop=True)
            df_bigrams_titles['标题-2字']=df_bigrams_titles.index
            df_bigrams_titles = df_bigrams_titles.reset_index(drop=True)
            df_thgrams_titles['标题-3字']=df_thgrams_titles.index
            df_thgrams_titles = df_thgrams_titles.reset_index(drop=True)
            df_comments_token['评论-1字']=df_comments_token.index
            df_comments_token = df_comments_token.reset_index(drop=True)
            df_bigrams_comments['评论-2字']=df_bigrams_comments.index
            df_bigrams_comments = df_bigrams_comments.reset_index(drop=True)
            df_thgrams_comments['评论-3字']=df_thgrams_comments.index
            df_thgrams_comments = df_thgrams_comments.reset_index(drop=True)
            if df_titles_token.empty:
                df_t = pd.DataFrame()
            elif df_bigrams_titles.empty:
                df_t = df_titles_token
            elif df_thgrams_titles.empty:
                df_t = pd.concat([df_titles_token,df_bigrams_titles],axis=1)
            else:
                df_t = pd.concat([df_titles_token,df_bigrams_titles,df_thgrams_titles],axis=1)
            if df_thgrams_comments.empty:
                df_c = pd.concat([df_comments_token,df_bigrams_comments],axis=1)
            else:
                df_c = pd.concat([df_comments_token,df_bigrams_comments,df_thgrams_comments],axis=1)
            df_out = pd.concat([df_t,df_c],axis=1)
            return df_out
        def change_coloum_pro(df):
            df[df.columns[1::2].tolist()],df[df.columns[0::2].tolist()]=df[df.columns[0::2].tolist()],df[df.columns[1::2].tolist()]
            sss = list(df.columns)
            sss[1::2],sss[0::2] = sss[0::2],sss[1::2]
            df.columns = sss
            return df
        def change_coloum(df):
            df.columns = [x+"-"+str(i) if x=="频率" else x for i,x in enumerate(df.columns)]
            a,b,c = [],[],[]
            for i,j in enumerate(list(df.columns)):
                if i%2==0:
                    a.append(j)
                else:
                    b.append(j)
            for i in range(int(len(list(df.columns))/2)):
                c.append(b[i])
                c.append(a[i])
            df = df[c]
            return df
        df_tmp = pd.DataFrame()
        files= os.listdir(paths)
        
        outfile = paths+"/处理结果/"
        if not os.path.exists(outfile):
            os.mkdir(outfile)
        writer = pd.ExcelWriter(outfile+"最终结果.xlsx")
        all_titles = []
        all_comments = []
        files = [file for file in files if "xlsx" in file]
        print(files)
        total_len = len(files)*4
        n = 0
        raise_data = 150/total_len
        for file in files:
            keyname = file.split("-")[0]
            path = paths+"/"+file
            df = pd.read_excel(path)
            df = df[["标题","内容"]]
            titles = []
            comments = []
            df.标题.apply(lambda x:titles.append(x))
            df.内容.apply(lambda x:comments.append(x))
            titles = [emoji.demojize(str(i)).lower() for i in titles]
            comments = [emoji.demojize(str(i)).lower() for i in comments]
            all_titles.append(titles)
            all_comments.append(comments)
            df_out = get_df_out(titles,comments)
            df_out = change_coloum(df_out)
            df_out.to_excel(writer,sheet_name=keyname+"-"+str(len(df)),index=None)
            n += raise_data
            canvas.coords(fill_line,(0,0,n,60))
            root.update()
        df_out = get_df_out(list(chain.from_iterable(all_titles)),list(chain.from_iterable(all_comments)))
        df_out = change_coloum(df_out)
        df_out.to_excel(outfile+"所有标题和评论词频汇总.xlsx",sheet_name="所有标题和评论词频汇总",index=None)
        #     print(df_out.columns)
        writer.close()
        test = pd.read_excel(outfile+"最终结果.xlsx",None)
        writer = pd.ExcelWriter(outfile+"最终结果(前一百).xlsx")
        for key in test.keys():
            pd_out = test[key]
            pd_out = pd_out.head(100)
            pd_out.to_excel(writer,sheet_name=key,index=None)
            n += raise_data
            canvas.coords(fill_line,(0,0,n,60))
            root.update()
        writer.close()
        df_good = pd.DataFrame()
        df_bad = pd.DataFrame()
        df_none = pd.DataFrame()
        for file in files:
            keyname = file.split("-")[0]
            path = paths+"/"+file
            df = pd.read_excel(path)
            df = df[["标题","内容","星级"]]
            df.loc[df["星级"].isnull(),"星级"] = 0
            df_good = pd.concat([df_good,df[df["星级"]>=4]])
            df_bad = pd.concat([df_bad,df[df["星级"].isin([1,2,3])]])
            df_none = pd.concat([df_none,df[df["星级"]==0]])
            n += raise_data
            canvas.coords(fill_line,(0,0,n,60))
            root.update()
        good_titles = [emoji.demojize(str(i)).lower() for i in df_good["标题"].to_list()]
        good_comments = [emoji.demojize(str(i)).lower() for i in df_good["内容"].to_list()]
        bad_titles = [emoji.demojize(str(i)).lower() for i in df_bad["标题"].to_list()]
        bad_comments = [emoji.demojize(str(i)).lower() for i in df_bad["内容"].to_list()]
        none_titles = [emoji.demojize(str(i)).lower() for i in df_none["标题"].to_list()]
        none_comments = [emoji.demojize(str(i)).lower() for i in df_none["内容"].to_list()]
        writer = pd.ExcelWriter(outfile+"标题-评论-星级汇总.xlsx")
        good_df_out = get_df_out(good_titles,good_comments)
        good_df_out.columns = [x+"-"+str(i) if x=="频率" else x for i,x in enumerate(good_df_out.columns)]
        good_df_out = change_coloum_pro(good_df_out)
        good_df_out.to_excel(writer,sheet_name="好评-"+str(len(good_df_out)),index=None)
        bad_df_out = get_df_out(bad_titles,bad_comments)
        bad_df_out.columns = [x+"-"+str(i) if x=="频率" else x for i,x in enumerate(bad_df_out.columns)]
        bad_df_out = change_coloum_pro(bad_df_out)
        bad_df_out.to_excel(writer,sheet_name="差评-"+str(len(bad_df_out)),index=None)
        none_df_out = get_df_out(none_titles,none_comments)
        if len(none_df_out)!=0:
            none_df_out.columns = [x+"-"+str(i) if x=="频率" else x for i,x in enumerate(none_df_out.columns)]
            none_df_out = change_coloum_pro(none_df_out)
            none_df_out.to_excel(writer,sheet_name="未评价-"+str(len(none_df_out)),index=None)
            good_bad_none_all = pd.concat([good_df_out,bad_df_out,none_df_out])
        else:
            good_bad_none_all = pd.concat([good_df_out,bad_df_out])
        df_tmp1 = good_bad_none_all[["频率-0","标题-1字"]].groupby("标题-1字").sum().sort_values(by="频率-0",ascending=False).reset_index()
        df_tmp2 = good_bad_none_all[["频率-2","标题-2字"]].groupby("标题-2字").sum().sort_values(by="频率-2",ascending=False).reset_index()
        df_tmp3 = good_bad_none_all[["频率-4","标题-3字"]].groupby("标题-3字").sum().sort_values(by="频率-4",ascending=False).reset_index()
        df_tmp4 = good_bad_none_all[["频率-6","评论-1字"]].groupby("评论-1字").sum().sort_values(by="频率-6",ascending=False).reset_index()
        df_tmp5 = good_bad_none_all[["频率-8","评论-2字"]].groupby("评论-2字").sum().sort_values(by="频率-8",ascending=False).reset_index()
        df_tmp6 = good_bad_none_all[["频率-10","评论-3字"]].groupby("评论-3字").sum().sort_values(by="频率-10",ascending=False).reset_index()
        df_all_temp = pd.concat([df_tmp1,df_tmp2,df_tmp3,df_tmp4,df_tmp5,df_tmp6],axis=1)
        df_all_temp.to_excel(writer,sheet_name="汇总-"+str(len(good_bad_none_all)),index=None)
        df_all = pd.DataFrame()
        
        for file in files:
            keyname = file.split("-")[0]
            path = paths+"/"+file
            df = pd.read_excel(path)
            df = df[["标题","内容","星级"]]
            if CheckVar2:
                df["内容翻译"] = df["内容"].apply(lambda x:BaiduTrans().get(x))
            df_all = pd.concat([df_all,df])
            n += raise_data
            canvas.coords(fill_line,(0,0,n,60))
            root.update()
        df_all.sort_values(by="星级",ascending=False,inplace=True)
        df_all.to_excel(writer,sheet_name="标题-评论-星级汇总-"+str(len(df_all)),index=None)
        writer.close()
        messagebox.showinfo('成功','已导出在->处理结果<-文件夹中')

def open_dir():
    os.system("start "+paths+"/处理结果")
root = Tk()
root.geometry('200x200')
root.title("关键词")
CheckVar2 = IntVar()


class MyThread(threading.Thread):
    def __init__(self,func,*args):
        super().__init__()
        self.func = func
        self.args = args
        self.setDaemon(True)
        self.start()
    def run(self):
        self.func(*self.args)

select_dir_button = Button(root,text="选择文件夹",command=lambda :MyThread(select_dir,),width="20").pack()
output_excel_button = Button(root,text="导出excel",command=lambda :MyThread(output_excel,),width="20").pack()
canvas = Canvas(root,width="150",height="20",bg="white")
def show_hide_canvas(str):
    if str == "show":
        canvas.pack()
canvas.pack_forget()

C1 = Checkbutton(root, text = "翻译评论", variable = CheckVar2, onvalue = 1, offvalue = 0, width = 20).pack()
open_dir_button = Button(root,text="打开所在文件夹",command=lambda :MyThread(open_dir,),width="20").pack()
root.mainloop()
























