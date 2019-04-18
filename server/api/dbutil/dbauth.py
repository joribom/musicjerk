import hashlib
import uuid
from secrets import token_urlsafe  # For cookie generation
from .dbmanager import using_db, fst


@using_db
def get_user_id(cur, username):
    command = """
        SELECT uid, cookie
        FROM users
        WHERE name=%s;
    """
    cur.execute(command, (username.lower(),))
    return cur.fetchone()


@using_db
def login(cur, username):
    cur.execute("SELECT uid FROM users WHERE name=%s;", (username.lower(),))
    uid = fst(cur.fetchone())
    session = token_urlsafe(16)
    cur.execute("UPDATE users SET session=%s WHERE uid=%s;", (session, uid))
    return uid, session


@using_db
def set_tokens(cur, uid, access_token, refresh_token):
    command = """
        UPDATE spotify_tokens
        SET access_token=%s, refresh_token=%s
        WHERE uid=%s
    """
    cur.execute(command, (access_token, refresh_token, uid))


@using_db
def get_tokens(cur, uid):
    command = """
        SELECT access_token, refresh_token
        FROM spotify_tokens
        WHERE uid=%s
    """
    cur.execute(command, (uid,))
    return cur.fetchone()


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
def add_password(cur, userid, password):
    command = """
        INSERT INTO passwords
        VALUES (%s, %s, %s);
    """
    salt = uuid.uuid4().hex
    salted_password = (password + salt).encode("ascii")
    hashed_password = hashlib.sha512(salted_password).hexdigest()
    cur.execute(command, (userid, hashed_password, salt))


@using_db
def check_password(cur, user, password):
    command = """
        SELECT hash, salt
        FROM users NATURAL JOIN passwords
        WHERE name=%s;
    """
    cur.execute(command, (user.lower(),))
    stored_hash, salt = cur.fetchone()
    hash = hashlib.sha512((password + salt).encode("ascii")).hexdigest()
    return hash == stored_hash


@using_db
def _set_default_passwords(cur):
    command = """
        SELECT users.uid
        FROM users LEFT OUTER JOIN passwords
        ON users.uid=passwords.uid
        WHERE hash IS NULL;
    """
    cur.execute(command)
    for row in cur.fetchall():
        uid = row['uid']
        add_password(uid, 'password')


# Set default passwords when this module is imported
_set_default_passwords()
