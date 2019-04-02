import requests, re
from urllib import parse
from difflib import SequenceMatcher

session = requests.Session()
search_url = 'https://en.wikipedia.org/w/api.php?action=query&list=search&srlimit=5&srsearch={search_string}&utf8=&format=json'
summary_url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&pageids={pageid}'
filename_url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=images&pageids={pageid}'
image_url = 'https://en.wikipedia.org//w/api.php?action=query&titles=Image:{filename}&prop=imageinfo&iiprop=url&format=json'

def string_compare(string1, string2):
    seq = SequenceMatcher(None, " ".join(sorted(string1.lower().split())), " ".join(sorted(string2.lower().split())))
    return seq.ratio()

def best_pageid(results, album):
    pageid = None
    best_diff = 0
    for result in results:
        title = result['title'].lower()
        # Special case for titles such as "Superorganism (album by Superorganism)"
        if album.lower() in title and "album" in title:
            return str(result['pageid'])
        diff1 = string_compare(title, album + " " + "(album)")
        title = re.sub(r'\(.*?\)', '', title).strip()
        diff = max(string_compare(title, album), diff1)
        if diff < 0.8:
            continue
        if 'album' in title:
            return str(result['pageid'])
        if diff > best_diff:
            best_diff = diff
            pageid = result['pageid']
        elif pageid is None:
            pageid = result['pageid']
    return str(pageid) if pageid is not None else None

def best_match(possible_images, album, artist):
    image = None
    best_diff = 0
    album = album
    artist = artist
    for cur_image in possible_images:
        image_name = cur_image.replace("File:", '', 1)
        diff = string_compare(image_name.replace("_", ' '), album) + (string_compare(image_name.replace("_", ' '), artist) if album in image_name else 0)
        #print(album, artist, image_name, diff)
        if diff > best_diff:
            image = image_name
            best_diff = diff
        elif image is None:
            image = image_name
    return image

def get_page_id(search_string, album):
    try:
        search_string = search_string.replace(".", " ")
        #print("Attempting Wikipedia API call: %s" % search_url.format(search_string = parse.quote(search_string)))
        res = session.get(url = search_url.format(search_string = parse.quote(search_string))).json()
        pageid = best_pageid(res['query']['search'], album)
        return pageid
    except Exception as e:
        print("Could not find wiki page for '%s'. Exception: %s" % (search_string, str(e)))
        return None

def _get_summary(pageid):
    try:
        #print("Attempting Wikipedia API call: %s" % summary_url.format(pageid = pageid))
        res = session.get(url = summary_url.format(pageid = pageid)).json()
        summary = res['query']['pages'][pageid]['extract']
        return summary
    except Exception as e:
        print("Could not get wiki summary for pageid %s. Exception: %s" % (pageid, str(e)))
        return "No Wikipedia entry found for this album! :("

def get_image_url(pageid, album, artist):
    try:
        #print("Attempting Wikipedia API call: %s" % filename_url.format(pageid = pageid))
        res = session.get(url = filename_url.format(pageid = pageid)).json()
        images = res['query']['pages'][pageid]['images']
        possible_images = [image["title"] for image in images if not image["title"].lower().endswith(".svg") and not image["title"].lower().endswith(".ogg")]
        if len(possible_images) == 0:
            print("Found no images for %s by %s!" % (album, artist))
            return None
        else:
            image = best_match(possible_images, album, artist)
            if image is None:
                print("Found no matching image!")
                return None
            #print("Attempting Wikipedia API call: %s" % image_url.format(filename = parse.quote(image)))
            res = session.get(url = image_url.format(filename = parse.quote(image))).json()
            pages = res['query']['pages']
            return list(pages.values())[0]["imageinfo"][0]["url"]
    except Exception as e:
        print("Could not get image url for pageid %s. Exception: %s" % (pageid, str(e)))
        return None

def get_wiki_summary(album, artist):
    album  = re.sub('\s*\(.*?\)', '', album)
    artist = re.sub('\s*\(.*?\)', '', artist)
    pageid = get_page_id("%s %s" % (artist, album), album)
    if pageid is None:
        return "No Wikipedia entry found for this album! :("
    return _get_summary(pageid)

def get_wiki_info(album, artist):
    album  = re.sub('\s*\(.*?\)', '', album)
    artist = re.sub('\s*\(.*?\)', '', artist)
    pageid = get_page_id("%s %s" % (artist, album), album)
    if pageid is None:
        return "No Wikipedia entry found for this album! :(", None
    return _get_summary(pageid), get_image_url(pageid, album, artist)
