import gspread
import re
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_time
from dateutil.tz import tzlocal
from threading import Thread, Lock
from collections import namedtuple
from .externalapi.spotifyreader import get_spotify_data
from .externalapi.wikireader import get_wiki_info, get_wiki_summary
from .externalapi.discogsreader import get_genres
from . import dbmanager

Album = namedtuple('Album', 'week mandatory title artist selected_by url')
Rating = namedtuple('Rating', 'album_id uid rating best worst')

global updating, sheet, latest_update, latest_update_check, scope
updating = Lock()
sheet = None
latest_update_check = datetime.now(tzlocal())
latest_update = None
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


def check_updates():
    start_in_thread(update_values)


def make_url(title, artist):
    url = '%s-%s' % (title.lower().strip().replace(" ", "_"), artist.lower().strip().replace(" ", "_"))
    url = re.sub('[^a-zA-Z0-9\_\-]', '', url)
    return url

def start_in_thread(func, *args):
    thread = Thread(target=func, args=tuple(args))
    thread.daemon = True
    thread.start()

def update_api_values(albums):
    for album_id, album in albums:
        if dbmanager.album_info_set(album_id):
            continue
        print("Fetching info about %s - %s..." % (str(album.artist), str(album.title)))
        if album.title is not None and album.artist is not None:
            spotify_id, image_url = get_spotify_data(album.title, album.artist)
            if image_url is None:
                summary, image_url = get_wiki_info(album.title, album.artist)
            else:
                summary = get_wiki_summary(album.title, album.artist)
            dbmanager.update_album_info(album_id, spotify_id, image_url, summary)


def update_slow_api_values(albums):
    for album_id, album in albums:
        if dbmanager.album_genres_set(album_id):
            continue
        print("Fetching slow info about %s - %s..." % (str(album.artist), str(album.title)))
        genres, styles = get_genres(album.title, album.artist)
        dbmanager.update_album_genres(album_id, genres, styles)


def update_required():
    global sheet, latest_update, latest_update_check
    if datetime.now(tzlocal()) - latest_update_check < timedelta(minutes = 5):
        return False
    latest_change_time = parse_time(sheet.cell(1, 1).value)
    latest_update_check = datetime.now(tzlocal())
    if latest_update < latest_change_time:
        print("Update required...")
    return latest_update < latest_change_time


def connect():
    global sheet, scope
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Musicjerk's big album sheet").sheet1

def update_values():
    global updating, sheet, latest_update, latest_update_check
    if updating.locked():
        return
    if latest_update is not None and not update_required():
        return
    updating.acquire()
    print("Updating values from google sheets...")
    latest_update = datetime.now(tzlocal())
    connect()
    all_values = sheet.get_all_values()
    top_row = all_values[0]
    col_headers = all_values[1]
    users = {}
    print("Parsing users...")
    for cell in top_row[5:]:
        name = cell.lower()
        if name and name not in users:
            uid = dbmanager.get_user_uid(name)
            users[name] = uid

    print("Parsing users finished!")
    index = 3
    albums = []
    print("Parsing albums...")
    for row in all_values[2:]:
        title = re.sub(r'\([^\)]*\)', '', row[0])
        if not title:
            break
        artist = row[1]
        chosen_by = dbmanager.get_user_uid(row[2].lower())
        url = make_url(title, artist)
        week = int(index / 2)
        mand = (index == 3) or ((index % 2) == 0)
        album = Album(week, mand, title, artist, chosen_by, url)
        album_id = dbmanager.update_album(album)
        albums.append((album_id, album))
        for col in range(7, len(row), 3):
            name = top_row[col].lower()
            uid = dbmanager.get_user_uid(name)
            rating_str = row[col]
            rating = int(rating_str) if rating_str and rating_str.strip() != '-' else None
            best_str = row[col + 1]
            best = list(map(str.strip, best_str.split(';'))) if best_str and best_str.strip() != '-' else None
            worst_str = row[col + 2]
            worst = list(map(str.strip, worst_str.split(';'))) if worst_str and worst_str.strip() != '-' else None
            dbmanager.update_rating(Rating(album_id, uid, rating, best, worst))
        index += 1
    print("Parsing albums finished!")
    start_in_thread(update_slow_api_values, albums[:])
    update_api_values(albums[:])
    updating.release()


if __name__ == "__main__":
    update_values()
