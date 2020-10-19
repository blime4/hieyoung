import os
import pandas as pd

key_words = ["plant hanger", "plant holder","wall plant"]
bad_words = []
hit_words = []
sea_words = []
# bad_words = ["augmented reality","reversible","system","method","tool","process","indicator","technique","saucer"]
df_rest = pd.DataFrame()
df_hit = pd.DataFrame()
df_all = pd.DataFrame()
check_1,check_2 = False,False

def clean_deep():
    global df_rest,df_all,df_hit
    print("[ run ]---正在进行深度清洗源数据")
    if not os.path.exists("已处理"):
        print("[ warning ]---数据未清洗，尝试自动清洗")
        # clean()
    if not os.path.exists("已处理") or len(os.listdir("已处理"))==0:
        print("[ error ]---自动清洗失败")
    else:
        df = pd.read_excel("./已处理/初步数据整理.xlsx",None)
        keys = list(df.keys())
        df_all = pd.DataFrame()
        for i in keys:
            df_i = df[i]
            df_all = pd.concat([df_all,df_i])
        df_all.drop_duplicates(subset=["专利号"],keep="first",inplace=True)
        global key_words,bad_words
        Hit = [i.lower() for i in key_words]
        hit_apps = [i.lower() for i in hit_words]
        df_rest = df_all
        df_hit = pd.DataFrame()
        for i in Hit:
            df_hit_i = df_rest[df_rest["标题"].str.contains(i)]
            df_rest = df_rest[~df_rest["标题"].str.contains(i)]
            df_hit = pd.concat([df_hit,df_hit_i])
        if len(df_hit)==0:
            print("[ tip ]---命中数据为空")
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
        print("[ ok ]---深度数据整理完成，已保存到“/已处理”文件夹“命中数据.xlsx”中")
        global check_1,check_2
        check_1 = False
        check_2 = False
        _check()

def _check():
    global check_1,check_2
    global df_rest,df_all,df_hit
    if check_2 == False:
        if os.path.exists("已处理"):
            if os.path.isfile("已处理/全部数据.xlsx") and os.path.isfile("已处理/未命中数据.xlsx") and os.path.isfile("已处理/命中数据.xlsx"):
                check_1 = True
                # print("[ tip ] check_1 = True")
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
            # print("[ tip ] check_1 = False")
            print("[ tip ] check = True")
            # show_df_all()




def test_clean_deep():
    global df_rest,df_all,df_hit
    print("[ run ]---正在进行深度清洗源数据")
    if not os.path.exists("已处理"):
        print("[ warning ]---数据未清洗，尝试自动清洗")
        # clean()
    if not os.path.exists("已处理") or len(os.listdir("已处理"))==0:
        print("[ error ]---自动清洗失败")
    else:
        df = pd.read_excel("./已处理/初步数据整理.xlsx",None)
        keys = list(df.keys())
        df_all = pd.DataFrame()
        for i in keys:
            df_i = df[i]
            df_all = pd.concat([df_all,df_i])
        df_all.drop_duplicates(subset=["专利号"],keep="first",inplace=True)
        global key_words,bad_words
        Hit = [i.lower() for i in key_words]
        hit_apps = [i.lower() for i in hit_words]
        df_rest = df_all
        df_hit = pd.DataFrame()
        for i in Hit:
            df_hit_i = df_rest[df_rest["标题"].str.contains(i)]
            df_rest = df_rest[~df_rest["标题"].str.contains(i)]
            df_hit = pd.concat([df_hit,df_hit_i])
        if len(df_hit)==0:
            print("[ tip ]---命中数据为空")
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
        print("[ test ]---"+str(len(df_hit))+"---"+str(len(df_rest)))
        print("[ ok ]---深度数据整理完成，已保存到“/已处理”文件夹“命中数据.xlsx”中")
