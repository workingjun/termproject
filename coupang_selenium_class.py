from selenium.webdriver.common.by import By

class SearchManager:
    def __init__(self, driver):
        self.driver = driver
        self.location = "arguments[0].scrollIntoView({ behavior: 'auto', block: 'center', inline: 'center' });"
        self.url = 'https://www.coupang.com'

    def Loading_Options(self):
        """
        This part is Loading options of Searching options
        This just needs when the webpage reloading or you clicking Options.

        This is a part that cannot be left out.       
        """

        xpath = "//div[contains(@class, 'search-filter-options search-')]"
        elems = self.driver.find_elements(By.XPATH, xpath)

        return elems

    def page_source(self):
        # Gets the source of the current page.  
        return self.driver.page_source
    
###############################################################################################################

class Setting_Options(SearchManager):
    def getting_keyword(self, keyword):
        """
        This is a part that get the keyword for searching
        Give the keyword in, you could searching shopping list. 
        """

        self.driver.get(self.url)

        xpath='//*[@id="headerSearchKeyword"]'
        self.driver.find_element(By.XPATH, xpath).send_keys(keyword)
        self.driver.find_element(By.XPATH, xpath).send_keys("\n")

    def Click_option(self, option_name = None, option_item_name = None):
        """
        If the "option_name" and 'option_item_num' are None, 
        click all more view options.

        If the "option_name" and 'option_item_num' are not None, 
        click more view option of those and click item label that you want to do.    
        """

        elems = self.Loading_Options()

        if option_item_name is None:
            if option_name is None:
                for i in range(4, len(elems)-2):
                    try:
                        self.driver.execute_script(self.location, elems[i])
                        elems[i].find_element(By.TAG_NAME, 'span').click()

                    except:
                        continue
            else:
                option_num, _ = self.find_index_of_Options(option_name)
                self.driver.execute_script(self.location, elems[option_num])
                elems[option_num].find_element(By.TAG_NAME, 'span').click()
        else:
            option_num, _ = self.find_index_of_Options(option_name)

            try:
                more_view_elem = elems[option_num].find_element(By.TAG_NAME, 'span')
                if more_view_elem.get_attribute("style") != 'opacity: 1;':
                    self.driver.execute_script(self.location, elems[option_num])
                    more_view_elem.click()
            except:
                pass
            
            finally:
                option_num, option_item_num = self.find_index_of_Options(option_name, option_item_name)

                elems_option1 = elems[option_num].find_elements(By.TAG_NAME, 'li')
                self.driver.execute_script(self.location, elems_option1[option_item_num])
                elems_option1[option_item_num].click()    
                    
    def setting_Price(self, minPrice, maxPrice):
        # Set the mininum price and Maximum price that you wnant directly.
         
        elems = self.Loading_Options()
        index, _ = self.find_index_of_Options("가격")

        xpath = "//input[@title='minPrice']"
        elems[index].find_element(By.XPATH, xpath).send_keys(str(minPrice))

        xpath = "//input[@title='maxPrice']"
        elems[index].find_element(By.XPATH, xpath).send_keys(str(maxPrice))

        xpath = '//*[@id="searchPriceFilter"]/div/a'
        elems[index].find_element(By.XPATH, xpath).click()

    def print_Option_names(self):
            
        """
        You can print elements in options before you click.
        
        For clicking, you would need to print all option.
        So, this part is that you get infromations of Searching options in coupang site.
        
        Clicking elements is concluded in the method name "Click_option".
        """ 
        text_list = self.Save_Options()

        for text in text_list:
            print(text[0])
        
    def print_Option_items(self, option_name):
        try:
            self.Click_option(option_name)

        except:
            pass

        finally:
            option_num, _ = self.find_index_of_Options(option_name)
            text_list = self.Save_Options()
            
            for text in text_list[option_num - 4]:
                print(text)

    def Save_Options(self):
        # This function returns texts of all options you need.

        elems = self.Loading_Options()
        texts = [elem.text.split('\n') for elem in elems[4:]]
        text_list = []

        for i, text in enumerate(texts, start = 4):
            if text[-1] in ["닫기", "더보기"]:
                text.pop()
            if text[-1] == "검색":
                text.pop()
            if text[-1].endswith("~ 원"):
                text.pop()
            
            text_list.append(text)

        return text_list

    def find_index_of_Options(self, option_name, option_item_name = None):
        """
        This is a part that find the index of clicking Options.
        If you search "laptop", you can find many options, such as "Storage Capacity", "CPU" and "RAM Capacity".   
        """

        text_list = self.Save_Options()

        option_num = None
        option_item_num = None

        for i in range(len(text_list)):
            if text_list[i][0]==option_name:
                option_num = i + 4
                for j in range(len(text_list[i])):        
                    if text_list[i][j]==option_item_name:
                        option_item_num = j - 1
                        break
                if option_item_num is not None:
                    break

        return option_num, option_item_num  