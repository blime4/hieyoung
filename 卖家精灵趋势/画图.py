import matplotlib.pyplot as plt

import pandas as pd

colors = ["red", "green", "blue", "yellow"]

data = list(pd.read_csv("前两百条.csv")["月搜索趋势"])
keys= list(pd.read_csv("前两百条.csv")["关键词"])

daaa = {}
for ddd,key in zip(data,keys):
    dd = ddd.replace("{","").split("},")
    dd[-1] = dd[-1].replace("}","")
    da_xy = {}
    x_flag = ""
    for d in dd:
        xx = d.split(",")[0].split(":")[1].replace("'","")[:4]
        x = int(d.split(",")[0].split(":")[1].replace("'","")[4:])
        y = int(d.split(",")[1].split(":")[1])
        if xx != x_flag:
            da_xy[xx]=[[x,y]]
            x_flag=xx
        else:
            da_xy[xx].append([x,y])
    # for k in da_xy.keys():
    #     x = []
    #     y = []
    #     for i in da_xy[k]:
    #         x.append(i[0])
    #         y.append(i[1])  
    #     plt.plot(x,y,'-',label=k)
    # plt.title(key)
    # plt.xlabel("Month")
    # plt.ylabel("Search trends")
    # plt.legend()
    # plt.savefig("./缓存/"+key+".png",bbox_inches='tight')
    # plt.close()





