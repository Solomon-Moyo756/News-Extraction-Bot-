from selenium import webdriver
from selenium.webdriver.common.by import By
from NewsSelenium import NewsSelenium
from Article import NewsArticle
import time

class NewsExtractor:

    

    def __init__(self) -> None:
        self.articles = []
        self.bot = NewsSelenium("https://gothamist.com/")
        self.xpath_donate_popup = '//*[@id="om-gjymukk0gyrewa6wabuz-yesno"]/div/button'
        self.title_identifier = "h2" # search by class
        self.description_identifier = "" # search by ????
        self.date_identifier = "" # search by ????
        self.image_identifier = "" # search by ????
        self.bot.open_news_site()
        self.close_popup()
        time.sleep(2)
        self.extract_news()
    
    # close the possible pop up that is revealed on the landing page
    def close_popup(self):
        self.bot.wait_for_element(xpath_value=self.xpath_donate_popup)
        self.bot.close_popup(popup_xpath=self.xpath_donate_popup)

    ### this function is responsible for extracting all the news articles and saving the required details to the array of News Article object
    def extract_news(self):
        elements = self.bot.find_all_elements_by_class_name("h2")
        for a in elements:
            title = self.bot.extract_text_from_element(a)
            article = NewsArticle(
                title=title,
                description= "descr",
                date= "10/10/2000",
                picture_filepath="path/abcsd",
                count_of_search_phrases=3,
                is_money_mentioned=False
                )
            
            self.articles.append(article)

            # TODO: I realized some articles do not have enough information and might require me to enter inside the article and scan for appropriate infromation

    def get_resultant_articles(self):
        return self.articles

