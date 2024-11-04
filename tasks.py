from selenium import webdriver
from selenium.webdriver.common.by import By
from NewsExtractor import NewsExtractor
import time
from robocorp.tasks import task
from RPA.Robocorp.WorkItems import WorkItems



# if __name__ == "__main__":
#     news = NewsExtractor(search_value= "Trump")
#     results = news.get_resultant_articles()
#     # TODO: Create GitHub actions, and link them to your robocorb account
#     news.save_to_excel(results)


@task
def Extract_News_Task():
    work_item = WorkItems()
    work_item.get_input_work_item()
    input_search_phrase = work_item.get_work_item_variable("search_phrase")
    print(f"Search phrase is: {input_search_phrase}")
    news = NewsExtractor(search_value= input_search_phrase)
    results = news.get_resultant_articles()
    news.save_to_excel(results)