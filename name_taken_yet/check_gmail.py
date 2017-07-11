import contextlib
import os
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys as SKeys
from selenium.webdriver.chrome.options import Options as SOptions

DOT_ERROR = ("Someone already has that username." +
" Note that we ignore periods and capitalization in usernames. Try another?")

NO_DOT_ERROR = "That username is taken. Try another."

GMAIL_SIGNUP_URL = "https://accounts.google.com/SignUp?service=mail"

def setup_browser():
    """Returns a Chrome browser instance."""
    try:
        driver_path = os.environ["CHROME_DRIVER_PATH"]
    except KeyError as e:
        raise KeyError("Expect CHROME_DRIVER_PATH as environment variable")

    chrome_options = SOptions()
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(driver_path, chrome_options=chrome_options)

@contextlib.contextmanager
def open_browser(url, account_name):
    browser = setup_browser()
    browser.get(url)
    try:
        yield browser
    except WebDriverException as e:
        browser.close()
        raise sys.exc_info[1], None, sys.exc_info[2]
    browser.quit()

def check_account_exists(account_name):
    with open_browser(GMAIL_SIGNUP_URL, account_name) as browser:
        account_name_field = browser.find_element_by_id("GmailAddress")
        account_name_field.send_keys(account_name)
        account_name_field.submit()
        # must sleep in order for DOM to update the span
        # with text if failed.
        time.sleep(1)
        # Now DOM should populated this span if account taken already
        warning = browser.find_element_by_id("errormsg_0_GmailAddress")
        if DOT_ERROR in warning.text:
            return {"existed": True, "reason": DOT_ERROR}
        elif NO_DOT_ERROR in warning.text:
            return {"existed": True, "reason": NO_DOT_ERROR}
        else:
            return {"existed": False}
