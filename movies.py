import movie_class
import fresh_tomatoes
import requests

API_KEY = "535f2a41b3683d5dc7a995601961d6d8"
DEFAULT_TRAILER = "NL6CDFn2i3I"


def get_movies(user_input):
    """Returns movie info based on user input, either via query or now playing movies"""

    if user_input:
        payload = {
            "api_key": API_KEY,
            "query": user_input
        }

        api_res = requests.get("http://api.themoviedb.org/3/search/movie?", params=payload)
        movies_data = api_res.json()

    else:
        payload = {
            "api_key": API_KEY
        }

        api_res = requests.get("http://api.themoviedb.org/3/movie/now_playing?", params=payload)
        movies_data = api_res.json()

    try:
        print movies_data["errors"]
        return False
    except:
        movie_list = []
        for m in range(len(movies_data["results"])): # how to make this better
            movie = make_movie(movies_data["results"][m])
            if movie:
                movie_list.append(movie)
        return movie_list


def get_youtube(movie_id):
    """get Youtube id to use in the tile"""
    payload = {"api_key": API_KEY}
    api_res = requests.get("http://api.themoviedb.org/3/movie/" + str(movie_id) + "/videos?", params=payload)
    youtube_data = api_res.json()

    try:
        return youtube_data["results"][0]["key"]
    except:
        # if there is no trailer, return default trailer
        return DEFAULT_TRAILER


def make_movie(movie_data):
    """extract data for each movie tile and make it a Movie object"""

    # if poster exists make movie, else skip
    if movie_data["poster_path"]:
        title = movie_data["title"]
        plot = movie_data["overview"].encode('utf-8')
        movie_id = movie_data["id"]
        year = movie_data['release_date'][:4]
        youtube_link = get_youtube(movie_id)
        poster = "https://image.tmdb.org/t/p/w600_and_h900_bestv2/" + str(movie_data["poster_path"])
        movie = movie_class.Movie(title, poster, plot, year, youtube_link)
    else:
        movie = False

    return movie


def generate_page():
    """generating page with movie tiles from fresh_tomatoes.py"""

    user_input = raw_input("Search for movies based on a keyword "
                           "or if you want to see the new playing movies press enter: ")

    # debugging helpers
    # user_input = ""
    # user_input = "friend"

    movies = get_movies(user_input)

    if movies:
        fresh_tomatoes.open_movies_page(movies)
    else:
        print "No movies, use another word"
        return generate_page()

    return "All good"


generate_page()
