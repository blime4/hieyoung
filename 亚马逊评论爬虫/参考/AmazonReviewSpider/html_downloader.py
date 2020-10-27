import requests
from requests import Timeout

'''
http://docs.python-requests.org/en/master/
'''


class Downloader(object):
    def __init__(self):
        self.content_cache = {}
        self.request_session = requests.session()
        self.request_session.proxies

    def download(self, url, retry_count=3, headers=None, proxies=None, data=None):
        '''
        :param url: 准备下载的 URL 链接
        :param retry_count: 如果 url 下载失败重试次数
        :param headers: http header={'X':'x', 'X':'x'}
        :param proxies: 代理设置 proxies={"https": "http://12.112.122.12:3212"}
        :param data: 需要 urlencode(post_data) 的 POST 数据
        :return: 网页内容或者 None
        '''

        # 如果缓存里面有，直接返回
        if url in self.content_cache:
            # 　print("缓存里面有，直接返回")
            return self.content_cache.get(url)

        if headers:
            self.request_session.headers.update(headers)
        try:
            #print("Downloader downloading the page...")
            if data:
                content = self.request_session.post(url, data, proxies=proxies).content
            else:
                content = self.request_session.get(url, proxies=proxies).content
            content = content.decode('utf8', 'ignore')
            content = str(content)
            # print("url加入缓存-> url=" + url)
            self.content_cache[url] = content
        except (ConnectionError, Timeout) as e:
            print('Downloader download ConnectionError or Timeout:' + str(e))
            content = None
            if retry_count > 0:
                self.download(url, retry_count - 1, headers, proxies, data)
        except Exception as e:
            print('Downloader download Exception:' + e)
            content = None
        return content


if __name__ == '__main__':
    # pass
    url = "https://www.amazon.co.uk/Monitor-Transmission-Lullabies-Temperature-Monitoring/product-reviews/B01HXPQUUI/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    content = Downloader().download(url)
    content2 = Downloader().download(url, retry_count=2)
    print(str(content2))
