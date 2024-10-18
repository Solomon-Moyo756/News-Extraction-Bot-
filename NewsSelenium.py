from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

class NewsSelenium:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()

    def open_news_site(self):
        # Open the specified news site URL
        self.driver.get(self.url)
        self.driver.maximize_window()

    def find_element_by_xpath(self, xpath_value):
        # Find an element using the given XPath value
        result = self.driver.find_element(by=By.XPATH, value=xpath_value)
        return result

    def find_element_by_name(self, name_value):
        # Find an element using the name value
        result = self.driver.find_element(by=By.NAME, value=name_value)
        return result

    def find_element_by_class_name_from_element(self,from_element, class_name_value):
        # this function finds element by class name  from a given element, finding an element in another element
        result = from_element.find_element(by=By.CLASS_NAME,value=class_name_value)
        return result
    
    def find_element_by_xpath_from_element(self,from_element, xpath_value):
        # this function finds element by xpath name  from a given element, finding an element in another element
        result = from_element.find_element(by=By.XPATH,value=xpath_value)
        return result
    
    def find_element_by_css_selector_from_element(self,from_element, css_selector_value):
        # this function finds element by xpath name  from a given element, finding an element in another element
        result = from_element.find_element(by=By.CSS_SELECTOR,value=css_selector_value)
        return result

    
    def find_element_by_class_name(self,class_name_value):
        result = self.driver.find_element(by=By.CLASS_NAME,value=class_name_value)
        return result
    
    
    def find_all_elements_by_class_name(self,class_name):
        elements = self.driver.find_elements(by=By.CLASS_NAME, value=class_name)
        return elements

    def find_all_elements_by_css_selector(self, css_selector):
        print(f"finding by css selector...{css_selector}")
        
        elements = self.driver.find_elements(by= By.CSS_SELECTOR, value= css_selector)
        #articles =  self.driver.find_elements(By.CSS_SELECTOR, '.v-card.gothamist-card')
        print(len(elements))
        #print(articles)
        return elements

    
    def extract_text_from_element(self,element):
        return element.text if element else ""
    
    def scroll_page_until_element(self, xpath_value):
        # scroll pqge to load other elements
        target_element = self.find_element_by_xpath(xpath_value=xpath_value)
        if target_element:
            self.driver.execute_script("arguments[0].scrollIntoView();", target_element)
        else:
            print(f"Could not find the element with XPath '{xpath_value}' to scroll to.")

    def close_popup(self, popup_xpath):
        try:
            popup = self.find_element_by_xpath(popup_xpath)
            if popup:
                popup.click()
        except Exception as e:
            print(f"Popup close button not found: {e}")

    def wait_for_element(self, xpath_value, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath_value)))
        except Exception as e:
            print(f"Element with XPath '{xpath_value}' not found: {e}")
            return None


    def close_browser(self):
        # Close the browser session
        self.driver.quit()
