import hashlib, uuid, psycopg2
from secrets import token_urlsafe # For cookie generation

conn = psycopg2.connect("dbname=musicjerk user=postgres")
cur = conn.cursor()
fst = lambda x: x[0] if x is not None else None
snd = lambda x: x[1] if x is not None else None

def using_db(func):
    def wrapper(*args, **kwargs):
        cur = conn.cursor()
        try:
            result = func(cur, *args, **kwargs)
            conn.commit()
            cur.close()
            return result
        except Exception as e:
            print(str(e))
            conn.rollback()
            cur.close()
            return None
    return wrapper

@using_db
def get_user_id(cur, username):
    cur.execute("SELECT uid, cookie FROM users WHERE name=%s;", (username.lower(),))
    return cur.fetchone()

@using_db
def login(cur, username):
    cur.execute("SELECT uid FROM users WHERE name=%s;", (username.lower(),))
    uid = fst(cur.fetchone())
    print(uid)
    session = token_urlsafe(16);
    cur.execute("UPDATE users SET session=%s WHERE uid=%s;", (session, uid))
    return uid, session

@using_db
def set_tokens(cur, uid, access_token, refresh_token):
    cur.execute('UPDATE spotify_tokens SET access_token=%s, refresh_token=%s WHERE uid=%s',
        (access_token, refresh_token, uid)
    )

@using_db
def get_tokens(cur, uid):
    cur.execute('SELECT access_token, refresh_token FROM spotify_tokens WHERE uid=%s', (uid,))
    return cur.fetchone();

@using_db
def verify_login(cur, uid, session):
    cur.execute("SELECT session FROM users WHERE uid=%s;", (uid,))
    res = cur.fetchone()
    return session is not None and fst(res) == session

@using_db
def get_name(cur, uid):
    cur.execute("SELECT name FROM users WHERE uid=%s;", (uid,))
    res = cur.fetchone()
    return fst(res)


@using_db
def add_password(cur, user, password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512((password + salt).encode("ascii")).hexdigest()
    cur.execute("INSERT INTO passwords VALUES ((SELECT uid FROM users WHERE name=%s), %s, %s);", (user.lower(), hashed_password, salt))

@using_db
def check_password(cur, user, password):
    cur.execute("SELECT hash, salt FROM users NATURAL JOIN passwords WHERE name=%s;", (user.lower(),))
    stored_hash, salt = cur.fetchone()
    hash = hashlib.sha512((password + salt).encode("ascii")).hexdigest()
    return hash == stored_hash


@using_db
def _album_id_exists(cur, album_id):
    command = 'SELECT EXISTS(SELECT 1 FROM albums WHERE id=%s);'
    cur.execute(command, (album_id,))
    return fst(cur.fetchone())

@using_db
def _get_uid(cur, name):
    command = 'SELECT uid FROM users WHERE name=%s;'
    cur.execute(command, (name,))
    return fst(cur.fetchone())

@using_db
def _add_user(cur, name):
    command = 'INSERT INTO users (name) VALUES (%s) RETURNING uid;'
    cur.execute(command, (name,))
    return fst(cur.fetchone())

def get_user_uid(name):
    uid = _get_uid(name)
    if uid is None:
        uid = _add_user(name)
    return uid

@using_db
def _get_album_id(cur, week, mandatory):
    command = 'SELECT id FROM albums where week=%s AND mandatory=%s;'
    cur.execute(command, (week, mandatory))
    return fst(cur.fetchone())

@using_db
def _add_album(cur, week, mandatory, title, artist, selected_by, url):
    command = """
        INSERT INTO albums
        (week, mandatory, title, artist, selected_by, url)
        VALUES
        (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """
    cur.execute(command, (week, mandatory, title, artist, selected_by, url))
    return fst(cur.fetchone())

@using_db
def _update_album(cur, album_id, title, artist, selected_by, url):
    command = """
        UPDATE albums SET
        title=%s, artist=%s, selected_by=%s, url=%s
        WHERE
        id=%s;
    """
    cur.execute(command, (title, artist, selected_by, url, album_id))

def update_album(album):
    """Album = namedtuple('Album', 'week mandatory title artist selected_by url')"""
    album_id = _get_album_id(album.week, album.mandatory)
    if album_id is None:
        album_id = _add_album(
            album.week,
            album.mandatory,
            album.title,
            album.artist,
            album.selected_by,
            album.url
        )
    else:
        _update_album(
            album_id,
            album.title,
            album.artist,
            album.selected_by,
            album.url
        )
    return album_id

@using_db
def _rating_exists(cur, album_id, uid):
    command = """
        SELECT EXISTS(
            SELECT 1 FROM ratings
            WHERE album_id=%s AND uid=%s
        );
    """
    cur.execute(command, (album_id, uid))
    return fst(cur.fetchone())

@using_db
def _insert_rating(cur, album_id, uid, rating):
    command = """
        INSERT INTO ratings (album_id, uid, rating)
        VALUES
        (%s, %s, %s);
    """
    cur.execute(command, (album_id, uid, rating))

@using_db
def _update_rating(cur, album_id, uid, rating):
    command = """
        UPDATE ratings SET
        album_id=%s, uid=%s
        WHERE
        rating=%s;
    """
    cur.execute(command, (album_id, uid, rating))

def update_rating(rating):
    """Rating = namedtuple('Rating', 'album_id uid rating best worst')"""
    if not _rating_exists(
            rating.album_id,
            rating.uid
        ):
        _insert_rating(
            rating.album_id,
            rating.uid,
            rating.rating
        )
    else:
        _update_rating(
            rating.album_id,
            rating.uid,
            rating.rating
        )

if __name__ == "__main__":
    from collections import namedtuple
    Album = namedtuple('Album', 'week mandatory title artist selected_by url')
    Rating = namedtuple('Rating', 'album_id uid rating best worst')
    url = '%s-%s' % ('Title'.lower().replace(" ", "_"), 'Artist'.lower().replace(" ", "_"))
    uid = 2
    album = Album(1, True, 'Title', 'Artist', uid, url)
    album_id = update_album(album)
    update_rating(Rating(album_id, uid, 7, ['Best1', 'Best 2'], ['Worst 1', 'Worst2']))
    #update_rating(Rating(album_id, 91, 7, None, ['Worst 1', 'Worst2']))
    #update_rating(Rating(album_id, 92, None, None, None))
