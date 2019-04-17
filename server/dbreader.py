from . import dbupdater
import psycopg2
from .dbmanager import using_db as using_db_inner

dbupdater.check_updates()

def using_db(func):
    def wrapper(*args, **kwargs):
        dbupdater.check_updates()
        new_func = using_db_inner(func)
        result = new_func(*args, **kwargs)
        return result
    return wrapper

fst = lambda x: x[0] if x is not None else None

@using_db
def get_albums_basic(cur):
    command = """
        SELECT title, artist, url, image_url
        FROM albums
        ORDER BY week DESC, mandatory DESC;
    """
    cur.execute(command)
    albums = cur.fetchall()
    data = []
    for i in range(0, len(albums) - 1, 2):
        mand = albums[i]
        opt = albums[i + 1]
        data.append((
            {'name': mand[0], 'artist': mand[1], 'url' : mand[2], 'image' : mand[3]},
            {'name': opt[0], 'artist': opt[1], 'url' : opt[2], 'image' : opt[3]}))
    mand = albums[-1]
    data.append(({'name': mand[0], 'artist': mand[1], 'url' : mand[2], 'image' : mand[3]}, None))
    return data

@using_db
def get_this_weeks_albums(cur):
    command = """
        SELECT title, artist, url, image_url
        FROM albums
        ORDER BY week DESC, mandatory DESC
        LIMIT 2;
    """
    cur.execute(command)
    mand, opt = cur.fetchall()
    data = (
        {'name': mand[0], 'artist': mand[1], 'url' : mand[2], 'image' : mand[3]},
        {'name': opt[0], 'artist': opt[1], 'url' : opt[2], 'image' : opt[3]})
    return data


@using_db
def get_members(cur):
    command = """
        SELECT name
        FROM users NATURAL JOIN ratings
        GROUP BY uid
        ORDER BY uid ASC;"""
    cur.execute(command)
    return list(map(fst, cur.fetchall()))

@using_db
def get_member_info(cur, name):
    command = """
        SELECT rating, title, url
        FROM ratings NATURAL JOIN users LEFT OUTER JOIN albums
        ON ratings.album_id=albums.id
        WHERE name=%s AND rating IS NOT NULL
        ORDER BY week ASC, mandatory DESC;
    """
    cur.execute(command, (name,))
    ratings = []
    for i, info in enumerate(cur.fetchall()):
        ratings.append({'y': info[0], 'x': i, 'title': info[1], 'url': info[2]})
    data = {'likeness': None, 'albums': ratings}
    return data


@using_db
def get_album(cur, albumname):
    command = """
        SELECT title, artist, summary, genres, styles, spotify_id, image_url
        FROM albums
        WHERE url=%s;
    """
    print(command)
    cur.execute(command, (albumname,))
    info = cur.fetchone()
    print(info)
    data = dict(zip([
        'name', 'artist', 'summary', 'genres',
        'styles', 'spotify_id', 'image'
        ], info)) if info is not None else {}
    return data

@using_db
def get_album_averages(cur):
    command = """
        SELECT title, score, url
        FROM albums
        ORDER BY week ASC, mandatory DESC;
    """
    cur.execute(command)
    avgs = []
    for i, info in enumerate(cur.fetchall()):
        avgs.append({
            "title": info[0],
            "x": i,
            "y": round(float(info[1]), 2) if info[1] is not None else None,
            "url": info[2]})
    return avgs

if __name__ == "__main__":
    #print(get_albums_basic())
    #print(get_this_weeks_albums())
    #print(get_members())
    #print(
    print(get_album_averages())
