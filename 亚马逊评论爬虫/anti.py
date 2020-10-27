import random

# 反爬虫

class anti:
    def __init__(self):
        self.uas = []
        with open("UserAgent.txt") as f:
            self.uas = f.readlines()

    def get_user_agent(self):
        cnt = random.randint(0,len(self.uas)-1)
        return self.uas[cnt].replace("\n","")

    def get_headers(self,referer):
        headers = {
            'Referer': referer,
            'User-agent':self.get_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accetp-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8'
        }
        return headers
    

if __name__ == '__main__':
    pass
    # urlPart1 = "http://www.amazon.com/product-reviews/"
    # urlPart2 = "/?ie=UTF8&reviewerType=all_reviews&pageNumber="
    # asin = "9178905931"
    # referer = urlPart1 + asin + urlPart2 + "1"
    # anti = anti()
    # headers= anti.get_headers(referer)
    # print(headers)
