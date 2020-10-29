import http.client
import hashlib
import urllib
import random
import time
import json
import requests
from fake_useragent import UserAgent

class fy:
    def get(self,text):
        i = random.randint(1,3)
        if i == 1:
            return Baidu().get(text)
        if i == 2:
            return YouDao().get(text)
        if i == 3:
            return Google().get(text)

# 百度翻译

class Baidu:
    def __init__(self):
        print("用百度翻译")
        self.appid = '20170821000075622'  # 填写你的appid
        self.secretKey = 'eBnL61SbV_jhi9E0cHTS'  # 填写你的密钥
        self.httpClient = None
        self.myurl = '/api/trans/vip/translate'
        self.fromLang = 'auto'   #原文语种
        self.toLang = 'zh'   #译文语种
        self.salt = random.randint(32768, 65536)
        
    
    def get(self,text):
        self.text = text
        self.sign = self.appid + text + str(self.salt) + self.secretKey
        self.sign = hashlib.md5(self.sign.encode()).hexdigest()
        self.myurl = self.myurl + '?appid=' + self.appid + '&q=' + urllib.parse.quote(text) + '&from=' + self.fromLang + '&to=' + self.toLang + '&salt=' + str(self.salt) + '&sign=' + self.sign
        self.httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        self.httpClient.request('GET', self.myurl)

        # response是HTTPResponse对象
        response = self.httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        try:
            return result["trans_result"][0]['dst']
        except:
            YouDao().get(self.text)
            # time.sleep(1)
            # self.httpClient.request('GET', self.myurl)
            # # response是HTTPResponse对象
            # response = self.httpClient.getresponse()
            # result_all = response.read().decode("utf-8")
            # result = json.loads(result_all)
            # return result["trans_result"][0]['dst']


# 有道翻译
class YouDao:
    def __init__(self):
        print("用有道翻译")
        self.url = "http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i="
        self.headers = {
            'user_agent':UserAgent().Chrome
        }

    def get(self,text):
        response =  requests.get(self.url + text,headers=self.headers)
        try:
            return eval(response.text.strip())["translateResult"][0][0]["tgt"]
        except:
            Google().get(text)

## 谷歌翻译

class Google:
    def __init__(self):
        print("用谷歌翻译")
        self.url = "http://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=auto&tl=zh&q="
        self.headers = {
            'user_agent':UserAgent().Chrome
        }

    def get(self,text):
        response =  requests.get(self.url + text,headers=self.headers)
        try:
            return eval(response.text)["sentences"][0]["trans"]
        except:
            Baidu().get(text)



if __name__ == '__main__':
    i= "show me ,please !"
    # ans = YouDao().get("I have a plan")
    # print(Google().get(i))
    # print(ans)
    # print(YouDao().get(i))
    # while True:
    #     # print(BaiduTrans().get(i))
    #     ans = Google().get(i)
    #     print(ans)
