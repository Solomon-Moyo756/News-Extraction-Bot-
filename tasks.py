from selenium import webdriver
from selenium.webdriver.common.by import By
from NewsExtractor import NewsExtractor
import time
from robocorp.tasks import task
from RPA.Robocorp.WorkItems import WorkItems



# if __name__ == "__main__":
#     news = NewsExtractor(search_value= "Trump")
#     results = news.get_resultant_articles()
#     for i in range(len(results)):
#         print(f'title{i}: {results[i].title} \n descr: {results[i].description}\n date: {results[i].date}\n image: {results[i].picture_filepath}\n count_of_search_phrases: {results[i].count_of_search_phrases}\n is_money_mentioned: {results[i].is_money_mentioned}\n\n')
        
#         # TODO: try rewview all the search results, meaning find a way to click the load more button and read all the n results
#         # Find the number of times the search phrase was included in the results
#         # Find if the title and description include money in them...
#         # save the details in excel file, and download the image to a specific folder in your laptop
#         # Create robocorb account
#         # TODO: Create GitHub actions, and link them to your robocorb account
#         # TODO: make use of robocorb work items to input data for this bot.
#     news.save_to_excel(results)


@task
def Extract_News_Task():
    work_item = WorkItems()
    work_item.get_input_work_item()
    input_search_phrase = work_item.get_work_item_variable("search_phrase")

    print(f"Search phrase is: {input_search_phrase}")
    news = NewsExtractor(search_value= input_search_phrase)
    results = news.get_resultant_articles()
    for i in range(len(results)):
        print(f'title{i}: {results[i].title} \n descr: {results[i].description}\n date: {results[i].date}\n image: {results[i].picture_filepath}\n count_of_search_phrases: {results[i].count_of_search_phrases}\n is_money_mentioned: {results[i].is_money_mentioned}\n\n')
        
        # TODO: try rewview all the search results, meaning find a way to click the load more button and read all the n results
        # Find the number of times the search phrase was included in the results
        # Find if the title and description include money in them...
        # save the details in excel file, and download the image to a specific folder in your laptop
        # Create robocorb account
        # TODO: Create GitHub actions, and link them to your robocorb account
    #news.save_to_excel(results)