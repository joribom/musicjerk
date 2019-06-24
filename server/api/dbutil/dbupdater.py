import re
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_time
from dateutil.tz import tzlocal
from threading import Thread, Lock
from collections import namedtuple
from server.externalapi.spotifyreader import get_spotify_data
from server.externalapi.wikireader import get_wiki_info, get_wiki_summary
from server.externalapi.discogsreader import get_genres
from . import dbmanager

Album = namedtuple('Album', 'week mandatory title artist selected_by url')
Rating = namedtuple('Rating', 'album_id uid rating best worst')

global updating, sheet, latest_update, latest_update_check, scope
updating = Lock()
sheet = None
latest_update_check = datetime.now(tzlocal())
latest_update = None
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1APR4vigWFUewWAMn1-iIML-4wKb0bWuS4f5xJW-KO2o'


def get_sheet_time():
    return sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='A1'
    ).execute().get('values')[0][0]


def get_all_values():
    print(get_sheet_time())
    return sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='A1:XX1000'
    ).execute().get('values')


def connect():
    global sheet, SCOPE

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPE)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()


def check_updates():
    start_in_thread(update_values)


def make_url(title, artist):
    url = '%s-%s' % (
        title.lower().strip().replace(" ", "_"),
        artist.lower().strip().replace(" ", "_")
    )
    url = re.sub(r'[^a-zA-Z0-9\_\-]', '', url)
    return url


def value_set(string):
    return string and string.strip() != '-'


def start_in_thread(func, *args):
    thread = Thread(target=func, args=tuple(args))
    thread.daemon = True
    thread.start()


def update_api_values(albums):
    for album_id, album in albums:
        if dbmanager.album_info_set(album_id):
            continue
        print("Fetching info about %s - %s..." % (
            str(album.artist), str(album.title)
        ))
        if album.title is not None and album.artist is not None:
            _, _, spotify_id, image_url = get_spotify_data(album.title,
                                                           album.artist)
            if image_url is None:
                summary, image_url = get_wiki_info(album.title, album.artist)
            else:
                summary = get_wiki_summary(album.title, album.artist)
            dbmanager.update_album_info(
                album_id, spotify_id,
                image_url, summary
            )


def update_slow_api_values(albums):
    for album_id, album in albums:
        if dbmanager.album_genres_set(album_id):
            continue
        print("Fetching slow info about %s - %s..." % (
            str(album.artist), str(album.title)
        ))
        genres, styles = get_genres(album.title, album.artist)
        dbmanager.update_album_genres(album_id, genres, styles)


def update_required():
    global sheet, latest_update, latest_update_check
    if datetime.now(tzlocal()) - latest_update_check < timedelta(minutes=5):
        return False
    latest_change_time = parse_time(get_sheet_time())
    latest_update_check = datetime.now(tzlocal())
    if latest_update < latest_change_time:
        print("Update required...")
    return latest_update < latest_change_time


def update_values():
    global updating, latest_update, latest_update_check
    if updating.locked():
        return
    if latest_update is not None and not update_required():
        return
    updating.acquire()
    print("Updating values from google sheets...")
    latest_update = datetime.now(tzlocal())
    connect()
    all_values = get_all_values()
    top_row = all_values[0]
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
    N = len(users) * 3 + 7
    for row in all_values[2:]:
        row += [''] * (N - len(row))
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
            rating, worst, best = None, None, None
            rating_str, best_str, worst_str = row[col:col+3]
            if value_set(rating_str):
                rating = int(rating_str)
            if value_set(best_str):
                best = list(map(str.strip, best_str.split(';')))
            if value_set(worst_str):
                worst = list(map(str.strip, worst_str.split(';')))
            dbmanager.update_rating(Rating(album_id, uid, rating, best, worst))
        index += 1
    print("Parsing albums finished!")
    start_in_thread(update_slow_api_values, albums[:])
    update_api_values(albums[:])
    updating.release()


if __name__ == "__main__":
    update_values()
