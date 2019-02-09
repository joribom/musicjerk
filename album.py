from wikireader import get_wiki_info
from urllib import parse

class Album:
    def __init__(self, title = None, artist = None, chosen_by = None,
                 rating = None, best_tracks = None, worst_tracks = None):
        self.title = title
        self.artist = artist
        self.chosen_by = chosen_by
        self.rating = float(rating.replace(',', '.')) if rating else None
        self.best_tracks = best_tracks
        self.worst_tracks = worst_tracks
        if self.title is not None and self.artist is not None:
            print("Fetching info about %s - %s..." % (str(self.artist), str(self.title)))
            self._summary, self._image_url = get_wiki_info(self.title, self.artist)

    def add_value(self, header, value):
        if header == "Rating":
            self.rating = int(value) if value else None
        elif header == "Worst Track(s)":
            self.best_tracks = best_tracks
        elif header == "Best Track(s)":
            self.worst_tracks = worst_tracks

    def add_value(self, header, value):
        if header == "Rating":
            self.rating = int(value) if value else None
        elif header == "Worst Track(s)":
            self.best_tracks = best_tracks
        elif header == "Best Track(s)":
            self.worst_tracks = worst_tracks

    @property
    def url(self):
        unicode_url = '%s-%s' % (self.title.lower().replace(" ", "_"), self.artist.lower().replace(" ", "_"))
        return parse.quote(unicode_url.encode('utf-8')).lower()

    @property
    def image_description(self):
        return 'Album Cover (from Wikipedia)' if self._image_url is not None else 'No image found :('

    @property
    def summary(self):
        return self._summary

    @property
    def image_url(self):
        return self._image_url
