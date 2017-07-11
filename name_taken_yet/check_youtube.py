import os

from apiclient.discovery import build
from apiclient.errors import HttpError

# Code credit from YT Data API code sample:
# https://developers.google.com/youtube/v3/code_samples/python

try:
    DEVELOPER_KEY = os.environ["YT_DEVELOPER_KEY"]
except KeyError as e:
    raise KeyError("Expect YT_DEVELOPER_KEY as environment variable.")

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(search_term):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        q=search_term,
        part="snippet",
        maxResults=5
    ).execute()

    return process_search_result(search_term, search_response)

def get_channel_details(snippet):
    return {
        "channel_title": snippet["title"],
        "channel_id": snippet["channelId"]
    }

def process_search_result(desired_title, response):
    """Determine whether title of any channels match
    the exact the desired channel name, and
    a list of channel titles are similar to the
    desired channel name.

    For example, if the desired channel name is "Just do it":
        search results are:
            - JustDoIt
            - Just do It
            - Just_Do_It
            - ?23? Just D0 |t
    Then only "Just do It" is considered the exact match,
    since YT custom URL is case-insentivie, plus that channel
    name is too similar to ours. The rest are considerd similar.
    We returns the first four similar names.

    """

    results = {"exact": None, "similar": []}
    print(response)
    for result in response.get("items", []):
        snippet = result["snippet"]
        r_title = snippet["title"]
        if (desired_title == r_title
            or desired_title.lower() == r_title.lower()):
            results["exact"] = get_channel_details(snippet)
        else:
            results["similar"].append(
                get_channel_details(snippet))
    return results
