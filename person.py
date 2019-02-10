from collections import OrderedDict
from album import Album

class Person:
    def __init__(self, name):
        self.name = name
        self.albums = OrderedDict()
        self.likeness_list = []

    def reset_data():
        self.albums = OrderedDict()

    def update_album(self, album_name, rating, best_tracks, worst_tracks):
        album = Album(rating, best_tracks, worst_tracks)
        self.albums[album_name] = album

    def add_value(self, album_name, header, value):
        if album_name not in self.albums:
            self.albums[album_name] = Album()
        self.albums[album_name].add_value(header, value)

    def get_ratings(self):
        ratings = []
        for album in self.albums.values():
            if album.rating is not None:
                ratings.append(album.rating)
        return ratings

    def generate_likeness(self, people):
        print("Generating likeness list for %s." % self.name)
        likenesses = []
        for other in people:
            if self == other:
                continue
            likenesses.append((other.name, other.compare(self)))
        likenesses = sorted(likenesses, key = lambda x: 0 if x[1] is None else -x[1])
        likenesses = [(name.title(), "%.2f" % (likeness * 100) if likeness is not None else "None") for name, likeness in likenesses]
        self.likeness_list = likenesses

    def compare(self, other):
        sum = 0.0
        count = 0
        for album_name in self.albums:
            if not album_name in other.albums:
                continue
            self_rating  = self.albums.get(album_name).rating
            other_rating = other.albums.get(album_name).rating
            if self_rating is not None and other_rating is not None:
                likeness = (10.0 - abs(self_rating - other_rating)) / 10.0
                sum += likeness
                count += 1
        return sum / float(count) if count > 0 else None
