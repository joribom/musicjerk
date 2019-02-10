import spotipy, json, re
from spotipy.oauth2 import SpotifyClientCredentials

with open('spotify_secret.json', 'r') as f:
    data = json.load(f)

client_credentials_manager = SpotifyClientCredentials(client_id = data["client_id"], client_secret = data["client_secret"])
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def get_spotify_image(album, artist):
    try:
        album = re.sub("\s*\(.*?\)", "", album)
        results = sp.search(q = 'album:%s artist:%s' % (album, artist), type = 'album')
        return results['albums']['items'][0]['images'][0]['url']
    except (KeyError, IndexError) as e:
        return None
