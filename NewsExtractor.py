from selenium import webdriver
from selenium.webdriver.common.by import By
from NewsSelenium import NewsSelenium
from Article import NewsArticle
import time
from ElementIdentifiers import Identifier
import logging
import re
import os
from openpyxl import Workbook
import requests
import string
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NewsExtractor:

    

    def __init__(self,search_value) -> None:
        self.logger = logging.getLogger(__name__)
        self.articles = []
        self.bot = NewsSelenium("https://gothamist.com/")
        self.search_value = search_value
        self.bot.open_news_site()
        self.bot.wait_for_element(timeout=10,xpath_value=Identifier.donate_popup_xpath)
        self.bot.close_popup(popup_xpath=Identifier.donate_popup_xpath)
        time.sleep(2)
        self.search_the_phrase(self.search_value)
        #time.sleep(2)
        print("waiting for articles results...")
        time.sleep(5)
        self.bot.wait_for_search_results(Identifier.css_selector_each_news_article_card)
        self.extract_news()
    
 

    def search_the_phrase(self,search_phrase_value):
        #find the search I con and cclick it
        self.bot.wait_for_control_room_overlay_to_disappear()
        self.bot.wait_for_element(timeout=10,xpath_value=Identifier.search_icon_xpath)
        try:
            #try this action and repeat it once if it fails
            search_icon = self.bot.find_element_by_xpath(xpath_value= Identifier.search_icon_xpath)
            self.bot.click_using_js(search_icon)
            print("search icon found")
        except Exception as e:
            print("trying again...")
            search_icon = self.bot.find_element_by_xpath(xpath_value= Identifier.search_icon_xpath)
            self.bot.click_using_js(search_icon)
        #search for the given search phrase
        time.sleep(1)
        self.bot.wait_for_control_room_overlay_to_disappear()
        self.bot.wait_for_element(timeout=10,xpath_value=Identifier.search_input_xpath)
        try:
            search_input = self.bot.find_element_by_xpath(xpath_value= Identifier.search_input_xpath)
            self.bot.input_search_phrase(search_input_element=search_input,search_phrase_value=search_phrase_value)
        except Exception as e:
            print("trying again...")
            search_input = self.bot.find_element_by_xpath(xpath_value= Identifier.search_input_xpath)
            search_input.send_keys(search_phrase_value)
            self.bot.input_search_phrase(search_input_element=search_input,search_phrase_value=search_phrase_value)
        time.sleep(2)
        self.bot.wait_for_element(timeout=10,xpath_value=Identifier.search_submit_button_xpath)
        try:
            search_submit_button = self.bot.find_element_by_xpath(xpath_value= Identifier.search_submit_button_xpath)
            self.bot.click_using_js(search_submit_button)
            print("seaccrhing ...")
        except Exception as e:
            print("trying again...")
            search_submit_button = self.bot.find_element_by_xpath(xpath_value= Identifier.search_submit_button_xpath)
            self.bot.click_using_js(search_submit_button)

    ### this function is responsible for extracting all the news articles and saving the required details to the array of News Article object
    def extract_news(self):
        articles = self.bot.find_all_elements_by_css_selector(Identifier.css_selector_each_news_article_card)
        # get the number of search results 
        search_results_element = self.bot.find_element_by_css_selector(css_selector_value=Identifier.num_search_results_css_selector)
        search_results_text = self.bot.find_text_from_element(search_results_element)
        num_search_results = int(search_results_text.split()[0])
        print(f"{search_results_text}: {self.search_value}")
        # check if all the news articles have been loaded, load more from the search results
        while len(articles)<num_search_results:
            #click the load more button
            load_more_button = self.bot.find_element_by_xpath(xpath_value=Identifier.load_more_button_xpath)
            self.bot.click_using_js(element=load_more_button)
            self.bot.wait_for_search_results(css_selector=Identifier.css_selector_each_news_article_card)
            articles = self.bot.find_all_elements_by_css_selector(Identifier.css_selector_each_news_article_card)
            continue
        count = 0
        
        for a in articles:
            print("extracting...")
            self.bot.wait_for_control_room_overlay_to_disappear()
            # check for the subscribe now pop up and close it if it is there
            try:
                self.bot.wait_for_element(timeout=2,xpath_value=Identifier.subscribe_pop_up_xpath)
                subscribe_pop_up_close_button = self.bot.find_element_by_xpath(xpath_value= Identifier.subscribe_pop_up_xpath)
                subscribe_pop_up_close_button.click()
            except Exception as e:
                #self.logger.error(f"close 'subscribe pop up' button not found: {e}")
                print("subscribe pop up not found.. continue.")

            try:
                #print(f"{a.text} \n\n")
                title_element = self.bot.find_element_by_class_name_from_element(from_element= a,class_name_value= Identifier.title_class_name)
                title = self.bot.find_text_from_element(title_element)
                time.sleep(1)
                by_line = self.bot.find_element_by_class_name_from_element(from_element= a, class_name_value=Identifier.by_line_class_name) # card slot includes the write of this article
                try:
                    description_element = self.bot.find_element_by_class_name_from_element(from_element= a,class_name_value= Identifier.description_class_name)
                    description = self.bot.find_text_from_element(description_element)
                    count=count+1
                    print(count)
                except Exception as no_descr:
                    # If no description is found, handle this exception
                    description = "No description available"
                    #self.logger.error(f"No description available{no_descr}")
                try:

                    date_published_element = self.bot.find_element_by_class_name_from_element(from_element= a, class_name_value=Identifier.date_class_name)
                    date_published = self.bot.find_text_from_element(date_published_element).split('\n')
                except Exception as date_not_found:
                    date_published = "date not found"
                    #self.logger.error(f"date not found {date_not_found}")

                try:
                    image_element = self.bot.find_element_by_css_selector_from_element(from_element= a, css_selector_value=Identifier.image_css_selector)
                    picture_filepath = self.bot.get_element_attribute(element=image_element,attribute_name='src')
                except Exception as image_not_found:
                    picture_filepath = "no image path found"
                    #self.logger.error(f"no image path found {image_not_found}")

                count_phrases = self.count_search_phrase(title=title,description=description)
                is_money_mentioned = self.search_for_money(title=title, description=description)
                article = NewsArticle(
                    title =title,
                    description = description,
                    date = date_published,
                    picture_filepath = picture_filepath,
                    count_of_search_phrases = count_phrases,
                    is_money_mentioned = is_money_mentioned
                    )
                
                self.articles.append(article)

                
            except Exception as e:
                self.logger.error(f"Error extracting article: {e}")

            # TODO: I realized some articles do not have enough information and might require me to enter inside the article and scan for appropriate infromation

    def get_resultant_articles(self):
        return self.articles
    
    def search_for_money(self, title, description):
        money_pattern = r'(\$|dollars|USD)\b'
        match_desc = re.search(money_pattern, description, re.IGNORECASE)
        match_title = re.search(money_pattern, title, re.IGNORECASE)
        if match_desc or match_title:
            return True
        else:
            return False

    def count_search_phrase(self,title, description):
        arr_description_words = description.lower().split()
        arr_title_words = title.lower().split()

        count = 0
        count += sum(1 for word in arr_description_words if self.search_value.lower() in word)
        count += sum(1 for word in arr_title_words if self.search_value.lower() in word)
        
        return count
    def save_to_excel(self,data):
        # Convert the data to a DataFrame
        # Create a new workbook and select the active worksheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Articles"

        ws.append(["Title", "Description", "Date","image name","count_of_search_phrases","is_money_mentioned"])
        # Write the data (articles) to the excel file
        count = 0
        output_dir = os.path.join(os.getcwd(), "output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for article in data:
            count+=1
            is_money_mentioned = "No"
            if article.is_money_mentioned == True:
                is_money_mentioned = "Yes"
            
            image_name = generate_image_name(article.title)
            row = [article.title,article.description,article.date,image_name,article.count_of_search_phrases,is_money_mentioned]
            ws.append(row)
            print(f"{article.title} saved successfully!")
            # download the image
            download_article_photo(article.picture_filepath,image_name=f'{output_dir}//{image_name}')
        # Save the workbook to an output folder
        wb.save(os.path.join(output_dir, "articles.xlsx"))
        print("Excel file created successfully!")


def download_article_photo(image_url,image_name):
    print(f"image url: {image_url}")
    response = requests.get(image_url) # send a get request to the image url
    # check if the response was a successful one
    if response.status_code == 200:
        
        with open(f"{image_name}.webp", "wb") as file:
            file.write(response.content)
        print(f"Image downloaded successfully! name: {image_name}")
    else:
        print(f"Failed to download image {image_name}. Status code:", response.status_code)

def sanitize_filename(title):
    # Remove any characters that are not valid in filenames
    title = re.sub(r'[<>:"/\\|?*]', '', title)  # Remove invalid characters
    title = title.replace(' ', '_')  # Replace spaces with underscores
    return title

def trim_title(title, max_words):
    # Split the title into words and take only the first 'max_words' words
    words = title.split()
    trimmed_title = ' '.join(words[:max_words])  # Join the first max_words words
    return trimmed_title

def generate_random_suffix(length=6):
    # Generate a random suffix of a specified length
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_image_name(title):
    trimmed_title = trim_title(title=title, max_words=15)
    sanitized_title = sanitize_filename(trimmed_title)
    random_suffix = generate_random_suffix()
    resultant_title = f"{sanitized_title}_{random_suffix}"
    return resultant_title
