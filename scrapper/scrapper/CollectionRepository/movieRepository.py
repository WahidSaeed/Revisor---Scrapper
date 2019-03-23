import bisect
from scrapper.Utility.utility import binarySearch

class MovieRepository:

#    Sample Collection Repository
#    {
#        'First Letter': {
#            'Year Concatenated as 20192030': [{
#                '_id': 'sdfsdg33sdf',
#                'Title in ASCII': 234677565675
#            }]
#        }
#    }    

    collection = {}

    def add(self, _id, movie):
        first_letter = movie["Title"][0].upper()
        movie_title_ASCII = int(''.join([str(ord(letter)) for letter in movie['Title']]))
        movie_year = movie["Year"]
        if isinstance(movie_year, dict):
            movie_year = str(movie_year['from']) + str(movie_year['to'])
        movies = list(self.collection[first_letter].keys()) if first_letter in list(self.collection.keys()) else []
        is_first_entry = True if len(movies) == 0 else False
        movies = list(self.collection[first_letter][movie_year]) if movie_year in movies else None
        movie_object_tuple = (_id, movie_title_ASCII)
        if movies is None:
            if is_first_entry:
                self.collection[first_letter] = {movie_year: [movie_object_tuple]}
            else:
                self.collection[first_letter].update({movie_year: [movie_object_tuple]})
        else:
            _ids, movie_titles = zip(*movies)
            slice_index = bisect.bisect(movie_titles, movie_title_ASCII)
            movies_sliced_1 = movies[:slice_index]
            movies_sliced_2 = movies[slice_index:]
            movies_sliced_1.append(movie_object_tuple)
            movies = movies_sliced_1 + movies_sliced_2
            self.collection[first_letter][movie_year] = movies

    def get(self, movie):
        first_letter = movie["Title"][0].upper()
        movie_title_ASCII = int(''.join([str(ord(letter)) for letter in movie['Title']]))
        movie_year = movie["Year"]
        if isinstance(movie_year, dict):
            movie_year = str(movie_year['from']) + str(movie_year['to'])
        movies = list(self.collection[first_letter].keys()) if first_letter in list(self.collection.keys()) else []
        movies = list(self.collection[first_letter][movie_year]) if movie_year in movies else None
        if movies is None:
            return None
        else:
            _ids, movie_titles = zip(*movies)
            title_index = binarySearch(movie_titles, 0, len(movie_titles) - 1, movie_title_ASCII)
            if title_index is not None:
                return _ids[title_index]
        return None