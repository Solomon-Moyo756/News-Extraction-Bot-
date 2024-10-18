from selenium import webdriver
from selenium.webdriver.common.by import By
from NewsExtractor import NewsExtractor
import time

if __name__ == "__main__":
    news = NewsExtractor()
    results = news.get_resultant_articles()
    for i in range(len(results)):
        print(f'title{i}: {results[i].title} \n descr: {results[i].description}\n date: {results[i].date}\n\n')
        