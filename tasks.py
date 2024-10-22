from selenium import webdriver
from selenium.webdriver.common.by import By
from NewsExtractor import NewsExtractor
import time

if __name__ == "__main__":
    news = NewsExtractor(search_value= "Trump")
    results = news.get_resultant_articles()
    for i in range(len(results)):
        print(f'title{i}: {results[i].title} \n descr: {results[i].description}\n date: {results[i].date}\n image: {results[i].picture_filepath}\n count_of_search_phrases: {results[i].count_of_search_phrases}\n is_money_mentioned: {results[i].is_money_mentioned}\n\n')
        
        # TODO: try rewview all the search results, meaning find a way to click the load more button and read all the n results
        # Find the number of times the search phrase was included in the results
        # Find if the title and description include money in them...