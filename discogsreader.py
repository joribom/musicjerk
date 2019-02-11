import discogs_client, json, re
from pprint import pprint
from datetime import datetime, timedelta
from time import sleep

latest_fetch = datetime.now()

with open('discogs_secret.json', 'r') as f:
    data = json.load(f)
token = data['token']

client = discogs_client.Client('MusicjerkServer/0.1', user_token=token)

def get_genres(album, artist):
    try:
        album = re.sub('\s*\(.*?\)', '', album)
        artist = re.sub('\s*\(.*?\)', '', artist)
        global latest_fetch
        if datetime.now() - latest_fetch < timedelta(seconds = 1.5):
            sleep((timedelta(seconds = 3) - (datetime.now() - latest_fetch)).total_seconds())
        results = client.search(album + " " + artist, type='release')
        if not results:
            results = client.search(album, type='release')
        latest_fetch = datetime.now()
        return results[0].genres, results[0].styles
    except Exception:
        return [], []

if __name__ == "__main__":
    print(get_genres("People who can eat people are the luckiest people in the world", "AJJ"))
