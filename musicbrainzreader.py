import requests, re
from pprint import pprint
from urllib import parse
from datetime import datetime, timedelta
from time import sleep

session = requests.Session()
search_url = 'https://musicbrainz.org/ws/2/release?query="{search_string}"&fmt=json'
release_group_url = 'https://musicbrainz.org/ws/2/release-group/{group_id}?inc=tags+releases&fmt=json'
release_url = 'https://musicbrainz.org/ws/2/release/{release_id}?inc=recordings&fmt=json'

latest_fetch = datetime.now()

def get_release_group(album, artist):
    try:
        data = session.get(url = search_url.format(search_string = parse.quote(album))).json()
        global latest_fetch
        latest_fetch = datetime.now()
        for rel_group in data['releases']:
            try:
                for credit in rel_group['artist-credit']:
                    if credit['artist']['name'] == artist:
                        break
                else:
                    continue
                if rel_group['status'] != 'Official' or rel_group['release-group']['primary-type'] != 'Album':
                    continue
                return rel_group['release-group']['id']
            except KeyError:
                continue
        return None
    except Exception as e:
        print("Could not find musicbrainz page for '%s'. Exception: %s" % (album, str(e)))
        return None

def get_release(group_id):
    try:
        data = session.get(url = release_group_url.format(group_id = parse.quote(group_id))).json()
        tags = [(tag['name'], tag['count']) for tag in data['tags']]
        tags = ["%s (%s)" % tag for tag in sorted(tags, key = lambda x: -int(x[1]))]
        release = None
        for current in data['releases']:
            if current['status'] == 'Official':
                release = current['id']
                break
        return tags, release
    except Exception as e:
        print("Could not find musicbrainz release for '%s'. Exception: %s" % (group_id, str(e)))
        return [], None

def get_tracks(release_id):
    try:
        data = session.get(url = release_url.format(release_id = parse.quote(release_id))).json()
        tracks = data['media'][0]['tracks']
        tracklist = [track['title'] for track in tracks]
        return tracklist
    except Exception as e:
        print("Could not find musicbrainz tracks for '%s'. Exception: %s" % (release_id, str(e)))
        return None

def get_album_info(album, artist):
    if datetime.now() - latest_fetch < timedelta(seconds = 3):
        sleep((timedelta(seconds = 3) - (datetime.now() - latest_fetch)).total_seconds())
    group_id = get_release_group(album, artist)
    if group_id is None:
        return [], None
    tags, release = get_release(group_id)
    if release is not None:
        tracks = get_tracks(release)
        return tags, tracks
    return tags, None
