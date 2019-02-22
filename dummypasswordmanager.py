import hashlib, uuid
from secrets import token_urlsafe # For cookie generation

default_username = 'debug'
default_password = 'debug'
default_uid      = '1'
default_session  = '-5mmo_aRB6Kck1rT8GNhpg'

access = None
refresh = None

def get_user_id(username):
    return default_uid if username == default_username else None

def login(username):
    if username == default_username:
        return default_uid, default_session
    return None, None

def set_tokens(uid, access_token, refresh_token):
    if uid == default_uid:
        access = access_token
        refresh = refresh_token


def get_tokens(uid):
    return access, refresh

def verify_login(uid, session):
    return uid == default_uid and session == default_session

def get_name(uid):
    return default_username if uid == default_uid else None


def add_password(user, password):
    pass

def check_password(user, password):
    return user == default_username and password == default_password
