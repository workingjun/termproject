import requests
from bs4 import BeautifulSoup

class coupang_search():
        def __init__(self, keyword, page_num):
                self.keyword = keyword
                self.page_num = page_num
                
        def request(self):
                header={
                        'User-Agent': (
                                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " 
                                "AppleWebKit/537.36 (KHTML, like Gecko) " 
                                "Chrome/121.0.0.0 Safari/537.36"
                                ),

                        "Accept-Language": "ko-KR,ko;q=0.9"
                        }
                
                base_url = "https://www.coupang.com/np/search"

                query_params = [
                f"q={self.keyword}",
                "channel=user",
                "component=",
                "eventCategory=SRP",
                "trcid=",
                "traid=",
                "sorter=scoreDesc",
                "minPrice=",
                "maxPrice=",
                "priceRange=",
                "filterType=",
                "listSize=36",
                "filter=",
                "isPriceRange=false",
                "brand=",
                "offerCondition=",
                "rating=0",
                f"page={self.page_num}",
                "rocketAll=false",
                "searchIndexingToken=1=9",
                "backgroundColor="
                ]

                coupang_url = f"{base_url}?" + "&".join(query_params)

                raw = requests.get(coupang_url, headers=header) 
                search = BeautifulSoup(raw.text, 'html.parser')
                return search
        
        def find_html(self):
                product_num = 1
                
                link_list, imageLink_list, title_list, price_list, point_list=[], [], [], [], [] 

                search = self.request()
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
                