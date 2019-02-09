import gspread, os
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_time
from dateutil.tz import tzlocal
from collections import OrderedDict
from person import Person
from album import Album

# Decorator for functions that use data from google sheets,
# to automatically check for new updates.
def check_updates(func):
    def wrapper(reader, *args):
        try:
            if reader.update_required():
                reader.update_values()
        except Exception as e:
            print ("Caught an exception! '%s'" % str(e))
            reader.__init__()
        return func(reader, *args)
    return wrapper

def avg(lst):
    return sum(lst) / len(lst)

class Reader:

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    def __init__(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', Reader.scope)
        client = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        self.sheet = client.open("Musicjerk's big album sheet").sheet1
        self.latest_update_check = datetime.now(tzlocal())
        self.people = OrderedDict()
        self.album_dict = {}
        self.latest_update = None
        self.update_values()

    def update_required(self):
        if datetime.now(tzlocal()) - self.latest_update_check < timedelta(seconds = 5):
            return False
        latest_change_time = parse_time(self.sheet.cell(1, 1).value)
        print(self.sheet.cell(1, 1).value)
        self.latest_update_check = datetime.now(tzlocal())
        if self.latest_update < latest_change_time:
            print("Update required...")
        return self.latest_update < latest_change_time

    def update_values(self):
        print("Updating values from google sheets...")
        self.latest_update = datetime.now(tzlocal())
        all_values   = self.sheet.get_all_values()
        top_row      = all_values[0]
        col_headers  = all_values[1]
        for cell in top_row[5:]:
            name = cell.lower()
            if name and self.people.get(name) is None:
                self.people[name] = Person(name)
        self.general_data = {}
        self.user_data    = {}
        self.albums       = []
        for row in all_values[2:]:
            album        = row[0].replace(" (Optional)", '')
            if not album:
                break                                        # Break since no more albums present
            artist       = row[1]
            chosen_by    = row[2]
            average      = row[3]
            best_tracks  = row[4]
            worst_tracks = row[5]
            self.albums.append(Album(album, artist, chosen_by, average, best_tracks, worst_tracks))
            self.album_dict[self.albums[-1].url_unparsed] = self.albums[-1]
            name = ""
            for col, value in enumerate(row[7:]):
                col    = col + 7
                name   = top_row[col].lower() if top_row[col] else name
                header = col_headers[col]
                self.people[name].add_value(album, header, value)
                if name not in self.user_data:
                    self.user_data[name] = {}
                if album not in self.user_data.get(name):
                    self.user_data[name][album] = {}
                self.user_data[name][album][header] = value
        print("All values have been updated!")
        for name in self.user_data:
            self.generate_fig(name)
        self.generate_average_rating_over_time()
        print("New figures have been generated!")

    def file_updated(self, filepath):
        return os.path.exists(filepath) and datetime.fromtimestamp(os.path.getctime(filepath), tzlocal()) > self.latest_update

    @property
    @check_updates
    def names(self):
        if self.update_required():
            self.update_values()
        return list(self.user_data.keys())

    @check_updates
    def generate_fig(self, name):
        filepath = "data/%s.png" % name
        if self.file_updated(filepath):
            return
        fig, ax = plt.subplots()

        index = list(range(0, 11))
        bar_width = 0.7

        print("Generating new figure for %s." % name)
        ratings = self.people.get(name).get_ratings()
        counts  = [0] * 11
        max_amount = 20
        for rating in ratings:
            counts[rating] += 1

        plt.grid(color='gray', axis = 'y', linestyle='-', linewidth=1, alpha = 0.5)
        rects1 = ax.bar(index, counts, bar_width, color='lightskyblue', edgecolor='black')

        ax.set_xlabel('Rating')
        ax.set_ylabel('Amount')
        ax.set_title(name.title() + "'s Ratings")
        ax.set_xticks([float(i) for i in index])
        ax.set_xticklabels(list(map(str, index)))
        ax.set_ylim(bottom = -0.5, top = max_amount + 0.5)
        ax.set_xlim(left = -0.5, right = 11.5)
        plt.yticks(range(0, max_amount, 2), labels = [str(i) for i in range(0, max_amount, 2)])
        ax.set_axisbelow(True)
        fig.tight_layout()
        plt.savefig("data/%s.png" % name, bbox_inches='tight')

    @check_updates
    def get_likeness(self, person):
        if person not in self.people:
            return []
        print("Generating comparison list for %s." % str(person))
        likenesses = []
        for person2 in self.people:
            if person == person2:
                continue
            likenesses.append((person2, self.people.get(person).compare(self.people.get(person2))))
        likenesses = sorted(likenesses, key = lambda x: 0 if x[1] is None else -x[1])
        likenesses = [(name.title(), "%.2f" % (likeness * 100) if likeness is not None else "None") for name, likeness in likenesses]
        return likenesses

    @check_updates
    def generate_average_rating_over_time(self):
        filepath = "data/average_ratings_over_time.png"
        if self.file_updated(filepath):
            return
        fig, ax = plt.subplots()
        line_width = 1.0
        diff = 10

        print("Generating new average over time figure")
        ratings = [album.rating for album in self.albums if album.rating is not None]
        indexes = range(1, len(ratings) + 1)
        averages = [avg(ratings[0 if i - diff < 0 else i - diff:i]) for i in indexes]

        rects1 = ax.plot(indexes, averages, line_width, color='b')

        ax.set_xlabel('Album nr.')
        ax.set_ylabel('Average Rating')
        ax.set_title("Average Rating (%d Latest Ratings)" % diff)
        ax.set_ylim(bottom = -0.5, top = 10.5)
        ax.set_xlim(left = 0.5, right = indexes[-1] + 0.5)
        plt.yticks(range(11), labels = [str(i) for i in range(11)])
        fig.tight_layout()
        plt.savefig(filepath, bbox_inches='tight')
