from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup   
import chromedriver_autoinstaller
import time
import math

class blog_search():
    def __init__(self, query_txt, cnt, driver):
        self.query_txt = query_txt
        self.cnt = cnt
        self.page_cnt = math.ceil(cnt / 30)
        self.driver = driver

    def saerch_and_scroll(self):
        self.driver.get('http://www.naver.com')
        time.sleep(2)

        element = self.driver.find_element(By.ID, 'query')
        element.send_keys(self.query_txt)
        element.send_keys("\n")

        self.driver.find_element(By.LINK_TEXT,'블로그').click( )

        self.scroll_down()

    def request_find_html(self):
        username_list, title_list, content_list = [], [], []
        no = 1

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        view_list = soup.find("ul", "lst_view _fe_view_infinite_scroll_append_target")

        for i in view_list:
            try:
                contents = i.find('div','view_wrap').find_all('div')
            except :
                continue
            else :
                # 블로그 주인 닉네임 추출
                username = i.find('div','user_info').find('a').get_text()
                username_list.append(username)

                #게시글 제목
                title= i.find('div','title_area').find('a').get_text()
                title_list.append(title)

                #게시글 내용
                content = i.find('div','dsc_area').get_text()         
                content_list.append(content)
                
                no += 1
                if no > self.cnt :
                    break

            time.sleep(0.5)   

        return username_list, title_list, content_list

    def scroll_down(self):
        i = 1
        while i <= self.page_cnt:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(3)
            i += 1

