class NewsArticle:


    def __init__(self,title, date, description, picture_filepath, count_of_search_phrases,is_money_mentioned) -> None:
        self.title = title
        self.date = date
        self.description = description
        self.picture_filepath = picture_filepath
        self.count_of_search_phrases = count_of_search_phrases
        self.is_money_mentioned = is_money_mentioned
