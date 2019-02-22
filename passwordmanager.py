import hashlib, uuid, psycopg2
from secrets import token_urlsafe # For cookie generation

conn = psycopg2.connect("dbname=musicjerk user=postgres")
cur = conn.cursor()

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
    uid = cur.fetchone()[0]
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
    return (res[0] == session) if res is not None else False

@using_db
def get_name(cur, uid):
    cur.execute("SELECT name FROM users WHERE uid=%s;", (uid,))
    res = cur.fetchone()
    return res[0] if res is not None else None


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

if __name__ == "__main__":
    print(check_password("johan", "test"))
