import requests

"https://en.wikipedia.org/w/api.php?action=query&list=search&srlimit=1&srsearch=Yoshimi%20Battles%20The%20Pink%20Robots%20The%20Flaming%20Lips%20Album&utf8=&format=json"
session = requests.Session()
search_url = 'https://en.wikipedia.org/w/api.php?action=query&list=search&srlimit=1&srsearch={search_string}&utf8=&format=json'
summary_url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&pageids={pageid}'
filename_url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=images&pageids={pageid}'
image_url = 'https://en.wikipedia.org//w/api.php?action=query&titles=Image:{filename}&prop=imageinfo&iiprop=url&format=json'

def get_page_id(search_string):
    try:
        res = session.get(url = search_url.format(search_string = search_string)).json()
        pageid = str(res['query']['search'][0]['pageid'])
        return pageid
    except Exception as e:
        print("Could not find wiki page for '%s'. Exception: %s" % (search_string, str(e)))

def get_summary(pageid):
    try:
        res = session.get(url = summary_url.format(pageid = pageid)).json()
        summary = res['query']['pages'][pageid]['extract']
        return summary
    except Exception as e:
        print("Could not get wiki summary for pageid %s. Exception: %s" % (pageid, str(e)))
        return None

def get_image_url(pageid):
    try:
        res = session.get(url = filename_url.format(pageid = pageid)).json()
        images = res['query']['pages'][pageid]['images']
        possible_images = [image["title"] for image in images if (".png" in image["title"] or ".jpg" in image["title"])]
        if len(possible_images) == 0:
            return None
        elif len(possible_images) == 1:
            res = session.get(url = image_url.format(filename = possible_images[0][5:])).json()
            pages = res['query']['pages']
            return list(pages.values())[0]["imageinfo"][0]["url"]
    except Exception as e:
        print("Could not get image url for pageid %s. Exception: %s" % (pageid, str(e)))
        return None

def get_wiki_info(album, artist):
    pageid = get_page_id(album + " " + artist + " album")
    return get_summary(pageid), get_image_url(pageid)



if __name__ == "__main__":
    print(get_wiki_info("Origin of Symmetry", "Muse"))
