import hashlib, uuid, psycopg2

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
    cur.execute("SELECT id FROM users WHERE name=%s", (username,))
    return cur.fetchone()

@using_db
def add_password(cur, user, password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512((password + salt).encode("ascii")).hexdigest()
    cur.execute("INSERT INTO passwords VALUES ((SELECT uid FROM users WHERE name='%s'), '%s', '%s');" % (user, hashed_password, salt))

@using_db
def check_password(cur, user, password):
    cur.execute("SELECT hash, salt FROM users NATURAL JOIN passwords WHERE name=%s", (user,))
    stored_hash, salt = cur.fetchone()
    hash = hashlib.sha512((password + salt).encode("ascii")).hexdigest()
    return hash == stored_hash

if __name__ == "__main__":
    print(check_password("Johan", "test"))
