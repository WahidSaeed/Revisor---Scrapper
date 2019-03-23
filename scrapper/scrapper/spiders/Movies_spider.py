import scrapy
import re
import json
from scrapper.items import MovieItem, MoviePoster, MovieReviewsItem
from urllib.parse import urlparse
from scrapper.enums.DML_enums import DML_Operation
from scrapper.Utility.utility import clean_text

class IMDBSpider(scrapy.Spider):
    name = 'Movies'
    allowed_domains = [
        'imdb.com',
        'rottentomatoes.com',
        'metacritic.com'
    ]
    rott_page = 1
    mtc_page = 0

    def start_requests(self):
        urls = [
            'https://www.imdb.com/search/title?title_type=feature,tv_movie,tv_series,tv_episode,tv_special,tv_miniseries,documentary,short,video,tv_short&countries=in&count=250'
            'https://www.imdb.com/search/title?title_type=feature,tv_movie,tv_series,tv_episode,tv_special,tv_miniseries,documentary,short,video,tv_short&countries=pk&count=250',
            'https://www.imdb.com/search/title?title_type=feature,tv_movie,tv_series,tv_episode,tv_special,tv_miniseries,documentary,short,video,tv_short&countries=us&count=250',
            'https://www.rottentomatoes.com/api/private/v2.0/browse?maxTomato=100&maxPopcorn=100&services=amazon%3Bhbo_go%3Bitunes%3Bnetflix_iw%3Bvudu%3Bamazon_prime%3Bfandango_now&certified&sortBy=release&type=dvd-streaming-all&page=' + str(self.rott_page),
            'https://www.metacritic.com/browse/movies/score/metascore/all/filtered?sort=desc&page=' + str(self.mtc_page) 
        ]
        for url in urls:
            uri = '{uri.netloc}'.format(uri=urlparse(url)).lower()
            if uri == 'www.imdb.com':
                yield scrapy.Request(url=url, callback=self.parse_IMDB_movie)
            elif uri == 'www.rottentomatoes.com':
                yield scrapy.Request(url=url, callback=self.parse_rottentomatoes_movie_link)
            elif uri == 'www.metacritic.com':
                yield scrapy.Request(url=url, callback=self.parse_metacritic_movie)

    def parse_IMDB_movie(self, response):
        for movie in response.css('div.lister-item'):
            relative_URL = movie.css('h3.lister-item-header a::attr(href)').extract_first()
            IMDB_ID = re.search('tt[0-9]+', relative_URL)
            MovieYear = movie.css('span.lister-item-year::text').extract_first()
            MovieYear = MovieYear.split('–')
            if len(MovieYear) == 1:
                MovieYear = re.search('[0-9]+', MovieYear[0]).group(0) if re.search('[0-9]+', MovieYear[0]) else None
            else:
                MovieYear = {
                'from': re.search('[0-9]+', MovieYear[0]).group(0) if re.search('[0-9]+', MovieYear[0]) else None, 
                'to': re.search('[0-9]+', MovieYear[1]).group(0) if re.search('[0-9]+', MovieYear[1]) else None
                }
            yield {'Item': (DML_Operation.SAVE_OBJECT, MovieItem(
                Title = clean_text(movie.css('h3.lister-item-header a::text').extract_first()),
                Synopsis = clean_text(movie.css('div.ratings-bar + p.text-muted::text').extract_first()),
                Certificate = clean_text(movie.css('span.certificate::text').extract_first()),
                RunTime = clean_text(movie.css('span.runtime::text').extract_first()),
                Genre = [clean_text(genre) for genre in movie.css('span.genre::text').extract_first().split(',')] if movie.css('span.genre::text').extract_first() else None,
                Rating = {
                    'IMDB': clean_text(movie.css('div.ratings-bar div.ratings-imdb-rating strong::text').extract_first())
                    },
                Link = {
                    'IMDB': IMDB_ID.group(0) if IMDB_ID else None,
                },
                Year = MovieYear,
                Files = []
            ))}
            if IMDB_ID:
                yield scrapy.Request('https://www.imdb.com/title/' + IMDB_ID.group(0) + '/mediaindex?refine=poster&ref_=ttmi_ref_pos', self.parse_IMDB_movie_poster)
                yield scrapy.Request('https://www.imdb.com/title/' + IMDB_ID.group(0) + '/reviews', self.parse_IMDB_movie_reviews)

        next_page = response.css('a.lister-page-next::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse_IMDB_movie)
    
    def parse_IMDB_movie_poster(self, response):
        file_urls = []
        MovieTitle = response.css('div.subpage_title_block h3 a::text').extract_first()
        MovieYear = response.css('div.subpage_title_block h3 span.nobr::text').extract_first()
        MovieYear = MovieYear.split('–')
        if len(MovieYear) == 1:
            MovieYear = re.search('[0-9]+', MovieYear[0]).group(0) if re.search('[0-9]+', MovieYear[0]) else None
        else:
            MovieYear = {
            'from': re.search('[0-9]+', MovieYear[0]).group(0) if re.search('[0-9]+', MovieYear[0]) else None, 
            'to': re.search('[0-9]+', MovieYear[1]).group(0) if re.search('[0-9]+', MovieYear[1]) else None
            }
        for poster in response.css('div.media_index_thumb_list a'):
            posterURL = poster.css('img::attr(src)').extract_first()
            posterURL = re.sub('\._V1_.*_AL_', '', str(posterURL))
            file_urls.append(posterURL)
        if len(file_urls) > 0:
            yield {'Item': (DML_Operation.SAVE_POSTERS, MoviePoster(
                Title = clean_text(MovieTitle),
                Year = MovieYear,
                PosterURL = file_urls[:-1] if len(file_urls) > 1 else []
                ))}

    def parse_IMDB_movie_reviews(self, response):
        MovieTitle = response.css('div.subpage_title_block h3 a::text').extract_first()
        MovieYear = response.css('div.subpage_title_block h3 span.nobr::text').extract_first()
        MovieYear = MovieYear.split('–')
        if len(MovieYear) == 1:
            MovieYear = re.search('[0-9]+', MovieYear[0]).group(0) if re.search('[0-9]+', MovieYear[0]) else None
        else:
            MovieYear = {
            'from': re.search('[0-9]+', MovieYear[0]).group(0) if re.search('[0-9]+', MovieYear[0]) else None, 
            'to': re.search('[0-9]+', MovieYear[1]).group(0) if re.search('[0-9]+', MovieYear[1]) else None
            }
        Reviews = []
        for reviews in response.css('div.lister-item-content'):
            Reviews.append({
                'ReviewSource': 'IMDB',
                'ReviewTitle': clean_text(reviews.css('a.title::text').extract_first()),
                'Review': clean_text(reviews.css('div.content div.text::text').extract_first()),
                'UserName': clean_text(reviews.css('span.display-name-link a::text').extract_first()),
                'UserNameLink': clean_text(reviews.css('span.display-name-link a::attr(href)').extract_first()),
                'ReviewDateAdded': clean_text(reviews.css('span.review-date::text').extract_first()),
                'Rating': clean_text(reviews.css('span.rating-other-user-rating span::text').extract_first()),
                'FullReviewLink': None
            })
            
        if len(Reviews) > 0:
            yield {'Item': (DML_Operation.SAVE_REVIEWS, MovieReviewsItem(
                Title = clean_text(MovieTitle),
                Reviews = Reviews,
                Year = MovieYear
            ))}
            
    def parse_rottentomatoes_movie_link(self, response):
        for movieID in json.loads(response.text)["results"]:
            yield scrapy.Request('https://www.rottentomatoes.com/api/private/v1.0/movies/' + str(movieID['id']), callback=self.parse_rottentomatoes_movie)
        self.rott_page += 1
        yield response.follow('browse?maxTomato=100&maxPopcorn=100&services=amazon%3Bhbo_go%3Bitunes%3Bnetflix_iw%3Bvudu%3Bamazon_prime%3Bfandango_now&certified&sortBy=release&type=dvd-streaming-all&page=' + str(self.rott_page), callback=self.parse_rottentomatoes_movie_link)

    def parse_rottentomatoes_movie(self, response):
        movie = json.loads(response.text)
        genre = []
        files = []
        for genreset in movie['genreSet']:
            genre.append(genreset['displayName'])
        for photo in movie['photos']['photos']:
            files.append(photo['url'])
        if movie is not None:
            yield {'Item': (DML_Operation.SAVE_OBJECT, MovieItem(
                Title = movie['title'],
                Synopsis = movie['synopsis'],
                Certificate = movie['mpaaRating'],
                RunTime = movie['runningTimeStr'],
                Genre = genre,
                Rating = {
                    'ROTT': { 'tomatoScore' : str(movie['ratings']['critics_score']), 'popcornScore': str(movie['ratings']['audience_score']) }
                    },
                Link = {
                    'ROTT': movie['url'],
                },
                Year = str(movie['year']),
                Files = files if len(files) > 0 else []
            ))}
            yield scrapy.Request('https://www.rottentomatoes.com' + movie['url'] + 'reviews/?type=top_critics', callback=self.parse_rottentomatoes_movie_reviews)

    def parse_rottentomatoes_movie_reviews(self, response):
        MovieTitle = response.css('div.center h2 a::text').extract_first()
        MovieYear = response.css('div.bottom_divider').extract()[0]
        if MovieYear:
            MovieYear = scrapy.Selector(text=str(MovieYear)).css('ul li:nth-child(4)').extract()[0]
        MovieYear = re.search('[0-9][0-9][0-9][0-9]', MovieYear).group(0) if re.search('[0-9][0-9][0-9][0-9]', MovieYear) else None
        Reviews = []
        for reviews in response.css('div.review_table_row'):
            Reviews.append({
                'ReviewSource':  'ROTT',
                'ReviewTitle': None,
                'Review': clean_text(reviews.css('div.the_review::text').extract_first()),
                'UserName': clean_text(reviews.css('div.critic_name a.articleLink::text').extract_first()),
                'UserNameLink': clean_text(reviews.css('div.critic_name a.articleLink::attr(href)').extract_first()),
                'ReviewDateAdded': clean_text(reviews.css('div.review_date::text').extract_first()),
                'Rating': '0' if reviews.css('div.rotten') else '1',
                'FullReviewLink': clean_text(reviews.css('div.subtle a::attr(href)').extract_first())
            })
            
        if len(Reviews) > 0:
            yield {'Item': (DML_Operation.SAVE_REVIEWS, MovieReviewsItem(
                Title = clean_text(MovieTitle),
                Reviews = Reviews,
                Year = str(MovieYear)
            ))}

    def parse_metacritic_movie(self, response):
        for movie in response.css('td.clamp-summary-wrap'):
            movie_url = movie.css('a.title::attr(href)').extract_first()
            yield response.follow(movie_url, callback=self.parse_metacritic_movie_reviews)
        self.mtc_page += 1
        yield response.follow('/browse/movies/score/metascore/all/filtered?sort=desc&page=' + str(self.mtc_page), callback=self.parse_metacritic_movie)

    def parse_metacritic_movie_reviews(self, response):
        MovieTitle = response.css('div.product_page_title h1::text').extract_first()
        MovieYear = response.css('span.release_date span:nth-child(2)::text').extract_first()
        MovieYear = re.search('[0-9][0-9][0-9][0-9]', MovieYear).group(0) if re.search('[0-9][0-9][0-9][0-9]', MovieYear) else None
        MoviePoster = response.css('div.product_header::attr(style)').extract_first()
        MoviePoster = re.search('https://static.metacritic.com/images/products/movies/1/.*\.jpg', str(MoviePoster))
        yield {'Item': (DML_Operation.SAVE_OBJECT, MovieItem(
                Title = clean_text(MovieTitle),
                Synopsis = clean_text(response.css('div.summary_deck.details_section span.blurb.blurb_expanded::text').extract_first() if response.css('div.summary_deck.details_section span.blurb.blurb_expanded::text').extract_first() else response.css('div.summary_deck.details_section span:nth-child(2) span::text').extract_first()),
                Certificate = clean_text(response.css('div.rating span:nth-child(2)::text').extract_first()),
                RunTime = clean_text(response.css('div.runtime span:nth-child(2)::text').extract_first()),
                Genre = response.css('div.genres span:nth-child(2) span::text').extract(),
                Rating = {
                    'MTC': clean_text(response.css('div.distribution div.score a.metascore_anchor div.metascore_w.larger.movie::text').extract_first())
                    },
                Link = {
                    'MTC': response.url,
                },
                Year = MovieYear,
                Files = [MoviePoster.group(0)] if MoviePoster else []
            ))}
        
        Reviews = []
        for review in response.css('div.critic_reviews2 div.review'):
            Reviews.append({
                'ReviewSource':  'MTC',
                'ReviewTitle': None,
                'Review': clean_text(review.css('div.summary a.no_hover::text').extract_first()),
                'UserName': clean_text(review.css('span.author a::text').extract_first()),
                'UserNameLink': clean_text(review.css('span.author a::attr(href)').extract_first()),
                'ReviewDateAdded': clean_text(review.css('div.date::text').extract_first()),
                'Rating': clean_text(review.css('div.score_wrap div.metascore_w::text').extract_first()),
                'FullReviewLink': clean_text(review.css('div.summary a.no_hover::attr(href)').extract_first())
            })

        if len(Reviews) > 0:
            yield {'Item': (DML_Operation.SAVE_REVIEWS, MovieReviewsItem(
                Title = clean_text(MovieTitle),
                Reviews = Reviews,
                Year = MovieYear
            ))}