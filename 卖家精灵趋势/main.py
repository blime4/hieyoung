import requests
from lxml import etree
import csv


## 模拟登录
LoginUrl = "https://www.sellersprite.com/w/user/signin"
data = {
    'email': 'hanyiyang03',
    'password_otn': 'hyy2018',
    'password': '22df72bbd0d4000fba10b23b9fe97b95'

}

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
}

session = requests.Session()
resp = session.post(url=LoginUrl, data=data, headers=headers)

# format_url = "https://www.sellersprite.com/v2/keyword-miner?station=US&order.field=searches&order.desc=true&keywords=dog%20life%20jacket"
# format_url = "https://www.sellersprite.com/v2/keyword-miner?station=US&order.field=searches&order.desc=true&keywords="
format_url = "https://www.sellersprite.com/v2/keyword-miner?keywords=key_change&station=US&order.field=searches&order.desc=true&size=200"

keyword = "dog life jacket"
key_url = format_url.replace("key_change",keyword.replace(" ","+"))

response = session.get(key_url, headers=headers)
html = etree.HTML(response.text)

## 获取数据
trs = html.xpath('//*[@id="table-condition-search"]/tbody/tr')
columns = ['关键词','所属类目','月搜索趋势','旺季','月搜索量','月购买量','点击集中度','商品数','市场分析','PPC竞价']
with open("前两百条.csv","w",encoding='utf-8-sig',newline="") as f:
    writer = csv.writer(f,dialect="excel")
    writer.writerow(columns)
    for tr in trs[1:]:
        关键词 = [i.strip().replace("\n","") for i in tr.xpath('.//td[3]/div/a[1]/span/text()')][0]
        所属类目 = [i.strip().replace("\n","") for i in tr.xpath('.//td[4]/div/text()')]
        月搜索趋势 = tr.xpath('.//div[@class="morris-table-inline"]/@data-y')[0].replace(" ","").replace("\n","")[1:-1]
        旺季 = [i.strip().replace("\n","") for i in tr.xpath('.//td[6]/div/text()')]
        月搜索量 = [i.strip().replace("\n","") for i in tr.xpath('.//td[7]/div[1]/text()')]
        月购买量 = [i.strip().replace("\n","") for i in tr.xpath('.//td[8]/div[1]/span/text()')]
        点击集中度 = [i.strip().replace("\n","") for i in tr.xpath('.//td[9]/div/a/text()')]
        商品数 = [i.strip().replace("\n","") for i in tr.xpath('.//td[10]/div[1]/span/text()')]
        市场分析 = [i.strip().replace("\n","") for i in tr.xpath('.//td[11]/div[1]/a/text()')]
        PPC竞价 = [i.strip().replace("\n","") for i in tr.xpath('.//td[12]/div[1]/text()')]
        lst = [关键词,所属类目,月搜索趋势,旺季,月搜索量,月购买量,点击集中度,商品数,市场分析,PPC竞价]
        writer.writerow(lst)



