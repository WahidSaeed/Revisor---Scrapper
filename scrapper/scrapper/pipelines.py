import scrapy
from scrapper.enums.DML_enums import DML_Operation
from scrapper.DatabaseHelper.movieDataHelper import MovieDatabaseHelper
import threading

class MoviePipeline(object):
    def __init__(self, movieDBHelper):
        self.movieDBHelper = movieDBHelper

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            movieDBHelper=MovieDatabaseHelper()
        )

    def open_spider(self, spider):
        self.movieDBHelper.open_connection()

    def close_spider(self, spider):
        self.movieDBHelper.close_connection()

    def process_item(self, item, spider):
        OPERATION, ITEMS = item['Item']
        if OPERATION == DML_Operation.SAVE_OBJECT:
            threading.Thread(target=self.movieDBHelper.insert_Movie, args=(ITEMS,)).start()
        elif OPERATION == DML_Operation.SAVE_POSTERS:
            threading.Thread(target=self.movieDBHelper.update_movie_photos, args=(ITEMS,)).start()
        elif OPERATION == DML_Operation.SAVE_REVIEWS:
            threading.Thread(target=self.movieDBHelper.insert_movie_reviews, args=(ITEMS,)).start()
        return ITEMS