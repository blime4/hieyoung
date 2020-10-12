from tkinter import *
import os
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from contextlib import closing
import threading
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance
import xlsxwriter
import xlrd
import logging
from logging import handlers


key_words = ["plant hanger"]
# key_words = []
bad_words = ["augmented reality","reversible","system","method","tool","process","indicator","technique","saucer"]
time_sacle = "60"
failurls = []

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
}

url = "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=page_change&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=search_change&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PTXT"


root = Tk()
root.geometry('850x550')
root.title("专利查询和搜索")

key_frame = Frame(width=350,height=300,bg="LightPink")
bad_frame = Frame(width=350,height=300,bg="Thistle")
fun_frame = Frame(width=700,height=50,bg="LightSeaGreen")
out_frame = Frame(width=700,height=250,bg="green")

out_frame_Labelframe = LabelFrame(out_frame,width=700,height=200,text="输出信息",padx=10,pady=10)
out_frame_Text = Text(out_frame_Labelframe,width=100,height=10)

def showinfo(result):
    realtime = time.strftime("%Y-%m-%d %H:%M:%S ")
    textvar = realtime + result #系统时间和传入结果
    out_frame_Text.insert(END,textvar) #显示在text框里面
    out_frame_Text.insert(INSERT,'\n') #换行

out_frame_Text.grid()
out_frame_Labelframe.grid()
# key_word_Scrollbar = Scrollbar(key_frame).grid(rowspan=3,column)
key_word_Var = StringVar()
key_word_Var.set("填写关键词")
key_word_Entry = Entry(key_frame,width=30,textvariable=key_word_Var)
def key_word_Entry_bind(event):
    key_word_Fun(key_word_Var.get())
key_word_Entry.bind("<Return>", key_word_Entry_bind)
key_word_Entry.grid(row=0,column=0)
def key_word_Fun(key_word_var_):
    global key_words
    if key_word_var_ == "":
        pass
    elif key_word_var_ == "填写关键词":
        pass
    else:
        if key_word_var_ in key_words:
            pass
        else:
            key_words.append(str(key_word_var_))
            key_word_Listbox.delete(0,END)
            for key_word in key_words:
                key_word_Listbox.insert(END,key_word)
                
key_word_Button = Button(key_frame,text="添加",command=lambda:key_word_Fun(key_word_Var.get())).grid(row=0,column=1)
key_word_Listbox = Listbox(key_frame,selectmode=MULTIPLE,height=10,width=60)
# key_word_Listbox = Listbox(key_frame,selectmode=MULTIPLE,height=10,width=60,yscrollcommand=key_word_Scrollbar.set)
for key_word in key_words:
    key_word_Listbox.insert(END,key_word)
key_word_Listbox.grid(row=1,columnspan=2)
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



bad_word_Var = StringVar()
bad_word_Var.set("填写排除词")
bad_word_Entry = Entry(bad_frame,width=50,textvariable=bad_word_Var)
def bad_word_Entry_bind(event):
    bad_word_Fun(key_word_Var.get())
bad_word_Entry.bind("<Return>", key_word_Entry_bind)
bad_word_Entry.grid(row=0,column=0)
def bad_word_Fun(bad_word_var_):
    global bad_words
    if bad_word_var_ == "":
        pass
    elif bad_word_var_ == "填写排除词":
        pass
    else:
        if bad_word_var_ in bad_words:
            pass
        else:
            bad_words.append(str(bad_word_var_))
            bad_word_Listbox.delete(0,END)
            for bad_word in bad_words:
                bad_word_Listbox.insert(END,bad_word)
                
bad_word_Button = Button(bad_frame,text="添加",command=lambda:bad_word_Fun(bad_word_Var.get())).grid(row=0,column=1)
bad_word_Listbox = Listbox(bad_frame,selectmode=MULTIPLE,height=10,width=60)
for bad_word in bad_words:
    bad_word_Listbox.insert(END,bad_word)
bad_word_Listbox.grid(row=1,columnspan=2)

def bad_word_Listbox_delete(ACTIVE):
    global bad_words
#     showinfo(int(bad_word_Listbox.curselection()[0]))
    bad_words = [j for i,j in enumerate(bad_words) if i != int(bad_word_Listbox.curselection()[0])]
    bad_word_Listbox.delete(ACTIVE)
    bad_word_Listbox.delete(0,END)
    for bad_word in bad_words:
        bad_word_Listbox.insert(END,bad_word)
bad_word_Listbox_Button = Button(bad_frame,text="删除排除词",command=lambda:bad_word_Listbox_delete(ACTIVE)).grid(row=2,columnspan=2)

time_scale_var = StringVar()
time_scale_var.set("60")
def get_time_scale_var():
    global time_sacle
    time_sacle = str(time_scale_var.get())
fun_frame_Label = Label(fun_frame,text="爬取时间间隔设置: 秒").grid(row=0,column=0)
fun_frame_Spinbox = Spinbox(fun_frame,from_=1,to=100,increment=1,textvariable=time_scale_var,command=get_time_scale_var).grid(row=0,column=1)
# fun_frame_Scale = Scale(fun_frame,from_=1,to=100,resolution=1,orient=HORIZONTAL,variable=time_scale_var,command=get_time_scale_var).grid(row=0,column=1)

#开始爬取数据
def spider():
    showinfo("[ run ]---开始爬取数据")
    showinfo("[ tip ]---这一步需要的时间，和爬取的时间间隔和爬取的内容数量有关，请耐心等待。")
    global key_words
    global time_sacle
    spider_key_words = key_words
    for key_word in spider_key_words:
        page_a = []
        page_img = []
        page_href = []
        key_words_url = url
        key_words_url = key_words_url.replace("search_change",str(key_word))
        url_1 = key_words_url
        url_1 = url_1.replace("page_change","1")
        response = requests.get( url_1 , headers=headers )
        if response.status_code == 200:
            showinfo("[一切正常]---开始爬取 "+key_word)
        else:
            showinfo("[出错]---错误状态码："+response.status_code)
        html_doc = response.text
        response.close()
        soup = BeautifulSoup(html_doc, 'html.parser')
        total_len = soup.find("body").find_all("i")[1].find_all("strong")[2].get_text()
        page_num = int(float(total_len)/50.5)+2
        showinfo("一共"+total_len+"个论文，共"+str(page_num-1)+"页")
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
        time.sleep(int(time_sacle))
        if page_num >= 2:
            for i in range(2,page_num):
                url_i = key_words_url
                url_i = url_i.replace("page_change",str(i))
                response = requests.get( url_i , headers=headers )
                if response.status_code == 200:
                    showinfo("[一切正常]---爬取到第"+str(i)+"页")
                else:
                    showinfo("[出错]---错误状态码："+response.status_code)
                html_doc = response.text
                response.close()
                soup = BeautifulSoup(html_doc, 'html.parser')
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
                time.sleep(int(time_sacle))
        page_dict = {"标题":page_a,"专利链接":page_href,"图片链接":page_img}
        page_df = pd.DataFrame(page_dict)
        if not os.path.exists("raw_data"):
            os.mkdir("raw_data")
        page_df.to_excel("./raw_data/"+key_word+".xlsx",index=None)
        showinfo("[ ok ]---"+key_word)
    showinfo("[ ok ]---全部导出完毕，保存在raw_data文件夹中")



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
    
    path = "./raw_data/"
    if not os.path.exists(path):
        showinfo("[ error ]---源数据未获取")
    else:
        files = os.listdir(path)
        if len(files) == 0:
            showinfo("[ error ]---源数据为空" )
        else:
            if not os.path.exists("cleaned"):
                os.mkdir("cleaned")
            writer = pd.ExcelWriter("./cleaned/cleaned_data.xlsx")    
            for file in files:
                df = pd.read_excel(path+file)
                key = file.split(".")[0]
                df = data_deal(df)
                df.to_excel(writer,sheet_name=key,index=None)
            showinfo("[ ok ]---数据清洗完成，已保存到cleaned文件夹中")
            writer.close()
    



#深度清洗源数据
def clean_deep():
    showinfo("[ run ]---正在进行深度清洗源数据")
    if not os.path.exists("cleaned"):
        showinfo("[ warning ]---数据未清洗，尝试自动清洗")
        clean()
    if not os.path.exists("cleaned") or len(os.listdir("cleaned"))==0:
        showinfo("[ error ]---自动清洗失败")
    else:
        try:
            df = pd.read_excel("./cleaned/cleaned_data.xlsx",None)
            keys = list(df.keys())
            df_all = pd.DataFrame()
            for i in keys:
                df_i = df[i]
                df_all = pd.concat([df_i,df_all])
            global key_words,bad_words
            Hit = [i.lower() for i in key_words]
            df_rest = df_all
    #         def get_hit(Hit):
            df_hit = pd.DataFrame()
    #             global df_rest
            for i in Hit:
                df_hit_i = df_rest[df_rest["标题"].str.contains(i)]
                df_rest = df_rest[~df_rest["标题"].str.contains(i)]
                df_hit = pd.concat([df_hit,df_hit_i])
    #             return df_hit
    #         df_hit = get_hit(Hit)
    #         def deal_hit(df_hit):
            for i in bad_words:
                i = i.lower()
                df_hit = df_hit[~df_hit["标题"].str.contains(i)]
    #             return df_hit
    #         df_hit = deal_hit(df_hit)
            df_hit.drop_duplicates(subset=["专利号"],keep="first",inplace=True)
    #         df_hit["标题长度"] = df_hit.apply(lambda row:len(row["标题"]),axis=1)
    #         df_hit.sort_values(by="标题长度",inplace=True)
            df_hit = df_hit[["专利号","pdf下载链接"]]
            df_hit.to_excel("./cleaned/demo.xlsx",index=None)
            df_all.to_excel("./cleaned/df_all.xlsx",index=None)
            df_rest.to_excel("./cleaned/df_rest.xlsx",index=None)
            showinfo("[ ok ]---深度数据清洗完成，已保存到cleaned文件夹demo.xlsx中")
        except:
            showinfo("[ error ]---出现异常")
#pdf下载

def pdf_down():
    showinfo("[ run ]---正在进行pdf下载")
    showinfo("[ tip ]---这一步需要很长时间，请耐心等待。")
    img_dir = "pdf/"
    thread_num = 50
    timeout = 30
    len_to_download = 0
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    def download(img_url,img_name):
        img_name = img_name +".pdf"
        if os.path.isfile(os.path.join(img_dir,img_name)):
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
                with open(os.path.join(img_dir,img_name),"wb") as f:
                    for data in r.iter_content(8192):
                        f.write(data)
    #             jpg_name = img_name + ".jpg"    
    #             page = convert_from_path(os.path.join(img_dir,img_name))
    #             page[0].save(os.path.join(img_dir,jpg_name),"PNG")
    #                 image = convert_from_path(os.path.join(img_dir,i))
    #                 image[0].save(os.path.join(img_dir,name),"PNG")
            except:
                showinfo('savefail\t%s' % img_url)
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
#         showinfo("thread %s is end ..."% threading.current_thread().name)
    def get_img_url_generate():
        imgs = []
        df = pd.read_excel("./cleaned/demo.xlsx")
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
            img_name = img_name +".pdf"
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
            if len(os.listdir(img_dir)) == len_to_download:
                showinfo("[ ok ]---全部重下完成")
                break
            if flag >= 5:
                showinfo("[ error ]---以下链接多次下载仍然失败")
                showinfo(" 可尝试手动下载，放在image文件夹中")
                for i,j in failurls:
                    showinfo(i,j)
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
            image = convert_from_path(os.path.join(img_dir,i))
            image[0].save(os.path.join(png_dir,name),"PNG")
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
    
    
    
def png2excel():
    showinfo("[ run ]---正在进行将图片插入到excel中")
    try:
        demo = xlrd.open_workbook("./cleaned/demo.xlsx",on_demand=True)
        sheet_names = demo.sheet_names()
        final = xlsxwriter.Workbook("./cleaned/img.xlsx")
        for sheet_name in sheet_names:
            worksheet = final.add_worksheet(sheet_name)
            nrows = demo.sheet_by_name(sheet_name).nrows
            ncols = demo.sheet_by_name(sheet_name).ncols
            i = 0
            while i<nrows:
                worksheet.write_row(i,0,demo.sheet_by_name(sheet_name).row_values(i))
                if i >0:
                    s = str(demo.sheet_by_name(sheet_name).cell(i,ncols-2)).replace("text:","").replace("'","")
                    png = "image_get/"+s+".png"
                    worksheet.insert_image(i,ncols,png,{'x_scale': 0.09, 'y_scale': 0.09})
                    tim = "image_time/"+s+".png"
                    worksheet.insert_image(i,ncols+1,tim,{'x_scale': 0.3, 'y_scale': 0.3})
                i += 1
            worksheet.write(0,ncols,"专利图片")
            worksheet.write(0,ncols+1,"授权时间")
            worksheet.set_default_row(80)
            worksheet.set_column(ncols,ncols+1,25)
        final.close()
        showinfo("[ ok ]---插入图片成功，已保存在cleaned文件夹img.xlsx中")
    except:
        showinfo("[ error ]---出现未知错误")

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
    
fun_frame_Button_spider = Button(fun_frame,text="开始爬取数据",command=spider).grid(row=0,column=2)        
fun_frame_Button_clean = Button(fun_frame,text="清洗源数据",command=clean).grid(row=0,column=3)
fun_frame_Button_clean_deep = Button(fun_frame,text="深度清洗源数据",command=clean_deep).grid(row=0,column=4)
fun_frame_Button_pdf_download = Button(fun_frame,text="pdf下载",command=pdf_down).grid(row=0,column=5)
fun_frame_Button_png2excel = Button(fun_frame,text="插入图片到excel",command=png2excel).grid(row=0,column=6)
fun_frame_Button_vip = Button(fun_frame,text="一键完成爬取清洗下载保存导出",command=vip,width=100,padx=10,pady=10).grid(row=1,columnspan=7)
    

key_frame.grid(row=0,column=0)
bad_frame.grid(row=0,column=1)
fun_frame.grid(row=1,columnspan=2)
out_frame.grid(row=2,columnspan=2)

root.mainloop()