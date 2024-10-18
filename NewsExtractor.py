from selenium import webdriver
from selenium.webdriver.common.by import By
from NewsSelenium import NewsSelenium
from Article import NewsArticle
import time
from ElementIdentifiers import Identifier

class NewsExtractor:

    

    def __init__(self,search_value) -> None:
        self.articles = []
        self.bot = NewsSelenium("https://gothamist.com/")

        self.bot.open_news_site()
        self.bot.wait_for_element(timeout=10,xpath_value=Identifier.donate_popup_xpath)
        self.bot.close_popup(popup_xpath=Identifier.donate_popup_xpath)
        time.sleep(2)
        self.search_phrase(search_value)
        #time.sleep(2)
        self.bot.wait_for_search_results(Identifier.css_selector_each_news_article_card)
        self.extract_news()
    
 

    def search_phrase(self,search_phrase_value):
        #find the search I con and cclick it
        self.bot.wait_for_element(timeout=10,xpath_value=Identifier.search_icon_xpath)
        search_icon =self.bot.find_element_by_xpath(xpath_value= Identifier.search_icon_xpath)
        search_icon.click()# this leads to the search page
        #search for the given search phrase
        time.sleep(1)
        self.bot.wait_for_element(timeout=10,xpath_value=Identifier.search_input_xpath)
        search_input = self.bot.find_element_by_xpath(xpath_value= Identifier.search_input_xpath)
        search_input.clear()
        search_input.send_keys(search_phrase_value)
        time.sleep(1)
        self.bot.wait_for_element(timeout=10,xpath_value=Identifier.search_submit_button_xpath)
        search_submit_button = self.bot.find_element_by_xpath(xpath_value= Identifier.search_submit_button_xpath)
        search_submit_button.click()

    ### this function is responsible for extracting all the news articles and saving the required details to the array of News Article object
    def extract_news(self):
        articles = self.bot.find_all_elements_by_css_selector(Identifier.css_selector_each_news_article_card)
        count = 0
        for a in articles:
            print("extracting...")
            try:
                #print(f"{a.text} \n\n")
                title = self.bot.find_element_by_class_name_from_element(from_element= a,class_name_value= Identifier.title_class_name).text
                time.sleep(1)
                by_line = self.bot.find_element_by_class_name_from_element(from_element= a, class_name_value=Identifier.by_line_class_name).text # card slot includes the write of this article
                try:
                    description = self.bot.find_element_by_class_name_from_element(from_element= a,class_name_value= Identifier.description_class_name).text
                    count=count+1
                    print(count)
                except Exception as no_descr:
                    # If no description is found, handle this exception
                    description = "No description available"
                try:

                    date_published = self.bot.find_element_by_class_name_from_element(from_element= a, class_name_value=Identifier.date_class_name).text.split('\n')
                except Exception as date_not_found:
                    date_published = "date not found"

                try:
                    image_element = self.bot.find_element_by_xpath_from_element(from_element= a, xpath_value=Identifier.image_xpath)
                    print(image_element)
                    picture_filepath = image_element.get_attribute('src')
                except Exception as image_not_found:
                    picture_filepath = "no image path found"
                #description = self.bot.find_element_by_xpath_from_element(from_element= card_slot, xpath_value='.//p[@class="desc"]').text
                article = NewsArticle(
                    title =title,
                    description = description,
                    date = date_published,
                    picture_filepath = picture_filepath,
                    count_of_search_phrases = 3,
                    is_money_mentioned = False
                    )
                
                self.articles.append(article)

                
            except Exception as e:
                print(f"Error extracting data from an article: {e}")

            # TODO: I realized some articles do not have enough information and might require me to enter inside the article and scan for appropriate infromation

    def get_resultant_articles(self):
        return self.articles

