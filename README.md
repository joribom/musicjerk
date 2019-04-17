# Musicjerk

Server for "The Musicjerk Project" (patent pending)

## Dependencies

* ```python3``` - Since the server runs in it
* ```gspread/oauth2client``` - For accessing the Google Sheet where each member enters their rating.
* ```flask/jinja2``` - For the server and template handling
* ```spotipy``` - For accessing albums on spotify
* ```lyricsgenius``` - For accessing lyrics from genius for the currently playing song
* ```discogs_client``` - For getting album genres/styles
* ```psycopg2``` - For database access in backend

## How to install
* Install python3
* Install pip3
* Run the command ```pip3 install oauth2client gspread jinja2 matplotlib spotipy flask lyricsgenius discogs_client psycopg2```
* Run the command ```pip3 install -r requirements.txt```

## How to run
```python3 server.py --nodb```

This will start the server on http://localhost:8000/ with no database connection. If you want to use a database, remove the 
```--nodb``` option, and create a psql server with name ```musicjerk```, then use ```db.sql``` to set up the database schema.
The master version of this server will always be running at https://bigmusicjerk.com/ , so feel free to check the 
webpage out there (runs on the master branch and pulls changes automatically through webhooks).
