# from SentimentClassifier import SentimentClassifier
# from DataBaseHelper import DatabaseHelper
# import datetime

# databasehelper = DatabaseHelper()
# isNotQuit=True
# text = input("Please enter a text for sentiment: ")
# while isNotQuit:
#     if text == "Quit":
#         break
#     else:
#         classify = SentimentClassifier(text)
#         print("Polarity: ",classify.polarity)
#         databasehelper.insert_Data('Reviews', {
#             "Input": text,
#             "Polarity": classify.polarity,
#             "Classify": 'pos' if (classify.polarity > 0) else 'neg'
#         })
#         text = input("Please enter a text for sentiment: ")

# from urllib.request import urlopen
# from bs4 import BeautifulSoup
import re
# import json

# abc = urlopen('https://www.rottentomatoes.com/api/private/v2.0/browse?maxTomato=100&maxPopcorn=100&services=amazon%3Bhbo_go%3Bitunes%3Bnetflix_iw%3Bvudu%3Bamazon_prime%3Bfandango_now&certified&sortBy=release&type=dvd-streaming-all&page=1')
# for data in json.load(abc)['results']:
#     print(data['title'])

# bs = BeautifulSoup(html, features='lxml')
# for movie in bs.find_all('div', {'class', 'lister-item'}):
#     print({
#         'Title': movie.find('h3', {'class', 'lister-item-header'}).a.get_text()
#     })

# file_urls = ['sd', 'dsf', 'df', 'ttrg', 'gdf', 'sdfsd', 'sdf']
# m = re.sub('\._V1_.*_AL_', '', 'https://m.media-amazon.com/images/M/MV5BOTM0ZTcxNDktNmY4OC00ZjAzLWJkMjktMTM4ZjZhNjdjOGVkXkEyXkFqcGdeQXVyMjQyMjI3MjI@._V1_UX100_CR0,0,100,100_AL_.jpg')
# print(len(file_urls))


# ab = '(2011)'
# ab = ab.split('–')
# if len(ab) == 1:
#     ab = re.search('[0-9]+', ab[0]).group(0) if re.search('[0-9]+', ab[0]) else None
# else:
#     ab = {
#         'from': re.search('[0-9]+', ab[0]).group(0) if re.search('[0-9]+', ab[0]) else None, 
#         'to': re.search('[0-9]+', ab[1]).group(0) if re.search('[0-9]+', ab[1]) else None
#         }

# date = 'Oct 26, 2018Limited'
# print(re.search('[0-9][0-9][0-9][0-9]', date).group(0))

#字
#print(b'\xff\xfeW['.decode('utf-16'))
# val = ''
# for letter in '字 Wahid':
#     val += str(ord(letter))

#print(int(val))
# t = "\"productId\":\"111111\""
# m = re.match("\W*productId[^:]*:\D*(\d+)", t)
# if m:
#     print(m.group(1))


# from pymongo import MongoClient
# from bson.objectid import ObjectId

# client = MongoClient()
# db = client['Revisor']
# m = db.Movies.aggregate([
#         {"$group":{"_id":"$Title","name":{"$first":"$name"},"count":{"$sum":1}}},
#         {"$match":{"count":{"$gt":1}}},
#         {"$project":{"name":1,"_id":0}}
#     ])
# # db['Movies'].update(
# #     { "_id": ObjectId('5c2413adfceebb055c857b31') }, 
# #     { 
# #         "$setOnInsert": { "Rating.XXX": "123", "Link.YYY": "123" },
# #         "$set": { "abc" }
# #     }, upsert=True )

# for a in m:
#     print(a)


# from urllib.parse import urlparse
# # from urlparse import urlparse  # Python 2
# parsed_uri = urlparse('http://stacKOverflow.com/questions/1234567/blah-blah-blah-blah' )
# result = '{uri.netloc}'.format(uri=parsed_uri)
# print(result.lower())

# item = {'Rating': {
#                     'ROTT': { 'tomatoScore' : 'dfg', 'popcornScore': 'dfsg' },
#                     'abc': 'df'
#                     }}
# key = list(item['Rating'].keys())[0]
# print(item['Rating'][key])                    

# class MovieRepository:
#     collection={}

#     def add(self, movie):
#         first_letter =  movie["Title"][0].upper()
#         movies =  self.collection[first_letter] if first_letter in list(self.collection.keys()) else None
#         if movies is None:
#             self.collection[first_letter] = [{ '_id': movie['_id'], 'Title': movie['Title'] }]
#         else:
#             movies = list(movies).append({ '_id': movie['_id'], 'Title': movie['Title'] })
#             self.collection[first_letter] = movie
    
#     def get(self, movie):
#         first_letter =  movie["Title"][0].upper()
#         movies = self.collection[first_letter]
#         if movie is None:
#             return None
#         else:
#             for _movie in list(movies):
#                 if _movie["Title"] == movie["Title"]:
#                     return _movie["_id"]
#         return None

# from scrapper.scrapper.CollectionRepository.movieRepository import MovieRepository

# movieRepo = MovieRepository()
# movieRepo.add('23fw5645g6y45645', {'Title': 'Wahid', 'Year': '2019'})
# print(movieRepo.get({'Title': 'Wahid', 'Year': '2019'}))
# movieRepo.add('difh38h3u4rn3iu4', {'Title': 'Wahid', 'Year': {'from': '2018', 'to': '2019'}})
# print(movieRepo.get({'Title': 'Wahid', 'Year': '2019'}))
# print(movieRepo.get({'Title': 'Wahid', 'Year': {'from': '2018', 'to': '2019'}}))

# var = {'ReviewSource': 'IMDB', 'ReviewTitle': ' One of the best\n', 'Review': 'Just 3 words required:\nSpectacular musical masterpiece !!', 'UserName': 'brilliantdev', 'UserNameLink': '/user/ur79936047/?ref_=tt_urv', 'ReviewDateAdded': '15 February 2019', 'Rating': '10', 'FullReviewLink': None}
# print(var.update({23:'43'}))
# print(var)

# from scrapy.selector import Selector
# from bs4 import BeautifulSoup
# selector = Selector(text='''
# <div class="product_header" style="background-image: url(https://static.metacritic.com/images/products/movies/1/c3fbfff4f7774ec970810a29ca782185.jpg);background-size:cover;"> </div>
# '''
# )

# bs = BeautifulSoup(selector)

# print(bs.get_text())
# MovieYear = str(selector.css('div.product_header::attr(style)').extract_first())
# MovieYear = re.search('https://static.metacritic.com/images/products/movies/1/.*\.jpg', MovieYear)
#MovieYear = re.search('[0-9][0-9][0-9][0-9]', MovieYear).group(0) if re.search('[0-9][0-9][0-9][0-9]', MovieYear) else None
#print(MovieYear.group(0))

# for target_list in selector.css('div.bottom_divider:nth-child(1) ul li:nth-child(4)'):
#     # bs = BeautifulSoup(target_list)
#     # print(bs.get_text())
#     print(target_list.css('::text').extract())
#     #print(target_list)

# movieRepo = MovieRepository()
# movieRepo.add('23fw5645g6y45645', {'Title': 'Wahid', 'Year': '2019'})
# print(movieRepo.get({'Title': 'Wahid', 'Year': '2019'}))
# movieRepo.add('difh38h3u4rn3iu4', {'Title': 'Wahid', 'Year': {'from': '2018', 'to': '2019'}})
# print(movieRepo.get({'Title': 'Wahid', 'Year': '2019'}))
# print(movieRepo.get({'Title': 'Wahid', 'Year': {'from': '2018', 'to': '2019'}}))

# import timeit
# print(timeit.timeit('"-".join(str(n) for n in range(100))', number=10000))

# movie_object = [
#         {'Year': '2019'}, 
#         {'Year': 
#             {
#                 'from': '2018', 
#                 'to': '2019'
#             }
#         },
#         {'Year': 
#             {
#                 'from': '2018', 
#                 'to': '2019'
#             }
#         }
#     ]

# print(isinstance(movie_object[0]['Year'], dict))
# print(isinstance(movie_object[1]['Year'], dict) == isinstance(movie_object[0]['Year'], dict))
# print(isinstance(movie_object[1]['Year'], dict) == isinstance(movie_object[2]['Year'], dict))


# abc = {
#     'W': {
#         '2019': [{
#             '_id': '1234',
#             'Title': 'Wahid 123'
#         }]
#     } 
# }

# print(abc['W'].keys())



# import bisect 

# li = [(1, 2), (3, 6), (4, 45), (6, 7), (7, 1)] 
# a, b = zip(*li)

# x = bisect.bisect(a, 6.5)
# a1 = li[:x]
# a2 = li[x:]

# a1.append(tuple((6.5, 4)))
# li = a1 + a2
# print(li)


var = {'Files': []}
print(var['Files'])