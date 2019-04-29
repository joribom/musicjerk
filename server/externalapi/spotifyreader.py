import spotipy, json, re
from pprint import pprint
from spotipy.oauth2 import SpotifyClientCredentials

with open('spotify_secret.json', 'r') as f:
    data = json.load(f)


client_credentials_manager = SpotifyClientCredentials(
    client_id=data["client_id"],
    client_secret=data["client_secret"]
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_client_id():
    return data['client_id']


def get_spotify_image(album, artist):
    try:
        album = re.sub(r"\s*\(.*?\)", "", album)
        results = sp.search(
            q='album:%s artist:%s' % (album, artist),
            type='album'
        )
        return results['albums']['items'][0]['images'][0]['url']
    except (KeyError, IndexError):
        return None


def get_spotify_data(album, artist):
    try:
        album = re.sub(r"\s*\(.*?\)", "", album)
        album_str = ('album:%s' % album if album else '')
        artist_str = (
            (' ' if album else '')
            + ('artist:%s' % artist if artist else '')
        )
        results = sp.search(
            q=album_str + artist_str,
            type='album'
        )
        album_data = results['albums']['items'][0]
        ret = (
            album_data['name'],
            album_data['artists'][0]['name'],
            album_data['id'],
            album_data['images'][0]['url']
        )
        return ret
    except (KeyError, IndexError):
        return None, None, None, None
