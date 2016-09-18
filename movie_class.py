# one super tiny class

class Movie(object):
    """making the Movie object"""
    def __init__(self, title, poster, plot, year, youtube_id):
        self.title = title
        self.poster_image_url = poster
        self.plot = plot
        self.youtube_id = youtube_id
