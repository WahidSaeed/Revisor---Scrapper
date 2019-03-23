import scrapy
import re
import json
from scrapper.items import MovieItem, MovieReviewsItem
from urllib.parse import urlparse

class IMDBSpider(scrapy.Spider):
    name = 'Books'
    allowed_domains = [
        'booklikes.com',
        'goodreads.com'
    ]
    
    def start_requests(self):
        urls = [
            'http://booklikes.com/catalog/list',
            'https://www.goodreads.com/genres/list'
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_booklikes_list_book)
    
    def parse_booklikes_list_book(self, response):
        for category in response.css('table.catalog-list'):
            pass
