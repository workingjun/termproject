from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup   
import math

class Searching_blog():
    def __init__(self, driver, content=50):
        self.driver = driver
        self.content = content
               
    def Saerch_and_Scroll(self, query):
        self.driver.get('http://www.naver.com')  

        element = self.driver.find_element(By.ID, 'query')
        element.send_keys(query)
        element.send_keys("\n")

        self.driver.find_element(By.LINK_TEXT,'블로그').click( )

        self.scroll_down()

    def find_html(self):
        username_list, blog_title_list, content_list = [], [], []
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
                blog_title_list.append(title)

                #게시글 내용
                content = i.find('div','dsc_area').get_text()         
                content_list.append(content)
                
                no += 1
                if no > self.content :
                    break

        return username_list, blog_title_list, content_list

    def scroll_down(self):
        page_cnt = math.ceil(self.content / 30)
        
        i = 1
        while i <= page_cnt:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            i += 1

