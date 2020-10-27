import http.client
import hashlib
import urllib
import random
import time
import json

class BaiduTrans:
    def __init__(self):
        self.appid = '20170821000075622'  # 填写你的appid
        self.secretKey = 'eBnL61SbV_jhi9E0cHTS'  # 填写你的密钥
        self.httpClient = None
        self.myurl = '/api/trans/vip/translate'
        self.fromLang = 'auto'   #原文语种
        self.toLang = 'zh'   #译文语种
        self.salt = random.randint(32768, 65536)
        
    
    def get(self,text):
        self.sign = self.appid + text + str(self.salt) + self.secretKey
        self.sign = hashlib.md5(self.sign.encode()).hexdigest()
        self.myurl = self.myurl + '?appid=' + self.appid + '&q=' + urllib.parse.quote(text) + '&from=' + self.fromLang + '&to=' + self.toLang + '&salt=' + str(self.salt) + '&sign=' + self.sign
        try:
            self.httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            self.httpClient.request('GET', self.myurl)

            # response是HTTPResponse对象
            response = self.httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            try:
                return result["trans_result"][0]['dst']
            except:
                time.sleep(1)
                self.httpClient.request('GET', self.myurl)
                # response是HTTPResponse对象
                response = self.httpClient.getresponse()
                result_all = response.read().decode("utf-8")
                result = json.loads(result_all)
                return result["trans_result"][0]['dst']

        except Exception as e:
            print (e)
        # finally:
        #     if self.httpClient:
        #         self.httpClient.close()

if __name__ == '__main__':
    i= "show me ,please !"
    # while True:
    #     print(BaiduTrans().get(i))