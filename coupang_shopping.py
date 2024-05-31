import requests
from bs4 import BeautifulSoup

class Shopping():
    def __init__(self, raw, page_num):
        self.raw = raw
        self.page_num = page_num
        
    def getting_page_source(self):
        search = BeautifulSoup(self.raw, 'html.parser')
        return search
    
    def find_html(self):
        product_num = 1
        
        link_list, imageLink_list, title_list, price_list, point_list=[], [], [], [], [] 

        search = self.getting_page_source()
        box = search.find('ul', {'id' : 'productList'})
        all_product = box.find_all('li', {'class': 'search-product'})

        for i, product in enumerate(all_product):
                imagefind = product.find("img", {'class' : 'search-product-wrap-img'})
                if imagefind.get("data-img-src") is None:
                        imageLink = "http:" + imagefind.get('src')
                else:
                        imageLink = "http:" + imagefind.get("data-img-src")

                title = product.find('div', {'class' : 'name'})
                price = product.find('strong', {'class' : 'price-value'})
                point = product.find('span', {'class' : 'rating-total-count'})
                
                if point is None:
                        point=''

                link2 = product.find('a')['href']
                link = "https://www.coupang.com" + link2

                imageLink_list.append(imageLink)
                
                title_text = f"{product_num}. {title.text.strip()}"

                title_list.append(title_text)
                price_list.append(price.text)

                if isinstance(point, str):
                        point_list.append(point)
                else:
                        point_list.append(point.text)
                
                link_list.append(link)    

                product_num += 1

        return link_list, imageLink_list, title_list, price_list, point_list
        

