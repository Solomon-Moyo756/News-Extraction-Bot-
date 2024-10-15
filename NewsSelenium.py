from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class NewsSelenium:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()

    def open_news_site(self):
        # Open the specified news site URL
        self.driver.get(self.url)

    def find_element_by_xpath(self, xpath_value):
        # Find an element using the given XPath value
        result = self.driver.find_element(by=By.XPATH, value=xpath_value)
        return result

    def find_element_by_name(self, name_value):
        # Find an element using the name value
        result = self.driver.find_element(by=By.NAME, value=name_value)
        return result
    
    def find_element_by_class_name(self,class_name_value):
        result = self.driver.find_element(by=By.CLASS_NAME,value=class_name_value)
        return result
    
    def extract_text_from_element(self,element):
        return element.text if element else ""
    
    def scroll_page_until_element(self, xpath_value):
        # scroll pqge to load other elements
        target_element = self.find_element_by_xpath(xpath_value=xpath_value)
        if target_element:
            self.driver.execute_script("arguments[0].scrollIntoView();", target_element)
        else:
            print(f"Could not find the element with XPath '{xpath_value}' to scroll to.")

    

    def close_browser(self):
        # Close the browser session
        self.driver.quit()
