import gspread, os, re
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_time
from dateutil.tz import tzlocal
from threading import Thread, Lock
from collections import namedtuple, OrderedDict
import dbmanager


def make_url(title, artist):
    return '%s-%s' % (title.lower().replace(" ", "_"), artist.lower().replace(" ", "_"))

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

Album = namedtuple('Album', 'week mandatory title artist selected_by url')
Rating = namedtuple('Rating', 'album_id uid rating best worst')

updating = Lock()
latest_update_check = datetime.now(tzlocal())
latest_update = None
mutex = Lock()
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

def connect():
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Musicjerk's big album sheet").sheet1
    return sheet

def update_values():
    if updating.locked():
        return
    updating.acquire()
    print("Updating values from google sheets...")
    latest_update = datetime.now(tzlocal())
    sheet = connect()
    all_values = sheet.get_all_values()
    top_row = all_values[0]
    col_headers = all_values[1]
    users = {}
    for cell in top_row[5:]:
        name = cell.lower()
        if name and name not in users:
            uid = dbmanager.get_user_uid(name)
            users[name] = uid

    index = 3
    for row in all_values[2:]:
        title = re.sub('\([^\)]*\)', '', row[0])
        if not title:
            break
        artist = row[1]
        chosen_by = dbmanager.get_user_uid(row[2].lower())
        url = make_url(title, artist)
        week = int(index / 2)
        mand = (index == 3) or ((index % 2) == 0)
        #print(Album(week, mand, title, artist, chosen_by))
        #hash = str(index)
        album_id = dbmanager.update_album(Album(week, mand, title, artist, chosen_by, url))
        for col in range(7, len(row), 3):
            name = top_row[col].lower()
            uid = users.get(name)
            rating_str = row[col]
            rating = int(rating_str) if rating_str and rating_str.strip() != '-' else None
            best_str = row[col + 1]
            best = list(map(str.strip, best_str.split(';'))) if best_str and best_str.strip() != '-' else None
            worst_str = row[col + 2]
            worst = list(map(str.strip, worst_str.split(';'))) if worst_str and worst_str.strip() != '-' else None
            #print('    ' + str(Rating(hash, uid, rating, best, worst)))
            dbmanager.update_rating(Rating(album_id, uid, rating, best, worst))
        index += 1

if __name__ == "__main__":
    update_values()
