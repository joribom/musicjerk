from wikireader import get_wiki_summary, get_wiki_info
from spotifyreader import get_spotify_data
from musicbrainzreader import get_album_info
from urllib import parse
from threading import Lock, Thread

def make_url(album, artist):
    return '%s-%s' % (album.lower().replace(" ", "_"), artist.lower().replace(" ", "_"))

class Album:
    def __init__(self, title = None, artist = None, chosen_by = None,
                 rating = None, best_tracks = None, worst_tracks = None, debug = False):
        self.title = title
        self.artist = artist
        self.mutex = Lock()
        self.update_values(chosen_by, rating, best_tracks, worst_tracks)
        self.debug = debug
        self._spotify_id = None
        self._image_url  = None
        self._summary    = None
        self._tags       = []
        self._tracks     = []

    def update_api_values(self):
        if self.title is not None and self.artist is not None and not self.debug:
            print("Fetching info about %s - %s..." % (str(self.artist), str(self.title)))
            spotify_id, image_url = get_spotify_data(self.title, self.artist)
            if image_url is None:
                summary, image_url = get_wiki_info(self.title, self.artist)
            else:
                summary = get_wiki_summary(self.title, self.artist)
            with self.mutex:
                self._spotify_id = spotify_id
                self._image_url  = image_url
                self._summary    = summary

    def update_slow_api_values(self):
        print("Fetching slow info about %s - %s..." % (str(self.artist), str(self.title)))
        tags, tracks = get_album_info(self.title, self.artist)
        with self.mutex:
            self._tags = tags
            self._tracks = tracks

    def update_values(self, chosen_by, rating, best_tracks, worst_tracks):
        self.chosen_by = chosen_by
        self.rating = float(rating.replace(',', '.')) if rating else None
        self.best_tracks = best_tracks
        self.worst_tracks = worst_tracks

    def add_value(self, header, value):
        if header == "Rating":
            self.rating = int(value) if value else None
        elif header == "Worst Track(s)":
            self.best_tracks = best_tracks
        elif header == "Best Track(s)":
            self.worst_tracks = worst_tracks

    @property
    def url_unparsed(self):
        with self.mutex:
            return make_url(self.title, self.artist)

    @property
    def url(self):
        # Mutex is done with url_unparsed
        return parse.quote(self.url_unparsed.encode('utf-8')).lower()


    @property
    def spotify_id(self):
        with self.mutex:
            return self._spotify_id

    @property
    def tags(self):
        with self.mutex:
            return  self._tags

    @property
    def tracks(self):
        with self.mutex:
            return self._tracks

    @property
    def image_description(self):
        with self.mutex:
            return 'Album Cover (from Wikipedia)' if self._image_url is not None else self.title

    @property
    def summary(self):
        with self.mutex:
            return self._summary

    @property
    def image_url(self):
        with self.mutex:
            return self._image_url
