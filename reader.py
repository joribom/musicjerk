import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_time
from dateutil.tz import tzlocal
from person import Person
import os

# Decorator for functions that use data from google sheets,
# to automatically check for new updates.
def check_updates(func):
    def wrapper(reader, *args):
        if reader.update_required():
            reader.update_values()
        return func(reader, *args)
    return wrapper

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
        self.people = {}
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
            album        = row[0]
            if not album:
                break                                        # Break since no more albums present
            self.albums.append(album)
            artist       = row[1]
            chosen_by    = row[2]
            average      = row[3]
            best_tracks  = row[4]
            worst_tracks = row[5]
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

    @property
    @check_updates
    def names(self):
        if self.update_required():
            self.update_values()
        return list(self.user_data.keys())

    @check_updates
    def generate_fig(self, name):
        if self.update_required():
            self.update_values()
        filepath = "data/%s.png" % name
        if os.path.exists(filepath) and datetime.fromtimestamp(os.path.getctime(filepath), tzlocal()) > self.latest_update:
            return
        fig, ax = plt.subplots()

        index = list(range(0, 11))
        bar_width = 0.7
        opacity = 0.4

        print("Generating new figure for %s." % name)
        ratings = self.people.get(name).get_ratings()
        counts  = [0] * 11
        for rating in ratings:
            counts[rating] += 1

        rects1 = ax.bar(index, counts, bar_width,
                        alpha=opacity, color='b')

        ax.set_xlabel('Rating')
        ax.set_ylabel('Amount')
        ax.set_title(name.title() + "'s Ratings")
        ax.set_xticks([float(i) for i in index])
        ax.set_xticklabels(list(map(str, index)))
        ax.set_ylim(bottom = -0.5, top = 20.5)
        ax.set_xlim(left = -0.5, right = 11.5)
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
