import requests
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import threading
from get_asin import GetAsin

# options = ChromeOptions()
# options.add_argument('--user-data-dir=D:\chrome_new')
# browser = webdriver.Chrome(options=options)
# url = "https://www.amazon.com/dp/9178905931"
# # url = next(urls)
# browser.get(url)

# ## 更改成95001

# # browser.find_element_by_xpath('//*[@id="glow-ingress-line2"]').click()
# # time.sleep(1)
# # browser.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').send_keys("95001")
# # browser.find_element_by_xpath('//*[@id="GLUXZipUpdate"]/span/input').click()
# # time.sleep(1)
# # browser.find_element_by_xpath('//*[@id="a-popover-4"]/div/div[2]/span/span').click()

# ## 登录卖家精灵

# WebDriverWait(browser,20,0.5).until(EC.presence_of_element_located((By.ID,"main-sellersprite-extension")))
# browser.find_element_by_xpath('//*[@id="main-sellersprite-extension"]/div/div').click()
# try:
#     ## 如果要登录的话
#     browser.find_element_by_xpath('//*[@id="form_signin"]/div[1]/div[2]').click()
#     WebDriverWait(browser,20,0.1).until(EC.presence_of_element_located((By.XPATH,'//*[@id="form_signin"]/div[2]/div[1]/input')))
#     browser.find_element_by_xpath('//*[@id="form_signin"]/div[2]/div[1]/input').send_keys("hanyiyang03")
#     browser.find_element_by_xpath('//*[@id="form_signin"]/div[2]/div[2]/input').send_keys("hyy2018")
#     browser.find_element_by_xpath('//*[@id="form_signin"]/div[2]/button').click()
# except:
#     print("已经登陆")
#     # browser.find_element_by_xpath('//*[@id="ext-main-box"]/header/div/div/div').click()

# browser.find_element_by_xpath('//*[@id="content-ext-main"]/div/footer/div[1]/button[3]').click()





failurls = []


def spider(urls):
    options = ChromeOptions()
    options.add_argument('--user-data-dir=D:\chrome_new')
    browser = webdriver.Chrome(options=options)
    # url = "https://www.amazon.com/dp/9178905931"
    i = 1
    j = 0
    while True:
        url = next(urls)
        if url:
            if i == 1:
                browser.get(url)
                ## 更改成95001
                # browser.find_element_by_xpath('//*[@id="glow-ingress-line2"]').click()
                # time.sleep(1)
                # browser.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').send_keys("95001")
                # browser.find_element_by_xpath('//*[@id="GLUXZipUpdate"]/span/input').click()
                # time.sleep(1)
                # browser.find_element_by_xpath('//*[@id="a-popover-4"]/div/div[2]/span/span').click()

                i += 1

                WebDriverWait(browser,20,0.5).until(EC.presence_of_element_located((By.ID,"main-sellersprite-extension")))
                browser.find_element_by_xpath('//*[@id="main-sellersprite-extension"]/div/div').click()
                try:
                    ## 如果要登录的话
                    browser.find_element_by_xpath('//*[@id="form_signin"]/div[1]/div[2]').click()
                    WebDriverWait(browser,20,0.1).until(EC.presence_of_element_located((By.XPATH,'//*[@id="form_signin"]/div[2]/div[1]/input')))
                    browser.find_element_by_xpath('//*[@id="form_signin"]/div[2]/div[1]/input').send_keys("hanyiyang03")
                    browser.find_element_by_xpath('//*[@id="form_signin"]/div[2]/div[2]/input').send_keys("hyy2018")
                    browser.find_element_by_xpath('//*[@id="form_signin"]/div[2]/button').click()
                except:
                    print("已经登陆")
                    # browser.find_element_by_xpath('//*[@id="ext-main-box"]/header/div/div/div').click()
                # //*[@id="content-ext-main"]/div/footer/div[1]/button[3]/div[2]
                browser.find_element_by_xpath('//*[@id="content-ext-main"]/div/footer/div[1]/button[3]/div[1]').click()
                time.sleep(0.1)
                # WebDriverWait(browser,20,0.5).until(EC.presence_of_element_located((By.XPATH,'//div[@style="transform: translateX(-200%);"]')))
                # print(url+"下载完成")
            else:

            ## 登录卖家精灵
                js = "window.open('" + url + "')"
                browser.execute_script(js)
                toHandle = browser.window_handles
                browser.switch_to_window(toHandle[-1])
                WebDriverWait(browser,20,0.5).until(EC.presence_of_element_located((By.ID,"main-sellersprite-extension")))
                browser.find_element_by_xpath('//*[@id="main-sellersprite-extension"]/div/div').click()
                try:
                    ## 如果要登录的话
                    browser.find_element_by_xpath('//*[@id="form_signin"]/div[1]/div[2]').click()
                    WebDriverWait(browser,20,0.1).until(EC.presence_of_element_located((By.XPATH,'//*[@id="form_signin"]/div[2]/div[1]/input')))
                    browser.find_element_by_xpath('//*[@id="form_signin"]/div[2]/div[1]/input').send_keys("hanyiyang03")
                    browser.find_element_by_xpath('//*[@id="form_signin"]/div[2]/div[2]/input').send_keys("hyy2018")
                    browser.find_element_by_xpath('//*[@id="form_signin"]/div[2]/button').click()
                except:
                    print("已经登陆")
                    # browser.find_element_by_xpath('//*[@id="ext-main-box"]/header/div/div/div').click()
                # //*[@id="content-ext-main"]/div/footer/div[1]/button[3]/div[2]
                browser.find_element_by_xpath('//*[@id="content-ext-main"]/div/footer/div[1]/button[3]/div[1]').click()
                time.sleep(0.1)
                # WebDriverWait(browser,20,0.5).until(EC.presence_of_element_located((By.XPATH,'//div[@style="transform: translateX(-200%);"]')))
                # print(url+"下载完成")
                time.sleep(5)
            j += 1
            if j % 10 == 0:
                time.sleep(10)
        else:
            break
    # browser.quit()
# def loop(urls):
#     while True:
#         try:
#             with lock:
#                 url = next(urls)
#         except StopIteration:
#             break
#         try:
#             spider(url)
#         except:
#             failurls.append(url)
    

if __name__ == '__main__':
    G = GetAsin()
    urls = G.get_urls_yield(G.from_txt())
    spider(urls)
    # for i in range(0,thread_num):
    #     t = threading.Thread(target=loop,name="LoopThread %s" %i,args=(urls,))
    #     t.start()
    #     tsk.append(t)
    # for tt in tsk:
    #     tt.join()



    