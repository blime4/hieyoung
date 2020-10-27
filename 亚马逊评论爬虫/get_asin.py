import os

class get_asin:
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

if __name__ == "__main__":
    asin = get_asin().from_txt()