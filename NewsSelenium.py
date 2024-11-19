from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import logging
import time

class NewsSelenium:
    def __init__(self, url):
        self.logger = logging.getLogger(__name__)
        self.url = url
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
        chrome_options.add_argument("--no-sandbox")  # Needed for cloud environments
        chrome_options.add_argument("--disable-dev-shm-usage")  # Avoid /dev/shm issues
        service = Service() 
        self.driver = webdriver.Chrome(service=service, options=chrome_options)


    def open_news_site(self):
        # Open the specified news site URL
        self.driver.get(f"{self.url}")
        self.driver.maximize_window()

    def find_element_by_xpath(self, xpath_value):
        # Find an element using the given XPath value
        result = self.driver.find_element(by=By.XPATH, value=xpath_value)
        return result
    
    def find_element_by_css_selector(self, css_selector_value):
        result = self.driver.find_element(by=By.CSS_SELECTOR,value=css_selector_value)
        return result

    def find_element_by_name(self, name_value):
        # Find an element using the name value
        result = self.driver.find_element(by=By.NAME, value=name_value)
        return result

    def find_element_by_class_name_from_element(self,from_element, class_name_value):
        # this function finds element by class name  from a given element, finding an element in another element
        result = self.driver.execute_script(f'return arguments[0].querySelector(".{class_name_value}")', from_element)
        return result
    
    def find_element_by_xpath_from_element(self,from_element, xpath_value):
        # this function finds element by xpath name  from a given element, finding an element in another element
        result = from_element.find_element(by=By.XPATH,value=xpath_value)
        return result
    
    def find_element_by_css_selector_from_element(self,from_element, css_selector_value):
        # this function finds element by xpath name  from a given element, finding an element in another element
        result = self.driver.execute_script(f'return arguments[0].querySelector("{css_selector_value}")', from_element)
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
        
        print(f"{len(elements)} elements found" )
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
    def wait_for_search_results(self,css_selector):
        # Wait until at least one article is present
        try:

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector))
            )
        except Exception as e:
            print(f"Element with css_selector '{css_selector}' not found: {e}")
            return None
    
    def wait_for_control_room_overlay_to_disappear(self):
        # Wait for the overlay to disappear
        try:
            WebDriverWait(self.driver , 10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "fc-dialog-overlay")))
            print(f"Element with css_selector fc-dialog-overlay was found")
        except Exception as e:
            print(f"Element with css_selector fc-dialog-overlay not found: {e}")
            return None

    def close_browser(self):
        # Close the browser session
        self.driver.quit()

    def click_using_js(self,element):
        self.driver.execute_script("arguments[0].click();", element)

    def input_search_phrase(self, search_input_element, search_phrase_value):
        # Use JavaScript to set the value of the input element
        self.driver.execute_script("""
            var inputElement = arguments[0];
            var value = arguments[1];
            inputElement.value = value;
            // Trigger the input event to simulate typing
            var event = new Event('input', { 'bubbles': true, 'cancelable': true });
            inputElement.dispatchEvent(event);
        """, search_input_element, search_phrase_value)

    def find_text_from_element(self,a):
        element_text = self.driver.execute_script('return arguments[0].textContent;', a)
        return element_text
    def get_element_attribute(self,element,attribute_name):
        # get an attribute from an element
        attribute = self.driver.execute_script(f"return arguments[0].getAttribute('{attribute_name}');", element)
        return attribute
        
