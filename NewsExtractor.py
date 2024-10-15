from selenium import webdriver
from selenium.webdriver.common.by import By
from NewsSelenium import NewsSelenium
import time

class NewsExtractor:

    def __init__(self) -> None:
        self.bot = NewsSelenium("https://gothamist.com/")
        self.bot.open_news_site()
        time.sleep(10)
