import scrapy


class MovieItem(scrapy.Item):
    Title = scrapy.Field()
    Year = scrapy.Field()
    Synopsis = scrapy.Field()
    Certificate = scrapy.Field()
    RunTime = scrapy.Field()
    Genre = scrapy.Field()
    Rating = scrapy.Field()   
    Link = scrapy.Field()
    Actors = scrapy.Field()
    Files = scrapy.Field()

class MoviePoster(scrapy.Item):
    Title = scrapy.Field()
    Year = scrapy.Field()
    PosterURL = scrapy.Field()
    Year = scrapy.Field()

class MovieReviewsItem(scrapy.Item):
    Title = scrapy.Field()
    Year = scrapy.Field()
    Reviews = scrapy.Field()

class BookItem(scrapy.Item):
    Title = scrapy.Field()
    Author = scrapy.Field()
    ISBN = scrapy.Field()
    PublishDate = scrapy.Field()
    Publisher = scrapy.Field()
    PagesNo = scrapy.Field()
    Category = scrapy.Field()

class BookReviewsItem(scrapy.Item):
    BookObjectID = scrapy.Field()
    BookTitle = scrapy.Field()
    ReviewSource = scrapy.Field() 
    Review = scrapy.Field()
    UserName = scrapy.Field()
    UserNameLink = scrapy.Field()
    ReviewDateAdded = scrapy.Field()
    Rating = scrapy.Field()
    FullReviewLink = scrapy.Field()