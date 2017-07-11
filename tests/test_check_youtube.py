import hashlib
import json
import os

import pytest

from name_taken_yet.check_youtube import youtube_search

def open_json_fixture(fixture_name):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    json_fpath = os.path.join(current_dir, fixture_name)
    with open(json_fpath, "r") as f:
        return json.load(f)

@pytest.fixture
def googledeveloper():
    return ("googledeveloper",
        open_json_fixture("googledeveloper.json"))

@pytest.fixture
def _urandom():
    """Although we can't guarnatee the test will always
    succeed, but we are confident that if we are random
    enough, the channel title search will yield nothing.
    """

    r = os.urandom(8)
    title = hashlib.sha1(r).hexdigest()
    return (title, open_json_fixture("urandom.json"))

def test_googledeveloper_returns(googledeveloper):
    title, expected_json = googledeveloper
    result = youtube_search(title)
    assert result["exact"] is None
    assert (result["similar"][0]["channel_id"] ==
        expected_json["similar"][0]["channel_id"])

def test_urandom(_urandom):
    title, expected_json = _urandom
    result = youtube_search(title)
    assert result["exact"] == None
    assert result["similar"] == []
