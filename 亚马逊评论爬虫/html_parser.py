from lxml import etree
from html_downloader import Downloader
from fake_useragent import UserAgent

class htmlparser(object):
    def __init__(self,base_url):
        self.amazon_base_url = base_url
    
    # https://www.amazon.com/dp/9178905931
    def parse_main_page_reviews_url(self,content):
        content = str(content)
        html = etree.HTML(content)
        subject = html.xpath('//a[@data-hook="see-all-reviews-link-foot"]')
        a_href = subject[0].get('href')
        return self.amazon_base_url + a_href
    
    def get_next_reviews_url(self, content):
        content = str(content)
        html = etree.HTML(content)
        subject = html.xpath('//li[@class="a-last"]/a')
        if len(subject) == 0:
            return ""
        a_href = subject[0].get('href')
        return self.amazon_base_url + a_href
    
    def get_reviews_info(self, content):
        content = str(content)
        content = content.replace("<br>","")
        content = content.replace("<br />","")
        html = etree.HTML(content)

        star_list = html.xpath('//i[@data-hook="review-star-rating"]/span/text()')   
        title_list = html.xpath('//a[@data-hook="review-title"]/span/text()')
        
        review_body_list = html.xpath('//span[@data-hook="review-body"]')

        all_review_list = []
        for i in range(len(star_list)):
            star_num = star_list[i][:1]
            all_review_list.append(
                {
                    "star":star_num,
                    "title": title_list[i],
                    "body": review_body_list[i]
                }
            )
        return all_review_list

if __name__ == '__main__':


    downloader = Downloader()
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
    }
    url = "https://www.amazon.com/dp/9178905931"
    content2 = downloader.download(url, retry_count=2)
    # content2 = downloader.download(url, retry_count=2, headers=headers).decode('utf8')
    print(htmlparser("https://www.amazon.com").parse_main_page_reviews_url(content2))