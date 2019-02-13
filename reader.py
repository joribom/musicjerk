import gspread, os
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_time
from dateutil.tz import tzlocal
from collections import OrderedDict
from person import Person
from album import Album, make_url
from copy import copy
from threading import Thread, Lock

def start_in_thread(func, args=()):
    thread = Thread(target=func, args=args)
    thread.daemon = True
    thread.start()

# Decorator for functions that use data from google sheets,
# to automatically check for new updates.
def check_updates(func):
    def wrapper(reader, *args):
        try:
            if reader.update_required():
                start_in_thread(reader.update_values)
        except Exception as e:
            print ("Caught an exception! '%s'" % str(e))
            reader.reconnect()
        return func(reader, *args)
    return wrapper

def avg(lst):
    return sum(lst) / len(lst)

class Reader:

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    def __init__(self):
        self.reconnect()
        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        self.latest_update_check = datetime.now(tzlocal())
        self._people = OrderedDict()
        self._albums = []
        self._album_dict = {}
        self.latest_update = None
        self.mutex    = Lock()
        self.updating = Lock()
        self.update_values()

    def user_exists(self, username):
        return username.lower() in self.people

    def reconnect(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', Reader.scope)
        client = gspread.authorize(creds)
        self.sheet = client.open("Musicjerk's big album sheet").sheet1

    @property
    @check_updates
    def albums(self):
        self.mutex.acquire()
        returnval = self._albums
        self.mutex.release()
        return returnval

    @property
    @check_updates
    def album_dict(self):
        self.mutex.acquire()
        returnval = self._album_dict
        self.mutex.release()
        return returnval

    @property
    @check_updates
    def people(self):
        self.mutex.acquire()
        returnval = self._people
        self.mutex.release()
        return returnval

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
        if self.updating.locked():
            return
        self.updating.acquire()
        print("Updating values from google sheets...")
        self.latest_update = datetime.now(tzlocal())
        all_values   = self.sheet.get_all_values()
        top_row      = all_values[0]
        col_headers  = all_values[1]
        new_people   = OrderedDict()
        for cell in top_row[5:]:
            name = cell.lower()
            if name and new_people.get(name) is None:
                new_people[name] = Person(name)
        self.general_data = {}
        self.user_data    = {}
        new_albums        = []
        new_album_dict    = {}
        for row in all_values[2:]:
            album        = row[0].replace(" (Optional)", '')
            if not album:
                break                                        # Break since no more albums present
            artist       = row[1]
            chosen_by    = row[2]
            average      = row[3]
            best_tracks  = row[4]
            worst_tracks = row[5]
            url = make_url(album, artist)
            if url in self._album_dict:
                new_albums.append(self._album_dict[url])
                new_albums[-1].update_values(chosen_by, average, best_tracks, worst_tracks)
            else:
                new_albums.append(Album(album, artist, chosen_by, average, best_tracks, worst_tracks))
            new_album_dict[url] = new_albums[-1]
            name = ""
            for col, value in enumerate(row[7:]):
                col    = col + 7
                name   = top_row[col].lower() if top_row[col] else name
                header = col_headers[col]
                new_people[name].add_value(album, header, value)
                if name not in self.user_data:
                    self.user_data[name] = {}
                if album not in self.user_data.get(name):
                    self.user_data[name][album] = {}
                self.user_data[name][album][header] = value
        for person in new_people.values():
            person.generate_likeness(new_people.values())
        self.mutex.acquire()
        self._albums     = copy(new_albums)
        self._album_dict = copy(new_album_dict)
        self._people     = copy(new_people)
        self.mutex.release()
        self.updating.release()
        start_in_thread(self.update_album_api_values)
        start_in_thread(self.update_slow_album_api_values)
        print("All values have been updated!")

    def update_album_api_values(self):
        print("Updating all albums from API calls...")
        for album in self._albums[::-1]:
            album.update_api_values()

    def update_slow_album_api_values(self):
        print("Updating all albums from API calls...")
        for album in self._albums[::-1]:
            album.update_slow_api_values()

    def file_updated(self, filepath):
        return os.path.exists(filepath) and datetime.fromtimestamp(os.path.getctime(filepath), tzlocal()) > self.latest_update

    @property
    @check_updates
    def names(self):
        return list(self.user_data.keys())

    @check_updates
    def get_likeness(self, person):
        if person not in self.people:
            return []
        return self.people.get(person).likeness_list
