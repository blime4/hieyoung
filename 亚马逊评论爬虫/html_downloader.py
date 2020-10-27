import requests
from requests import Timeout

class Downloader(object):
    def __init__(self):
        self.content_cache = {}
        self.request_session = requests.session()
        self.request_session.proxies
    
    def download(self,url,retry_count=3,headers=None,proxies=None,data=None):
        if url in self.content_cache:
            return self.content_cache.get(url)
        if headers:
            self.request_session.headers.update(headers)
        try:
            if data:
                content = self.request_session.post(url,data,proxies=proxies).content
            else:
                content = self.request_session.get(url,proxies=proxies).content
            content = content.decode("utf8","ignore")
            content = str(content)
            self.content_cache[url] = content
        except (ConnectionError,Timeout) as e:
            print('Downloader download ConnectionError or Timeout:' + str(e))
            content = None
            if retry_count> 0:
                self.download(url,retry_count-1,headers,proxies,data)
        except Exception as e:
            print('Downloader download Exception:' + e)
            content = None
        return content


if __name__ == '__main__':
    url = "https://www.amazon.com/dp/9178905931"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    }
    content = Downloader().download(url,headers=headers)
    print(content)