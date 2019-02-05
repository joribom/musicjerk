import requests

"https://en.wikipedia.org/w/api.php?action=query&list=search&srlimit=1&srsearch=Yoshimi%20Battles%20The%20Pink%20Robots%20The%20Flaming%20Lips%20Album&utf8=&format=json"
session = requests.Session()
search_url = 'https://en.wikipedia.org/w/api.php?action=query&list=search&srlimit=10&srsearch={search_string}&utf8=&format=json'
summary_url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&pageids={pageid}'
filename_url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=images&pageids={pageid}'
image_url = 'https://en.wikipedia.org//w/api.php?action=query&titles=Image:{filename}&prop=imageinfo&iiprop=url&format=json'

def best_match(possible_images, album, artist):
    image = None
    match = False
    best_res = 100000
    album = album.lower().replace(" ", '').replace("_", '')
    artist = artist.lower().replace(" ", '').replace("_", '')
    print(album)
    for cur_image in possible_images:
        image_name = cur_image.replace("File:", '', 1)
        image_match_string = image_name.lower().replace(" ", '').replace("_", '')
        if album in image_match_string:
            match = True
            res = len(image_match_string.replace(album, '').replace(artist, ''))
            if res < best_res:
                image = image_name
                best_res = res
        elif not match:
            image = image_name
    return image.replace('&', '%26')


def get_page_id(search_string):
    try:
        print("Attempting Wikipedia API call: %s" % search_url.format(search_string = search_string))
        res = session.get(url = search_url.format(search_string = search_string)).json()
        #for page in res['query']['search']:
            #page['pageid']
        pageid = str(res['query']['search'][0]['pageid'])
        return pageid
    except Exception as e:
        print("Could not find wiki page for '%s'. Exception: %s" % (search_string, str(e)))
        return None

def get_summary(pageid):
    try:
        print("Attempting Wikipedia API call: %s" % summary_url.format(pageid = pageid))
        res = session.get(url = summary_url.format(pageid = pageid)).json()
        summary = res['query']['pages'][pageid]['extract']
        return summary
    except Exception as e:
        print("Could not get wiki summary for pageid %s. Exception: %s" % (pageid, str(e)))
        return None

def get_image_url(pageid, album, artist):
    try:
        print("Attempting Wikipedia API call: %s" % filename_url.format(pageid = pageid))
        res = session.get(url = filename_url.format(pageid = pageid)).json()
        images = res['query']['pages'][pageid]['images']
        possible_images = [image["title"] for image in images if (".png" in image["title"].lower() or ".jpg" in image["title"].lower())]
        if len(possible_images) == 0:
            print("Found no images for %s by %s!" % (album, artist))
            return None
        else:
            image = best_match(possible_images, album, artist)
            print("Attempting Wikipedia API call: %s" % image_url.format(filename = image))
            res = session.get(url = image_url.format(filename = image)).json()
            pages = res['query']['pages']
            return list(pages.values())[0]["imageinfo"][0]["url"]
    except Exception as e:
        print("Could not get image url for pageid %s. Exception: %s" % (pageid, str(e)))
        return None

def get_wiki_info(album, artist):
    album = album.replace('&', '%26')
    artist = artist.replace('&', '%26')
    pageid = get_page_id((album + " (Album)"))
    if pageid is None:
        return "No Wikipedia entry for this album! :(", None
    return get_summary(pageid), get_image_url(pageid, album, artist)
