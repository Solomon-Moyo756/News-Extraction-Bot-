from selenium import webdriver
from selenium.webdriver.common.by import By
from NewsExtractor import NewsExtractor
import time

# use the
#bot = NewsSelenium("https://gothamist.com/")
#bot.open_news_site()
#element = bot.find_element_by_xpath('//*[@id="__nuxt"]/div/div/main/header/div[1]/div[2]/a/span')
#time.sleep(3)
#bot.scroll_page_until_element('//*[@id="gothamist-footer"]/div/div[2]/div[2]')
#extracted_text = bot.extract_text_from_element(element=element)
#print(extracted_text)
#time.sleep(10)


if __name__ == "__main__":
    NewsExtractor()