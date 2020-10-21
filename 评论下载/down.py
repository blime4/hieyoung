import os
import pandas as pd
import webbrowser
import shutil


df = pd.read_excel("./dd.xlsx",header=None)
df.columns = ["asin"]
for i in df["asin"]:
    url = "https://www.amazon.com/dp/"+i
    webbrowser.open(url)

df1 = pd.read_excel("./战术母婴包.xlsx",header=None)
df2 = pd.read_excel("./战术午餐包.xlsx",header=None)
df1.columns = ["asin"]
df2.columns = ["asin"]


if not os.path.exists("./战术母婴包"):
    os.mkdir("./战术母婴包")
if not os.path.exists("./战术午餐包"):
    os.mkdir("./战术午餐包")

for file in os.listdir("./dataset"):
    asin = file.split("-")[0]
    print(asin)
    if asin in list(df1["asin"]):
        shutil.copy("./dataset/"+file,"./战术母婴包")
    if asin in list(df2["asin"]):
        shutil.copy("./dataset/"+file,"./战术午餐包")

lissss = os.listdir("./战术母婴包")
lissss = [lis.split("-")[0] for lis in lissss]
l = list(df1["asin"])
for i in lissss:
    l.remove(i)
l
