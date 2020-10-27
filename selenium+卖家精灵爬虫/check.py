import os
from get_asin import GetAsin

asin = GetAsin().from_txt()


asin_download = [i.split("-")[0] for i in os.listdir("./dataset")]
asin_download = list(set(asin_download))

for i in asin:
    if i not in asin_download:
        print(i)
    
for i in asin_download:
    if i not in asin:
        print(i)


