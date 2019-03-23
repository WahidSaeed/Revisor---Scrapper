from bson.objectid import ObjectId
import pymongo
from scrapper.CollectionRepository.movieRepository import MovieRepository
from scrapper.settings import DATABASE_MOVIE, COLLECTION_MOVIE, COLLECTION_MOVIE_REVIEWS


class MovieDatabaseHelper:
    def __init__(self):
        self.movieRepository = MovieRepository()

    def open_connection(self):
        self.client = pymongo.MongoClient()
        self.db = self.client[DATABASE_MOVIE]

    def close_connection(self):
        self.client.close()
    
    def insert_Movie(self, movieDocument):
        _id = self.movieRepository.get(movieDocument)
        first_letter = movieDocument["Title"][0].upper()
        if _id is None:
            _id = self.db[COLLECTION_MOVIE + '_' + first_letter].insert_one(dict(movieDocument)).inserted_id
            self.movieRepository.add(_id, movieDocument)
        else:
            rating_key = list(movieDocument['Rating'].keys())[0]
            link_key = list(movieDocument['Link'].keys())[0]
            Files = list(movieDocument['Files'])
            self.db[COLLECTION_MOVIE + '_' + first_letter].update(
                {
                    '_id': {'$eq': ObjectId(_id)}
                },
                {
                    '$set': {
                        'Rating.' + rating_key: movieDocument['Rating'][rating_key], 
                        'Link.' + link_key: movieDocument['Link'][link_key] 
                    },
                    '$push': { 'files': { '$each': Files if len(Files) > 0 else None } }
                }
            )
    
    def update_movie_photos(self, movieDocument):
        _id = self.movieRepository.get(movieDocument)
        first_letter = movieDocument["Title"][0].upper()
        if _id is not None:
            self.db[COLLECTION_MOVIE + '_' + first_letter].update(
                {
                    '_id': { '$eq': ObjectId(_id) }
                },
                {
                    '$push': { 'files': { '$each': [] if movieDocument['PosterURL'] is None else list(movieDocument['PosterURL']) } }
                }
            )

    def insert_movie_reviews(self, movieDocument):
        _id = self.movieRepository.get(movieDocument)
        first_letter =  movieDocument["Title"][0].upper()
        if _id is not None:
            for Reviews in list(movieDocument['Reviews']):
                _Reviews = dict(Reviews)
                _Reviews.update({'MovieObjectID': ObjectId(_id)})
                self.db[COLLECTION_MOVIE_REVIEWS + '_' + first_letter].insert_one(dict(_Reviews))