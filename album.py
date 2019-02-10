from wikireader import get_wiki_summary, get_wiki_info
from spotifyreader import get_spotify_data
from urllib import parse

def make_url(album, artist):
    return '%s-%s' % (album.lower().replace(" ", "_"), artist.lower().replace(" ", "_"))

class Album:
    def __init__(self, title = None, artist = None, chosen_by = None,
                 rating = None, best_tracks = None, worst_tracks = None, debug = False):
        self.title = title
        self.artist = artist
        self.update_values(chosen_by, rating, best_tracks, worst_tracks)
        self.debug = debug
        if self.title is not None and self.artist is not None and not self.debug:
            print("Fetching info about %s - %s..." % (str(self.artist), str(self.title)))
            self.spotify_id, self._image_url = get_spotify_data(self.title, self.artist)
            if self._image_url is None:
                self._summary, self._image_url = get_wiki_info(self.title, self.artist)
            else:
                self._summary = get_wiki_summary(self.title, self.artist)

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
        return make_url(self.title, self.artist)

    @property
    def url(self):
        return parse.quote(self.url_unparsed.encode('utf-8')).lower()

    @property
    def image_description(self):
        return 'Album Cover (from Wikipedia)' if self._image_url is not None else 'No image found :('

    @property
    def summary(self):
        return self._summary

    @property
    def image_url(self):
        return self._image_url
