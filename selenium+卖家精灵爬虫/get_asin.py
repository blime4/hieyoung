import os

class GetAsin:
    def __init__(self):
        if not os.path.exists("缓存"):
            os.mkdir("缓存")
        
    def from_txt(self):
        try:
            with open("./缓存/asin.txt") as f:
                asin = [i.replace("\n","") for i in f.readlines()]
        except:
            print("asin.txt不存在")
        return asin
    
    def get_urls(self,asin):
        urls = ["https://www.amazon.com/dp/"+i for i in asin]
        return urls

    def get_urls_yield(self,asin):
        for i in asin:
            url = "https://www.amazon.com/dp/"+i
            yield url
if __name__ == "__main__":
    G = GetAsin()
    urls = G.get_urls(G.from_txt())
    print(urls)