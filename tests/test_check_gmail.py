import hashlib
import os

import pytest

from name_taken_yet.check_gmail import (
    check_account_exists,
    DOT_ERROR,
    NO_DOT_ERROR,
)

@pytest.fixture
def exist_gmail_with_dot():
    return "name.taken.yet.test@gmail.com"

@pytest.fixture
def exist_gmail_no_dot():
    return "nametakenyettest123@gmail.com"

@pytest.fixture
def non_exist_gmail():
    ub = os.urandom(12)
    ending = hashlib.sha1(ub).hexdigest()[:8]
    prefix = "name.taken.yet.test"
    return "{p}.{e}@gmail.com".format(
        p=prefix, e=ending)

def test_gmail_with_dot_exists(exist_gmail_with_dot):
    result = check_account_exists(exist_gmail_with_dot)
    assert result["existed"] == True
    assert DOT_ERROR == result["reason"]

def test_gmail_no_dot_exists(exist_gmail_no_dot):
    result = check_account_exists(exist_gmail_no_dot)
    assert result["existed"] == True
    assert NO_DOT_ERROR == result["reason"]

def test_non_exist_gmail(non_exist_gmail):
    result = check_account_exists(non_exist_gmail)
    assert result["existed"] == False
