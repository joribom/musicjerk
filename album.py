class Album:
    def __init__(self):
        self.rating = None
        self.best_tracks = None
        self.worst_tracks = None

    def add_value(self, header, value):
        if header == "Rating":
            self.rating = int(value) if value else None
        elif header == "Worst Track(s)":
            self.best_tracks = best_tracks
        elif header == "Best Track(s)":
            self.worst_tracks = worst_tracks
