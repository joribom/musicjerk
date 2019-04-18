import psycopg2
import psycopg2.extras

conn = psycopg2.connect("dbname=musicjerk user=postgres")
conn.set_client_encoding('UTF-8')
cur = conn.cursor()


def fst(x):
    return x[0] if x is not None else None


def using_db(func):
    def wrapper(*args, **kwargs):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
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
        rating=%s
        WHERE
        album_id=%s AND uid=%s;
    """
    cur.execute(command, (rating, album_id, uid))


def update_rating(rating):
    """Rating = namedtuple('Rating', 'album_id uid rating best worst')"""
    if not _rating_exists(
            rating.album_id,
            rating.uid):
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


@using_db
def update_album_info(cur, album_id, spotify_id, image_url, summary):
    command = """
        UPDATE albums SET
        image_url=%s, summary=%s, spotify_id=%s
        WHERE
        id=%s
    """
    cur.execute(command, (image_url, summary, spotify_id, album_id))


@using_db
def update_album_genres(cur, album_id, genres, styles):
    command = """
        UPDATE albums SET
        genres=%s, styles=%s
        WHERE
        id=%s
    """
    cur.execute(command, (genres, styles, album_id))


@using_db
def album_info_set(cur, album_id):
    command = 'SELECT spotify_id, image_url, summary FROM albums WHERE id=%s'
    cur.execute(command, (album_id,))
    res = fst(cur.fetchone())
    return all(map(lambda x: bool(x), res)) if res else False


@using_db
def album_genres_set(cur, album_id):
    command = 'SELECT genres, styles FROM albums WHERE id=%s'
    cur.execute(command, (album_id,))
    res = fst(cur.fetchone())
    return all(map(lambda x: bool(x), res)) if res else False
