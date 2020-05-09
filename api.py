import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import re
import json

from dotenv import load_dotenv
load_dotenv()


def spotifyQuery(search_phrase: str):
    try:
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret,
        )
        sp = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager
        )  # spotify object to access API
    except:
        print("Wrong Auth for Spotify", file=sys.stderr)
        return "Wrong Auth for Spotify"
    url = sp.search(search_phrase, limit=1, type="playlist")[
        "playlists"]["items"][0]["external_urls"]["spotify"]
    if url == None or url == "":
        return "No playlist found"
    url = url.replace("/playlist","/embed/playlist")
    return url


def tenorQuery(search_phrase: str):

    try:
        api_key = os.getenv("TENOR_API_KEY")
    except:
        print("Wrong Auth for Tenor", file=sys.stderr)
        return "Wrong Auth for Tenor"

    r = requests.get(
        "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s"
        % (search_phrase, api_key, 4)
    )

    if r.status_code == 200:
        gif = json.loads(r.content)
        links = []
        for result in gif["results"]:
            links.append(result["media"][0]["gif"]["url"])
        return links
    else:
        return "No GIF found"


def youtubeQuery(search_phrase: str):

    try:
        api_key = os.getenv("YT_KEY")
    except:
        print("Wrong Auth for YT", file=sys.stderr)
        return "Wrong Auth for YT"

    search_url = "https://www.googleapis.com/youtube/v3/search"
    video_url = "https://www.googleapis.com/youtube/v3/videos"

    search_params = {
        "key": api_key,
        "q": search_phrase,
        "part": "snippet",
        "maxResults": 1,
        "type": "video",
        "videoEmbeddable": "true",
    }

    r = requests.get(search_url, params=search_params)

    if r.status_code == 200:

        results = r.json()["items"]

        video_ids = []

        for result in results:
            video_ids.append(result["id"]["videoId"])

        video_params = {
            "key": os.getenv("YT_KEY"),
            "id": ",".join(video_ids),
            "part": "player",
            "maxResults": 1,
        }

        r = requests.get(video_url, params=video_params)

        if r.status_code == 200:
            results = r.json()["items"]

            embed_links = []
            for result in results:
                link = re.findall(
                    r"www.*\"\sf", result["player"]["embedHtml"])[0]
                link = link.replace('"', "")
                link = link.replace(" f", "")
                embed_links.append(link)
            # embed_links.reverse()

            return ("https://" + embed_links[0])
        else:
            return "No video found for the query"
    else:
        return "No video found for the query"
