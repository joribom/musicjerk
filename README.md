# Musicjerk

Server for "The Musicjerk Project" (patent pending)

## Dependencies

* Python3 - Since the server runs in it
* gspread/oauth2client - For accessing the Google Sheet where each member enters their rating.
* flask/jinja2 - For the server and template handling
* matplotlib - Used to plot graphs (DEPRECATED? Otherwise, soon to be deprecated)
* spotipy - For accessing albums on spotify
* lyricsgenius - For accessing lyrics from genius for the currently playing song
* discogsclient - For getting album genres/styles

## How to install
* Install python3
* Install pip3
* Run the command ```pip3 install oauth2client gspread jinja2 matplotlib spotipy flask lyricsgenius discogsclient```

## How to run
```python3 server.py```

This will start the server on http://localhost:8000/ .
The master version of this server will always be running at http://bigmusicjerk.com/ , so feel free to check the 
webpage out there (runs on the master branch and pulls changes automatically through webhooks).
