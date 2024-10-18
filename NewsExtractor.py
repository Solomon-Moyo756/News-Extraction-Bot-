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
        self.css_selector_each_news_article_card = '.v-card.gothamist-card'
        self.title_identifier = "h2" # search by class
        self.description_identifier = "desc" # search by ????
        self.date_identifier = "" # search by ????
        self.image_identifier = "" # search by ????
        self.bot.open_news_site()
        self.close_popup()
        self.bot.wait_for_element(timeout=10,xpath_value=self.xpath_donate_popup)
        time.sleep(2)
        self.extract_news()
    
    # close the possible pop up that is revealed on the landing page
    def close_popup(self):
        self.bot.close_popup(popup_xpath=self.xpath_donate_popup)

    ### this function is responsible for extracting all the news articles and saving the required details to the array of News Article object
    def extract_news(self):
        articles = self.bot.find_all_elements_by_css_selector(self.css_selector_each_news_article_card)
        count = 0
        for a in articles:
            print("extracting...")
            try:
                #print(f"{a.text} \n\n")
                title = self.bot.find_element_by_class_name_from_element(from_element= a,class_name_value= 'h2').text
                time.sleep(1)
                article_metadata = self.bot.find_element_by_css_selector_from_element (from_element= a, css_selector_value='.article-metadata').text.split('\n') # card slot includes most things, date(op[tional]) wrote and number of comments
                try:
                    description = self.bot.find_element_by_class_name_from_element(from_element= a,class_name_value= 'desc').text
                    count=count+1
                    print(count)
                except Exception as no_descr:
                    # If no description is found, handle this exception
                    description = "No description available"
                #description = self.bot.find_element_by_xpath_from_element(from_element= card_slot, xpath_value='.//p[@class="desc"]').text
                article = NewsArticle(
                    title=title,
                    description= description,
                    date= article_metadata,
                    picture_filepath="path/abcsd",
                    count_of_search_phrases=3,
                    is_money_mentioned=False
                    )
                
                self.articles.append(article)
            except Exception as e:
                print(f"Error extracting data from an article: {e}")

            # TODO: I realized some articles do not have enough information and might require me to enter inside the article and scan for appropriate infromation

    def get_resultant_articles(self):
        return self.articles

