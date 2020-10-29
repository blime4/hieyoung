from tkinter import *
from tkinter import messagebox
import os
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from contextlib import closing
import threading
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
import multiprocessing


class MyThread(threading.Thread):
    def __init__(self,func,*args):
        super().__init__()
        self.func = func
        self.args = args
        self.setDaemon(True)
        self.start()
    def run(self):
        self.func(*self.args)
if __name__ == "__main__":

    def showinfo(result):
        realtime = time.strftime("%H:%M:%S ")
        textvar = realtime + result #系统时间和传入结果
        out_frame_Text.insert(END,textvar) #显示在text框里面
        out_frame_Text.insert(INSERT,'\n') #换行
        out_frame_Text.update()
        out_frame_Text.see(END)

    def RightClickTip(click):
        if click == "关键词查询":
            showinfo("[ tip ]---TERM1：关键词1，TERM2：关键词2。可以只填关键词1，也可以填写两个做品牌关键词查询。")
        if click == "搜索关键词":
            showinfo("[ tip ]---搜索关键词，多级查询添加“ + ”即可。例如：pot+plant+hanger")
        if click == "排除无关词":
            showinfo("[ tip ]---排除“ 命中数据 ”中和本次调研无关的词。")
        if click == "新增命中词":
            showinfo("[ tip ]---添加与本次调研有关的词")
        if click == "爬取时间间隔":
            showinfo("[ tip ]---防止被反扒被封，设置的爬取间隔时间")
        if click == "开始爬取":
            showinfo("[ tip ]---开始爬取 关键词列表中所有关键词 并且会自动进行数据清洗。")
        if click == "深度数据整理":
            showinfo("[ tip ]---根据 “排除词”，“命中词”，“关键词“进行数据整理，生成命中数据.xlsx,未命中数据.xlsx")
        if click == "PDF下载和整理":
            showinfo("[ tip ]---下载命中数据.xlsx中所有的pdf，并且转换成PNG，得到需要的专利图片和授权时间")
        if click == "插入图片到excel":
            showinfo("[ tip ]---将下载好的图片插入到excel中，得到最终需要的xlsx")
        if click == "一键爬取清洗下载保存导出":
            showinfo("[ tip ]---一键完成 ”开始爬取“，”深度数据整理“，”PDF下载和整理“，”插入图片到excel“")
        if click == "显示所有数据":
            showinfo("[ tip ]---显示全部数据.xlsx")
        if click == "显示未命中数据":
            showinfo("[ tip ]---显示未命中数据.xlsx")
        if click == "显示命中数据":
            showinfo("[ tip ]---显示命中数据.xlsx")
        if click == "打开文件夹":
            showinfo("[ tip ]---打开工具所在文件夹，如果处理了数据，即会打开”已处理“文件夹")
        if click == "下载图片":
            showinfo("[ tip ]---下载表格中所有图片到缓存中。例如，点击了显示命中数据，再点下载图片，就是下载命中数据的图片。如果是显示点了”搜索一下“，再点下载图片，就是下载搜索命中的图片。")
    root = Tk()
    root.geometry('1100x650')
    root.title("专利查询和搜索")

    key_frame = Frame(width=425,height=250,bg="LightPink")
    sea_frame = Frame(width=225,height=250,bg="Yellow")
    bad_frame = Frame(width=225,height=250,bg="Thistle")
    hit_frame = Frame(width=225,height=250,bg="AntiqueWhite")
    fun_frame = Frame(width=200,height=400,bg="LightSeaGreen")
    out_frame = Frame(width=600,height=150,bg="green")
    png_frame = Frame(width=300,height=400)
    sho_frame = Frame(width=600,height=250)
    df_all = pd.DataFrame()
    df_rest = pd.DataFrame()
    df_hit = pd.DataFrame()

    out_frame_Labelframe = LabelFrame(out_frame,width=500,height=300,text="输出信息",padx=10,pady=10)
    out_frame_Text = Text(out_frame_Labelframe,width=80,height=7)
    out_frame_Text.grid()
    out_frame_Labelframe.grid()


    key_words = []
    bad_words = []
    hit_words = []
    sea_words = []
    done_words = []
    # bad_words = ["augmented reality","reversible","system","method","tool","process","indicator","technique","saucer"]

    if os.path.exists("缓存"):
        if os.path.isfile("缓存/排除词缓存.csv"):
            bad_words = list(pd.read_csv("缓存/排除词缓存.csv",header=None)[0])
            showinfo("[ ok ]---导入排除词成功")
        if os.path.exists("缓存/新增命中词缓存.csv"):
            hit_words = list(pd.read_csv("缓存/新增命中词缓存.csv",header=None)[0])
            showinfo("[ ok ]---导入新增命中词成功")
        if os.path.exists("缓存/搜索记录缓存.csv"):
            sea_words = list(pd.read_csv("缓存/搜索记录缓存.csv",header=None)[0])
            showinfo("[ ok ]---导入搜索记录成功")
        if os.path.exists("缓存/关键词缓存.csv"):
            key_words = list(pd.read_csv("缓存/关键词缓存.csv",header=None)[0])
            showinfo("[ ok ]---导入关键词成功")
        if os.path.exists("缓存/done.csv"):
            done_words = list(pd.read_csv("缓存/done.csv",header=None)[0])
            showinfo("[ ok ]---导入done成功")

    time_sacle = "5"
    failurls = []
    w_box = 400   
    h_box = 400
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }

    SURL = "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=page_change&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=search_change&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PTXT"
    SURL_2 = "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=page_change&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=search_change&FIELD1=&co1=AND&TERM2=term2_change&FIELD2=&d=PTXT"
    hit_word_Var = StringVar()
    hit_word_Var.set("新增命中词")
    hit_word_Entry = Entry(hit_frame,textvariable=hit_word_Var)
    def hit_word_Entry_bind(event):
        hit_word_Fun(hit_word_Var.get())
    hit_word_Entry.bind("<Return>", hit_word_Entry_bind)
    hit_word_Entry.grid(row=0,column=0)
    def hit_word_Fun(hit_word_var_):
        global hit_words
        if hit_word_var_ == "":
            pass
        elif hit_word_var_ == "新增命中词":
            pass
        else:
            if hit_word_var_ in hit_words:
                pass
            else:
                hit_words.append(str(hit_word_var_))
                hit_word_Listbox.delete(0,END)
                for hit_word in hit_words:
                    hit_word_Listbox.insert(END,hit_word)
                hit_word_Listbox.see(END)
                fast_clean_deep(str(hit_word_var_))
            hit_word_Var.set("新增命中词")
                    
    hit_word_Button = Button(hit_frame,text="添加",command=lambda :hit_word_Fun(hit_word_Var.get()))

    hit_word_Button.grid(row=0,column=1)
    def tip1(event):
        RightClickTip("新增命中词")
    hit_word_Button.bind("<Button-3>",tip1)

    def hit_word_save():
        if not os.path.exists("缓存"):
            os.mkdir("缓存")
        pd.DataFrame(hit_words).to_csv("缓存/新增命中词缓存.csv",header=FALSE,index=None)
        showinfo("[ ok ]---已保存到cache文件夹中")

    hit_word_save_Button = Button(hit_frame,text="保存",command=hit_word_save).grid(row=2,column=1)
    hit_word_Listbox = Listbox(hit_frame,height=10,width=32)
    # hit_word_Listbox = Listbox(hit_frame,height=10,width=60,yscrollcommand=hit_word_Scrollbar.set)
    for hit_word in hit_words:
        hit_word_Listbox.insert(END,hit_word)
    hit_word_Listbox.grid(row=1,columnspan=2)
    # hit_word_Scrollbar.config(command=hit_word_Listbox.yview)
    def delete_hit_word(hit_app):
        # showinfo("[ run ]---开始自动快速整理")
        df_hit = pd.read_excel("./已处理/命中数据.xlsx")
        df_rest = pd.read_excel("./已处理/未命中数据.xlsx")
        df_rest = pd.concat([df_rest,df_hit[df_hit["标题"].str.contains(hit_app)]])
        df_hit = df_hit[~df_hit["标题"].str.contains(hit_app)]
        df_hit.to_excel("./已处理/命中数据.xlsx",index=None)
        df_rest.to_excel("./已处理/未命中数据.xlsx",index=None)
        # showinfo("[ ok ]---自动快速整理完成")
        global check_1,check_2
        check_1 = False
        check_2 = False
        _check()
    def hit_word_Listbox_delete(ACTIVE):
        global hit_words
        delete_hit_word(hit_words[int(hit_word_Listbox.curselection()[0])])
        hit_words = [j for i,j in enumerate(hit_words) if i != int(hit_word_Listbox.curselection()[0])]
        hit_word_Listbox.delete(ACTIVE)
        hit_word_Listbox.delete(0,END)
        for hit_word in hit_words:
            hit_word_Listbox.insert(END,hit_word)

    hit_word_Listbox_Button = Button(hit_frame,text="删除命中词",command=lambda:hit_word_Listbox_delete(ACTIVE)).grid(row=2,columnspan=2)
    key_word_Var = StringVar()
    key_word_term2_Var = StringVar()
    key_word_Var.set("TERM1")
    key_word_term2_Var.set("TERM2")
    key_word_Entry = Entry(key_frame,textvariable=key_word_Var)
    key_word_term2 = Entry(key_frame,textvariable=key_word_term2_Var)
    def key_word_Entry_bind(event):
        key_word_Fun(key_word_Var.get(),key_word_term2_Var.get())
    key_word_Entry.bind("<Return>", key_word_Entry_bind)
    key_word_term2.bind("<Return>", key_word_Entry_bind)
    key_word_Entry.grid(row=0,column=0)
    key_word_term2.grid(row=0,column=1)
    def key_word_Fun(key_word_var_,key_word_term2_var_):
        global key_words
        if key_word_var_ == "":
            pass
        elif key_word_var_ == "TERM1":
            pass
        else:
            if key_word_term2_var_ == "TERM2" or key_word_term2_var_ == "":
                key_word_var_ = key_word_var_.lower()
                if key_word_var_ in key_words:
                    pass
                else:
                    key_words.append(str(key_word_var_))
                    key_word_Listbox.delete(0,END)
                    for key_word in key_words:
                        key_word_Listbox.insert(END,key_word)
                    key_word_Listbox.see(END)
            else:
                key_two_ = key_word_var_.lower() +"&"+key_word_term2_var_.lower()
                if key_two_ in key_words:
                    pass
                else:
                    key_words.append(str(key_two_))
                    key_word_Listbox.delete(0,END)
                    for key_word in key_words:
                        key_word_Listbox.insert(END,key_word)
                    key_word_Listbox.see(END)
            key_word_term2_Var.set("TERM2")
            key_word_Var.set("TERM1")
    def tip2(event):
        RightClickTip("关键词查询")
    key_word_Button = Button(key_frame,text="添加关键词",command=lambda :key_word_Fun(key_word_Var.get(),key_word_term2_Var.get()))
    key_word_Button.grid(row=0,column=2)
    key_word_Button.bind("<Button-3>",tip2)
    def key_word_save():
        if not os.path.exists("缓存"):
            os.mkdir("缓存")
        pd.DataFrame(key_words).to_csv("缓存/关键词缓存.csv",header=FALSE,index=None)
        showinfo("[ ok ]---已保存到cache文件夹中")

    key_word_save_Button = Button(key_frame,text="保存",command=key_word_save).grid(row=2,column=1)
    key_word_Listbox = Listbox(key_frame,height=10,width=60)
    # key_word_Listbox = Listbox(key_frame,height=10,width=60,yscrollcommand=key_word_Scrollbar.set)
    for key_word in key_words:
        key_word_Listbox.insert(END,key_word)
    key_word_Listbox.grid(row=1,columnspan=3)
    # key_word_Scrollbar.config(command=key_word_Listbox.yview)
    def key_word_Listbox_delete(ACTIVE):
        global key_words
    #     showinfo(int(key_word_Listbox.curselection()[0]))
        key_words = [j for i,j in enumerate(key_words) if i != int(key_word_Listbox.curselection()[0])]
        key_word_Listbox.delete(ACTIVE)
        key_word_Listbox.delete(0,END)
        for key_word in key_words:
            key_word_Listbox.insert(END,key_word)

    key_word_Listbox_Button = Button(key_frame,text="删除关键词",command=lambda:key_word_Listbox_delete(ACTIVE)).grid(row=2,columnspan=2)


    sea_word_Var = StringVar()
    sea_word_Var.set("搜索一下")
    sea_word_Entry = Entry(sea_frame,textvariable=sea_word_Var)
    def sea_word_Entry_bind(event):
        sea_word_Fun(sea_word_Var.get())

    sea_word_Entry.bind("<Return>", sea_word_Entry_bind)
    sea_word_Entry.grid(row=0,column=0)
    def write():
        pil_image = Image.new('RGB', (500, 500), (255,255,255))
        tk_image = ImageTk.PhotoImage(pil_image)
        label_img.configure(image=tk_image)
        label_img.image = tk_image
    def resize(w_box,h_box,pil_image):
        w,h = pil_image.size
        f1 = 1.0*w_box/w
        f2 = 1.0*h_box/h
        factor = min([f1,f2])
        width = int(w*factor)
        height = int(h*factor)
        return pil_image.resize((width,height),Image.ANTIALIAS)
    def forget_():
        write()
        search_all_button.grid_forget()
        search_rest_button.grid_forget()
        search_hit_button.grid_forget()
    def clear_tree(tree):
        x=tree.get_children()
        for item in x:
            tree.delete(item)
    def show_search_all():
        write()
        search_word_var_ = sea_word_Var.get()
        clear_tree(tree)
        df_search = muti_search(df_all,search_word_var_)
        # df_search = df_all[df_all["标题"].str.contains(search_word_var_)]
        for i,tup in enumerate(zip(df_search['标题'],df_search['pdf下载链接'],df_search["是否下载"])):
            tree.insert("",i,values=tup)
        global down_flag
        down_flag="s_all"
    def show_search_rest():
        # forget_()
        write()
        search_word_var_ = sea_word_Var.get()
        clear_tree(tree)
        df_search = muti_search(df_rest,search_word_var_)
        # df_search = df_rest[df_rest["标题"].str.contains(search_word_var_)]
        for i,tup in enumerate(zip(df_search['标题'],df_search['pdf下载链接'],df_search["是否下载"])):
            tree.insert("",i,values=tup)
        global down_flag
        down_flag="s_rest"
    def show_search_hit():
        # forget_()
        write()
        search_word_var_ = sea_word_Var.get()
        clear_tree(tree)
        df_search = muti_search(df_hit,search_word_var_)
        # df_search = df_hit[df_hit["标题"].str.contains(search_word_var_)]
        for i,tup in enumerate(zip(df_search['标题'],df_search['pdf下载链接'],df_search["是否下载"])):
            tree.insert("",i,values=tup)
        global down_flag
        down_flag="s_hit"
    def show_df_all():
        forget_()
        # tmp.grid(row=0,column=0,columnspan=3)
        tree.pack(side=LEFT, fill=Y)
        scrollbar.pack(side=RIGHT,fill=Y)
        clear_tree(tree)
        for i,tup in enumerate(zip(df_all['标题'],df_all['pdf下载链接'],df_all["是否下载"])):
            tree.insert("",i,values=tup)
        # label_img.grid(row=1,column=0,columnspan=3)
        global down_flag
        down_flag="all"
    def show_df_hit():
        forget_()
        # tmp.grid(row=0,column=0,columnspan=3)
        tree.pack(side=LEFT, fill=Y)
        scrollbar.pack(side=RIGHT,fill=Y)
        clear_tree(tree)
        for i,tup in enumerate(zip(df_hit['标题'],df_hit['pdf下载链接'],df_hit["是否下载"])):
            tree.insert("",i,values=tup)
        # label_img.grid(row=1,column=0,columnspan=3)
        global down_flag
        down_flag="hit"
    def show_df_rest():
        forget_()
        # tmp.grid(row=0,column=0,columnspan=3)
        tree.pack(side=LEFT, fill=Y)
        scrollbar.pack(side=RIGHT,fill=Y)
        clear_tree(tree)
        for i,tup in enumerate(zip(df_rest['标题'],df_rest['pdf下载链接'],df_rest["是否下载"])):
            tree.insert("",i,values=tup)
        # label_img.grid(row=1,column=0,columnspan=3)
        global down_flag
        down_flag="rest"
    tmp = Frame(sho_frame)
    scrollbar = Scrollbar(tmp)
    # scrollbar.pack_forget()
    tree = Treeview(tmp,column=('c1', 'c2','c3'),show="headings",yscrollcommand=scrollbar.set,height=8)
    tree.column('c1', width=250, anchor='center')
    tree.column('c2', width=230, anchor='center')
    tree.column('c3', width=100, anchor='center')
    tree.heading('c1', text='标题')
    tree.heading('c2', text='pdf下载链接')
    tree.heading('c3', text='本地是否下载')
    tree.pack(side=LEFT, fill=Y)
    scrollbar.pack(side=RIGHT,fill=Y)
    scrollbar.config(command=tree.yview)
    def treeviewClick(event):
        for item in tree.selection():
            item_text = tree.item(item,"values")
            if item_text[2]!="":
                # showinfo(item_text[2])
                img = Image.open(str(item_text[2]))
                img_resized = resize(w_box,h_box,img)
                tk_resized = ImageTk.PhotoImage(img_resized)
                # label_img.grid(row=2,column=0,columnspan=3)
                label_img.configure(image=tk_resized)
                label_img.image = tk_resized
            else:
                write()
    def treeviewRightClick(event):
        for item in tree.selection():
            item_text = tree.item(item,"values")
            # showinfo(item_text[1])
            webbrowser.open(item_text[1])
    tree.bind('<Button-1>', treeviewClick)
    tree.bind("<Button-3>",treeviewRightClick)
    # label_img = Label(tmp)
    # label_img.pack_forget()
    tmp.grid(row=1,column=0,columnspan=5)

    down_flag = ""

    def MyThread_download_search():
        MyThread(download_search)

    def download_search():
        showinfo("download_search")
        showinfo(down_flag)
        if down_flag == "all":
            df = df_all
        elif down_flag == "rest":
            df = df_rest
        elif down_flag == "hit":
            df = df_hit
        elif down_flag == "s_all":
            df = muti_search(df_all,sea_word_Var.get())
        elif down_flag == "s_rest":
            df = muti_search(df_rest,sea_word_Var.get())
        elif down_flag == "s_hit":
            df = muti_search(df_hit,sea_word_Var.get())
        down_search(df)
        global check_1,check_2
        check_1 = False
        check_2 = False
        _check()
        
        
    def wenjiajia():
        try:
            os.startfile(os.path.join(os.getcwd(),"已处理"))
        except:
            os.startfile(os.getcwd())
    def tip11(event):
        RightClickTip("显示所有数据")
    def tip12(event):
        RightClickTip("显示未命中数据")
    def tip13(event):
        RightClickTip("显示命中数据")
    def tip14(event):
        RightClickTip("打开文件夹")
    def tip15(event):
        RightClickTip("下载图片")
    df_all_button = Button(sho_frame,text="显示所有数据",command=show_df_all)
    df_all_button.grid(row=0,column=0)
    df_all_button.bind("<Button-3>",tip11)
    df_rest_button = Button(sho_frame,text="显示未命中数据",command=show_df_rest)
    df_rest_button.grid(row=0,column=1)
    df_rest_button.bind("<Button-3>",tip12)
    df_hit_button = Button(sho_frame,text="显示命中数据",command=show_df_hit)
    df_hit_button.grid(row=0,column=2)
    df_hit_button.bind("<Button-3>",tip13)
    show_wenjianjia_Button = Button(sho_frame,text="打开文件夹",command=wenjiajia)
    show_wenjianjia_Button.grid(row=0,column=3)
    show_wenjianjia_Button.bind("<Button-3>",tip14)
    download_search_Button = Button(sho_frame,text="下载图片",command=MyThread_download_search)
    download_search_Button.grid(row=0,column=4)
    download_search_Button.bind("<Button-3>",tip15)
    search_all_button = Button(sho_frame,text="所有数据中",command=show_search_all)
    search_rest_button = Button(sho_frame,text="未命中数据中",command=show_search_rest)
    search_hit_button = Button(sho_frame,text="命中数据中",command=show_search_hit)

    search_all_button.grid_forget()
    search_rest_button.grid_forget()
    search_hit_button.grid_forget()
    # tmp.grid_forget()
    def muti_search(df_all,search_tmp):
        df_for = df_all[df_all["标题"].str.contains(search_tmp.split("+")[0])]

        for i in search_tmp.split("+")[1:]:
            df_for = df_for[df_for["标题"].str.contains(i)]

        return df_for

    def sea_word_Fun(sea_word_var_):
        global sea_words
        if sea_word_var_ == "":
            pass
        elif sea_word_var_ == "搜索一下":
            pass
        else:
            showinfo("[ ok ]---搜索 "+str(sea_word_var_)+" 中")
            forget_()
            clear_tree(tree)
            # tmp.grid(row=0,column=0,columnspan=3)
            search_all_button.grid(row=2,column=0)
            search_rest_button.grid(row=2,column=1)
            search_hit_button.grid(row=2,column=2)
            df_search = muti_search(df_all,sea_word_var_)
            # df_search = df_all[df_all["标题"].str.contains(sea_word_var_)]
            for i,tup in enumerate(zip(df_search['标题'],df_search['pdf下载链接'],df_search["是否下载"])):
                tree.insert("",i,values=tup)
            if sea_word_var_ in sea_words:
                pass
            else:
                sea_words.append(str(sea_word_var_))
                sea_word_Listbox.delete(0,END)
                for sea_word in sea_words:
                    sea_word_Listbox.insert(END,sea_word)
                sea_word_Listbox.see(END)
            sea_word_Var.set("搜索一下")
    def tip3(event):
        RightClickTip("搜索关键词")                
    sea_word_Button = Button(sea_frame,text="添加",command=lambda:sea_word_Fun(sea_word_Var.get()))
    sea_word_Button.grid(row=0,column=1)
    sea_word_Button.bind("<Button-3>",tip3)
    def sea_word_save():
        if not os.path.exists("缓存"):
            os.mkdir("缓存")
        pd.DataFrame(sea_words).to_csv("缓存/搜索记录缓存.csv",header=FALSE,index=None)
        showinfo("[ ok ]---已保存到cache文件夹中")

    sea_word_save_Button = Button(sea_frame,text="保存",command=sea_word_save).grid(row=2,column=1)
    sea_word_Listbox = Listbox(sea_frame,height=10,width=32)
    # sea_word_Listbox = Listbox(sea_frame,height=10,width=60,yscrollcommand=sea_word_Scrollbar.set)
    for sea_word in sea_words:
        sea_word_Listbox.insert(END,sea_word)
    sea_word_Listbox.grid(row=1,columnspan=2)
    # sea_word_Scrollbar.config(command=sea_word_Listbox.yview)
    def sea_word_Listbox_delete(ACTIVE):
        global sea_words
    #     showinfo(int(sea_word_Listbox.curselection()[0]))
        sea_words = [j for i,j in enumerate(sea_words) if i != int(sea_word_Listbox.curselection()[0])]
        sea_word_Listbox.delete(ACTIVE)
        sea_word_Listbox.delete(0,END)
        for sea_word in sea_words:
            sea_word_Listbox.insert(END,sea_word)
    def sea_word_Listbox_double(event):
        # showinfo()
        sea_word_Fun(sea_word_Listbox.get(sea_word_Listbox.curselection()))
    sea_word_Listbox_Button = Button(sea_frame,text="删除搜索记录",command=lambda:sea_word_Listbox_delete(ACTIVE)).grid(row=2,columnspan=2)
    sea_word_Listbox.bind("<Double-1>",sea_word_Listbox_double)


    bad_word_Var = StringVar()
    bad_word_Var.set("排除无关词")
    bad_word_Entry = Entry(bad_frame,textvariable=bad_word_Var)
    def bad_word_Entry_bind(event):
        bad_word_Fun(bad_word_Var.get())
    bad_word_Entry.bind("<Return>", bad_word_Entry_bind)
    bad_word_Entry.grid(row=0,column=0)
    def bad_word_Fun(bad_word_var_):
        global bad_words,hit_words
        if bad_word_var_ == "":
            pass
        elif bad_word_var_ == "排除无关词":
            pass
        else:
            if bad_word_var_ in bad_words:
                pass
            else:
                bad_words.append(str(bad_word_var_))
                if str(bad_word_var_) in hit_words:
                    hit_words.remove(str(bad_word_var_))
                bad_word_Listbox.delete(0,END)
                for bad_word in bad_words:
                    bad_word_Listbox.insert(END,bad_word)
                bad_word_Listbox.see(END)
                clean_deep()
            bad_word_Var.set("排除无关词")
                    
    def tip4(event):
        RightClickTip("排除无关词")
    bad_word_Button = Button(bad_frame,text="添加",command=lambda:bad_word_Fun(bad_word_Var.get()))
    bad_word_Button.grid(row=0,column=1)
    bad_word_Button.bind("<Button-3>",tip4)
    bad_word_Listbox = Listbox(bad_frame,height=10,width=32)
    for bad_word in bad_words:
        bad_word_Listbox.insert(END,bad_word)
    bad_word_Listbox.grid(row=1,column=0,columnspan=2)

    def bad_word_Listbox_delete(ACTIVE):
        global bad_words
    #     showinfo(int(bad_word_Listbox.curselection()[0]))
        bad_words = [j for i,j in enumerate(bad_words) if i != int(bad_word_Listbox.curselection()[0])]
        bad_word_Listbox.delete(ACTIVE)
        bad_word_Listbox.delete(0,END)
        for bad_word in bad_words:
            bad_word_Listbox.insert(END,bad_word)
        clean_deep()

    def bad_word_save():
        if not os.path.exists("缓存"):
            os.mkdir("缓存")
        pd.DataFrame(bad_words).to_csv("缓存/排除词缓存.csv",header=FALSE,index=None)
        showinfo("[ ok ]---已保存到cache文件夹中")

    bad_word_Listbox_Button = Button(bad_frame,text="删除排除词",command=lambda:bad_word_Listbox_delete(ACTIVE)).grid(row=2,column=0)
    bad_word_save_Button = Button(bad_frame,text="保存",command=bad_word_save).grid(row=2,column=1)

    def MyThread_pdf():
        MyThread(pdf_down)
    def MyThread_spider():
        MyThread(spider)
    #开始爬取数据
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
                    showinfo(key+"---没有找到匹配专利")
                    done_words.append(key)
                else:
                    page_num = int(float(total_len)/50.5)+2
                    showinfo(key+"一共"+str(total_len)+"个专利，共"+str(page_num-1)+"页")
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
                    showinfo("导出"+key+"第一页")
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
            start = time.time()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            tasks = [asyncio.ensure_future(download(key)) for key in key_urls]
            if len(tasks) != 0:
                loop.run_until_complete(asyncio.wait(tasks))
            showinfo("[ tip ]---所有第一页已经爬取完成")
            tasks_s = []
            loop_s = asyncio.new_event_loop()
            asyncio.set_event_loop(loop_s)
            for key in pages_key_urls:
                for url in pages_key_urls[key]:
                    tasks_s.append(asyncio.ensure_future(download_s(key,url)))
            if len(tasks_s) !=0:
                loop_s.run_until_complete(asyncio.wait(tasks_s))
            showinfo("#"*40)
            end = time.time()
            showinfo('总共耗时{}秒'.format(end-start))
            showinfo("[ ok ]---全部导出完毕，保存在“原始数据”文件夹中")
            
            clean()
            clean_deep()

    # 清洗源数据
    def clean():
        def data_deal(df):
            def title_change(title):
                if title[0] == " ":
                    title = title[1:]
                title = title.lower()
                return title
            def img_change(img):
                a = img.split("=")[1]
                if a[0] == "D":
                    a = a[0] + "0" + a[1:]
                elif a[:2] == "PP":
                    a = a[:2] + "0" + a[2:]
                else:
                    while(1):
                        if len(a)>=8:
                            break
                        a = "0"+a
                return "https://pdfpiw.uspto.gov/.piw?Docid="+a
            def down_url(img):
                a = img.split("=")[1]
                one = a[-2:]
                two = a[-5:-2]
                three = a[-8:-5]
                return "https://pdfpiw.uspto.gov/"+one+"/"+two+"/"+three+"/1.pdf"
            def patent(img):
                a = img.split("=")[1]
                return a
            df["专利号"] = df.apply(lambda row:patent(row["图片链接"]),axis=1)
            df["标题"] = df.apply(lambda row:title_change(row["标题"]),axis=1)
            df["图片链接"] = df.apply(lambda row:img_change(row["图片链接"]),axis=1)
            df["pdf下载链接"] = df.apply(lambda row:down_url(row["图片链接"]),axis=1)
            
            return df
        
        path = "./原始数据/"
        if not os.path.exists(path):
            showinfo("[ error ]---源数据未获取")
        else:
            files = os.listdir(path)
            if len(files) == 0:
                showinfo("[ error ]---源数据为空" )
            else:
                if not os.path.exists("已处理"):
                    os.mkdir("已处理")
                writer = pd.ExcelWriter("./已处理/初步数据整理.xlsx")    
                for file in files:
                    df = pd.read_csv(path+file,header=None,names=["标题","pdf下载链接","图片链接"])
                    key = file.split(".")[0]
                    df = data_deal(df)
                    df.drop_duplicates(subset=["专利号"],keep="first",inplace=True)
                    df.to_excel(writer,sheet_name=key,index=None)
                showinfo("[ ok ]---数据清洗完成，已保存到“/已处理”文件夹中")
                writer.close()


    def fast_clean_deep(hit_app):
        showinfo("[ run ]---开始自动快速整理")
        df_hit = pd.read_excel("./已处理/命中数据.xlsx")
        df_rest = pd.read_excel("./已处理/未命中数据.xlsx")
        df_hit = pd.concat([df_hit,df_rest[df_rest["标题"].str.contains(hit_app)]])
        df_rest = df_rest[~df_rest["标题"].str.contains(hit_app)]
        df_hit.to_excel("./已处理/命中数据.xlsx",index=None)
        df_rest.to_excel("./已处理/未命中数据.xlsx",index=None)
        showinfo("[ ok ]---自动快速整理完成")
        global check_1,check_2
        check_1 = False
        check_2 = False
        _check()
        
    #深度清洗源数据
    def clean_deep():
        global df_rest,df_all,df_hit
        global check_1,check_2
        if len(df_rest) == 0 and len(df_all) == 0 and len(df_hit) == 0:
            showinfo("[ run ]---正在进行深度清洗源数据")
            if not os.path.exists("已处理"):
                showinfo("[ warning ]---数据未清洗，尝试自动清洗")
                clean()
            if not os.path.exists("已处理") or len(os.listdir("已处理"))==0:
                showinfo("[ error ]---自动清洗失败")
            else:
                df = pd.read_excel("./已处理/初步数据整理.xlsx",None)
                keys = list(df.keys())
                df_all = pd.DataFrame()
                for i in keys:
                    df_i = df[i]
                    df_all = pd.concat([df_all,df_i])
                df_all.drop_duplicates(subset=["专利号"],keep="first",inplace=True)
                # global key_words,bad_words,hit_words
                Hit = [i.lower() for i in key_words]
                hit_apps = [i.lower() for i in hit_words]
                df_rest = df_all
                df_hit = pd.DataFrame()
                for i in Hit:
                    df_hit_i = df_rest[df_rest["标题"].str.contains(i)]
                    df_rest = df_rest[~df_rest["标题"].str.contains(i)]
                    df_hit = pd.concat([df_hit,df_hit_i])
                if len(df_hit)==0:
                    showinfo("[ tip ]---命中数据为空")
                else:
                    for i in bad_words:
                        i = i.lower()
                        df_rest = pd.concat([df_rest,df_hit[df_hit["标题"].str.contains(i)]])
                        df_hit = df_hit[~df_hit["标题"].str.contains(i)]
                for i in hit_apps:
                    df_hit = pd.concat([df_hit,df_rest[df_rest["标题"].str.contains(i)]])
                    df_rest = df_rest[~df_rest["标题"].str.contains(i)]
                df_hit.drop_duplicates(subset=["专利号"],keep="first",inplace=True)
                df_rest.drop_duplicates(subset=["专利号"],keep="first",inplace=True)
                df_hit.to_excel("./已处理/命中数据.xlsx",index=None)
                df_all.to_excel("./已处理/全部数据.xlsx",index=None)
                df_rest.to_excel("./已处理/未命中数据.xlsx",index=None)
                showinfo("[ test ]---"+str(len(df_hit))+"---"+str(len(df_rest)))
                showinfo("[ ok ]---深度数据整理完成，已保存到“/已处理”文件夹“命中数据.xlsx”中")
                check_1 = False
                check_2 = False
                _check()
        else:
            showinfo("[ run ]---快速深度清理")
            # global key_words,bad_words,hit_words
            Hit = [i.lower() for i in key_words]
            hit_apps = [i.lower() for i in hit_words]
            for i in Hit:
                df_hit_i = df_rest[df_rest["标题"].str.contains(i)]
                df_rest = df_rest[~df_rest["标题"].str.contains(i)]
                df_hit = pd.concat([df_hit,df_hit_i])
            for i in hit_apps:
                df_hit = pd.concat([df_hit,df_rest[df_rest["标题"].str.contains(i)]])
                df_rest = df_rest[~df_rest["标题"].str.contains(i)]
            if len(df_hit)==0:
                showinfo("[ tip ]---命中数据为空")
            else:
                for i in bad_words:
                    i = i.lower()
                    df_rest = pd.concat([df_rest,df_hit[df_hit["标题"].str.contains(i)]])
                    df_hit = df_hit[~df_hit["标题"].str.contains(i)]
            df_hit.drop_duplicates(subset=["专利号"],keep="first",inplace=True)
            df_rest.drop_duplicates(subset=["专利号"],keep="first",inplace=True)
            df_hit.to_excel("./已处理/命中数据.xlsx",index=None)
            df_all.to_excel("./已处理/全部数据.xlsx",index=None)
            df_rest.to_excel("./已处理/未命中数据.xlsx",index=None)
            showinfo("[ test ]---"+str(len(df_hit))+"---"+str(len(df_rest)))
            showinfo("[ ok ]---快速深度数据整理完成，已保存到“/已处理”文件夹“命中数据.xlsx”中")
            check_1 = False
            check_2 = False
            _check()
    #pdf下载和整理
    def down_search(df):
        pdf_dir = "tmp/pdf/"
        png_dir = "tmp/png/"
        png_time = "tmp/png_time/"
        png_get = "tmp/png_get/"
        thread_num = 50 if len(df) >=50 else len(df)
        timeout = 30
        len_to_download = 0
        failurls = []
        showinfo("[ run ]---正在进行pdf下载")
        showinfo("[ tip ]---这一步需要很长时间，请耐心等待。")
        def download(img_url,img_name):
            img_name = img_name +".pdf"
            if os.path.isfile(os.path.join(pdf_dir,img_name)):
                return
            with closing(requests.get(img_url,stream=True,headers=headers,timeout=timeout)) as r:
                rc = r.status_code
                if 299 < rc or rc < 200:
                    showinfo ('returnCode%s\t%s' % (rc, img_url))
                    return
                content_length = int(r.headers.get('content-length', '0'))
                if content_length == 0:
                    showinfo ('size0\t%s' % img_url)
                    return
                try:
                    with open(os.path.join(pdf_dir,img_name),"wb") as f:
                        for data in r.iter_content(8192):
                            f.write(data)
                except:
                    showinfo('savefail\t%s' % img_url)
        lock = threading.Lock()
        def loop(imgs):
            while True:
                try:
                    with lock:
                        img_url,img_name = next(imgs)
        #                 showinfo(img_name)
                except StopIteration:
                    break
                try:
                    download(img_url,img_name)
                except:
                    global failurls
                    failurls.append((img_url,img_name))
                    showinfo("exceptfail\t%s"%img_url)
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
                    showinfo ('returnCode%s\t%s' % (rc, img_url))
                    return
                content_length = int(r.headers.get('content-length', '0'))
                if content_length == 0:
                    showinfo ('size0\t%s' % img_url)
                    return
                try:
                    with open(os.path.join(pdf_dir,img_name),"wb") as f:
                        for data in r.iter_content(8192):
                            f.write(data)
                except:
                    showinfo('savefail\t%s' % img_url)
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
        showinfo("[ run ]---pdf下载完成，正在检查是否有下载失败的内容")
        if len(failurls) != 0:
            showinfo("[ warning ]---有"+str(len(failurls))+"个下载失败，现在尝试重下")
            flag = 0
            while True:
                if len(failurls)==0:
                    showinfo("[ ok ]---全部重下完成")
                    break
                if len(os.listdir(pdf_dir)) == len_to_download:
                    showinfo("[ ok ]---全部重下完成")
                    break
                if flag >= 5:
                    showinfo("[ error ]---以下链接多次下载仍然失败")
                    showinfo(" 可尝试手动下载，放在image文件夹中")
                    for i,j in failurls:
                        showinfo(i+j)
                    break
                tryagain_fail(failurls)
                flag += 1
        showinfo("[ run ]---开始pdf转png")
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
                    showinfo("完成了"+str(j)+"个")
            except:
                showinfo(fitz.TOOLS.mupdf_warnings())
                showinfo("出错 --"+name)

        files = os.listdir(png_dir)
        showinfo("[ run ]---开始图片切割")
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
                showinfo("完成了"+str(j)+"个")
        showinfo("[ ok ]---pdf转png成功，保存在png_get,png_time文件夹中")        


    def pdf_down():
        showinfo("[ run ]---正在进行pdf下载")
        showinfo("[ tip ]---这一步需要很长时间，请耐心等待。")
        img_dir = "pdf/"
        tmp_dir = "tmp/pdf"
        thread_num = 50 

        timeout = 30
        len_to_download = 0
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        def download(img_url,img_name):
            img_name = img_name +".pdf"
            if os.path.isfile(os.path.join(img_dir,img_name)):
                return
            if os.path.isfile(os.path.join(tmp_dir,img_name)):
                copyfile(os.path.join(tmp_dir,img_name),os.path.join(img_dir,img_name))
                return
            with closing(requests.get(img_url,stream=True,headers=headers,timeout=timeout)) as r:
                rc = r.status_code
                if 299 < rc or rc < 200:
                    showinfo ('returnCode%s\t%s' % (rc, img_url))
                    return
                content_length = int(r.headers.get('content-length', '0'))
                if content_length == 0:
                    showinfo ('size0\t%s' % img_url)
                    return
                with open(os.path.join(img_dir,img_name),"wb") as f:
                    for data in r.iter_content(8192):
                        f.write(data)
                # except:
                #     showinfo('savefail\t%s' % img_url)
        lock = threading.Lock()
        
        def loop(imgs):
        #     showinfo ('thread %s is running...' % threading.current_thread().name)
            while True:
                try:
                    with lock:
                        img_url,img_name = next(imgs)
        #                 showinfo(img_name)
                except StopIteration:
                    break
                try:
                    download(img_url,img_name)
                except:
                    global failurls
                    failurls.append((img_url,img_name))
                    showinfo("exceptfail\t%s"%img_url)
        def get_img_url_generate():
            imgs = []
            df = pd.read_excel("./已处理/命中数据.xlsx")
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
        tsk = []
        imgs = get_img_url_generate()
        for i in range(0,thread_num):
            t = threading.Thread(target=loop,name="LoopThread %s" %i,args=(imgs,))
            t.start()
            tsk.append(t)
        for tt in tsk:
            tt.join()
        showinfo("[ run ]---pdf下载完成，正在检查是否有下载失败的内容")
        def tryagain_fail(fail_urls):
            global failurls
            failurls = []
            for img_url, img_name in fail_urls:
                img_name = str(img_name) +".pdf"
                if os.path.isfile(os.path.join(img_dir,img_name)):
                    return
                r = requests.get(img_url,stream=True,headers=headers,timeout=timeout)
                rc = r.status_code
                if 299 < rc or rc < 200:
                    showinfo ('returnCode%s\t%s' % (rc, img_url))
                    return
                content_length = int(r.headers.get('content-length', '0'))
                if content_length == 0:
                    showinfo ('size0\t%s' % img_url)
                    return
                try:
                    with open(os.path.join(img_dir,img_name),"wb") as f:
                        for data in r.iter_content(8192):
                            f.write(data)
                except:
                    showinfo('savefail\t%s' % img_url)
                    failurls.append((img_url,img_name))
        if len(failurls) != 0:
            showinfo("[ warning ]---有"+str(len(failurls))+"个下载失败，现在尝试重下")
            flag = 0
            while True:
                if len(failurls)==0:
                    showinfo("[ ok ]---全部重下完成")
                    break
                # if len(os.listdir(img_dir)) == len_to_download:
                #     showinfo("[ ok ]---全部重下完成")
                #     break
                if flag >= 5:
                    showinfo("[ error ]---以下链接多次下载仍然失败")
                    showinfo(" 可尝试手动下载，放在image文件夹中")
                    for i,j in failurls:
                        showinfo(str(i)+str(j))
                    break
                tryagain_fail(failurls)
                flag += 1
        showinfo("[ run ]---开始pdf转png")
        png_dir = "png/"
        if not os.path.exists(png_dir):
            os.makedirs(png_dir)
        for j,i in enumerate(os.listdir(img_dir)):
            name = i.split(".")[0] + ".png"
            if os.path.isfile(os.path.join(png_dir,name)):
                continue
            try:
                image = fitz.open(os.path.join(img_dir,i))
                page = image[0]
                rotate = int(0)
                zoom_x = 1.0
                zoom_y = 1.0
                trans = fitz.Matrix(zoom_x,zoom_y).preRotate(rotate)
                pm = page.getPixmap(matrix=trans,alpha=False)
                pm.writePNG(os.path.join(png_dir,name))
                if j % 50 == 0:
                    showinfo("完成了"+str(j)+"个")
            except:
                showinfo("出错 --"+name)

        files = os.listdir("./png/")
        showinfo("[ run ]---开始图片切割")
        for j,i in enumerate(files):
            img = Image.open("./png/"+i)
            w,h = img.size
            img_get = img.crop((0,int(h/2),w,h))
            tmp = img.crop((3*w/5,0,w,h/7))
            if not os.path.exists("png_time"):
                os.makedirs("png_time")
            if not os.path.exists("png_get"):
                os.makedirs("png_get")
            tmp.save("png_time/"+i)
            img_get.save("png_get/"+i)
            if j%50 == 0:
                showinfo("完成了"+str(j)+"个")
        showinfo("[ ok ]---pdf转png成功，保存在png_get,png_time文件夹中")
        _check()      

    def png2excel():
        showinfo("[ run ]---正在进行将图片插入到excel中")
        global check_1,check_2
        try:
            df_out = pd.read_excel("./已处理/命中数据.xlsx")
            df_out = df_out[["专利号","pdf下载链接"]]
            df_out.to_excel("./已处理/命中数据(简洁).xlsx",index=None)
            demo = xlrd.open_workbook("./已处理/命中数据(简洁).xlsx",on_demand=True)
            sheet_names = demo.sheet_names()
            final = xlsxwriter.Workbook("./已处理/最终结果.xlsx")
            for sheet_name in sheet_names:
                worksheet = final.add_worksheet(sheet_name)
                nrows = demo.sheet_by_name(sheet_name).nrows
                ncols = demo.sheet_by_name(sheet_name).ncols
                i = 0
                while i<nrows:
                    worksheet.write_row(i,0,demo.sheet_by_name(sheet_name).row_values(i))
                    if i >0:
                        s = str(demo.sheet_by_name(sheet_name).cell(i,ncols-2)).replace("text:","").replace("'","")
                        png = "png_get/"+s+".png"
                        worksheet.insert_image(i,ncols,png,{'x_scale': 0.3, 'y_scale': 0.3})
                        tim = "png_time/"+s+".png"
                        worksheet.insert_image(i,ncols+1,tim,{'x_scale': 0.8, 'y_scale': 0.8})
                    i += 1
                worksheet.write(0,ncols,"专利图片")
                worksheet.write(0,ncols+1,"授权时间")
                worksheet.set_default_row(80)
                worksheet.set_row(0,25)
                worksheet.set_column(ncols-1,ncols,40)
                worksheet.set_column(ncols,ncols+1,25)
            final.close()
            showinfo("[ ok ]---插入图片成功，已保存在cleaned文件夹'最终结果'.xlsx中")
            check_1 = False
            check_2 = False
            _check()
        except:
            showinfo("[ error ]---出现未知错误")
    # def MyThread_vip():
    #     MyThread(vip)
    def vip():
        showinfo("[ start ]---程序开始自动运行")
        showinfo("[ tip ]---请耐心等待")
        time.sleep(2)
        spider()
        clean()
        clean_deep()
        pdf_down()
        png2excel()
        showinfo("[ ok ]---一键操作完成")
        

    time_scale_var = StringVar()
    time_scale_var.set("5")
    def get_time_scale_var():
        global time_sacle
        time_sacle = str(time_scale_var.get())

    def tip5(event):
        RightClickTip("爬取时间间隔")
    def tip6(event):
        RightClickTip("开始爬取")
    def tip7(event):
        RightClickTip("深度数据整理")
    def tip8(event):
        RightClickTip("PDF下载和整理")
    def tip9(event):
        RightClickTip("插入图片到excel")
    def tip10(event):
        RightClickTip("一键爬取清洗下载保存导出")
    def open_tip():
        webbrowser.open("")
    fun_frame_Labelframe = LabelFrame(fun_frame,width=200,height=400,text="功能区",padx=10,pady=10)
    fun_frame_Label = Label(fun_frame_Labelframe,text="爬取时间间隔设置: 秒")
    fun_frame_Label.grid(row=0,column=0,sticky=E+W)
    fun_frame_Label.bind("<Button-3>",tip5)
    fun_frame_Spinbox = Spinbox(fun_frame_Labelframe,from_=1,to=100,increment=1,textvariable=time_scale_var,command=get_time_scale_var).grid(row=1,column=0,sticky=E+W)
    fun_frame_Button_spider = Button(fun_frame_Labelframe,text="开始爬取数据",command=MyThread_spider,pady=10)
    fun_frame_Button_spider.grid(row=2,column=0,sticky=E+W)     
    fun_frame_Button_spider.bind("<Button-3>",tip6)   
    # fun_frame_Button_clean = Button(fun_frame_Labelframe,text="初步数据整理",command=clean).grid(row=3,column=0,sticky=E+W)
    fun_frame_Button_clean_deep = Button(fun_frame_Labelframe,text="深度数据整理",command=clean_deep)
    fun_frame_Button_clean_deep.grid(row=4,column=0,sticky=E+W)
    fun_frame_Button_clean_deep.bind("<Button-3>",tip7)
    fun_frame_Button_pdf_download = Button(fun_frame_Labelframe,text="pdf下载和整理",command=MyThread_pdf,pady=10)
    fun_frame_Button_pdf_download.grid(row=5,column=0,sticky=E+W)
    fun_frame_Button_pdf_download.bind("<Button-3>",tip8)
    fun_frame_Button_png2excel = Button(fun_frame_Labelframe,text="插入图片到excel",command=png2excel,pady=10)
    fun_frame_Button_png2excel.grid(row=6,column=0,sticky=E+W)
    fun_frame_Button_png2excel.bind("<Button-3>",tip9)
    pil_image = Image.new('RGB', (500, 500), (255,255,255))
    tk_image = ImageTk.PhotoImage(pil_image)
    fun_frame_Button_vip = Button(fun_frame_Labelframe,text="一键爬取清洗下载保存导出",command=vip,pady=15)
    fun_frame_Button_vip.grid(row=7,column=0,columnspan=2,sticky=E+W)
    fun_frame_Button_vip.bind("<Button-3>",tip10)
    fun_frame_Button_tip = Button(fun_frame_Labelframe,text="查看使用手册",command=open_tip).grid(row=8,column=0,columnspan=2,sticky=E+W)
    fun_frame_Labelframe.grid()

    # 爬取数据之后
    check_1 = False
    check_2 = False

    def _check():
        global check_1,check_2
        global df_rest,df_all,df_hit
        if check_2 == False:
            if os.path.exists("已处理"):
                if os.path.isfile("已处理/全部数据.xlsx") and os.path.isfile("已处理/未命中数据.xlsx") and os.path.isfile("已处理/命中数据.xlsx"):
                    check_1 = True
                    # showinfo("[ tip ] check_1 = True")
            if check_1:
                df_all = pd.read_excel("已处理/全部数据.xlsx")
                df_rest = pd.read_excel("已处理/未命中数据.xlsx")
                df_hit = pd.read_excel("已处理/命中数据.xlsx")
                # df_hit = pd.merge(df_hit,df_all)
                if len(df_all) != 0:
                    df_all = df_all.reindex(df_all['标题'].str.len().sort_values(ascending=True).index)
                if len(df_rest) != 0:
                    df_rest = df_rest.reindex(df_rest['标题'].str.len().sort_values(ascending=True).index)
                if len(df_hit) != 0:
                    df_hit = df_hit.reindex(df_hit['标题'].str.len().sort_values(ascending=True).index)
                df_all["是否下载"]=""
                df_hit["是否下载"]=""
                df_rest["是否下载"]=""
                if not os.path.exists("tmp/png_get/"):
                    pass
                else:
                    for i in os.listdir("tmp/png_get/"):
                        ii = i.split(".")[0]
                        df_all.loc[df_all["专利号"]==ii,"是否下载"]=os.path.join("tmp/png_get/",i)
                        if '专利号' in list(df_hit.columns):  
                            df_hit.loc[df_hit["专利号"]==ii,"是否下载"]=os.path.join("tmp/png_get/",i)
                        df_rest.loc[df_rest["专利号"]==ii,"是否下载"]=os.path.join("tmp/png_get/",i)
                if not os.path.exists("png_get/"):
                    pass
                else:
                    for i in os.listdir("png_get/"):
                        ii = i.split(".")[0]
                        df_all.loc[df_all["专利号"]==ii,"是否下载"]=os.path.join("png_get/",i)
                        if '专利号' in list(df_hit.columns): 
                            df_hit.loc[df_hit["专利号"]==ii,"是否下载"]=os.path.join("png_get/",i)
                        df_rest.loc[df_rest["专利号"]==ii,"是否下载"]=os.path.join("png_get/",i)
                check_1 = False
                check_2 = True
                # showinfo("[ tip ] check_1 = False")
                showinfo("[ tip ] check = True")
                show_df_all()

    png_frame_Labelframe = LabelFrame(png_frame,text="图片展示区",padx=10,pady=10)

    label_img = Label(png_frame_Labelframe,image=tk_image)
    label_img.pack(expand=True,anchor="center",fill="both")
    png_frame_Labelframe.pack()

    key_frame.place(x=0,y=0)
    sea_frame.place(x=425,y=0)
    bad_frame.place(x=650,y=0)
    hit_frame.place(x=875,y=0)
    fun_frame.place(x=0,y=250)
    sho_frame.place(x=200,y=400)
    out_frame.place(x=200,y=250)
    png_frame.place(x=800,y=250)

    def on_closing():
        ans = messagebox.askokcancel("退出", "是否自动保存记录?")
        if ans:
            if not os.path.exists("缓存"):
                os.mkdir("缓存")
            if len(hit_words)!= 0:
                pd.DataFrame(hit_words).to_csv("缓存/新增命中词缓存.csv",header=FALSE,index=None)
            if len(bad_words)!= 0:
                pd.DataFrame(bad_words).to_csv("缓存/排除词缓存.csv",header=FALSE,index=None)
            if len(sea_words)!= 0:
                pd.DataFrame(sea_words).to_csv("缓存/搜索记录缓存.csv",header=FALSE,index=None)
            if len(key_words)!= 0:
                pd.DataFrame(key_words).to_csv("缓存/关键词缓存.csv",header=FALSE,index=None)
            if len(done_words)!= 0:
                pd.DataFrame(done_words).to_csv("缓存/done.csv",header=FALSE,index=None)
            root.destroy()
        else:
            if len(done_words)!= 0:
                pd.DataFrame(done_words).to_csv("缓存/done.csv",header=FALSE,index=None)
            root.destroy()
    root.after(1000,_check)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
