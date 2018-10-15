from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time
import configparser
import logging
import sys
import argparse


config = configparser.ConfigParser()
config.read('digest_script_config.ini')
pb_logfile = config['DEFAULT']["pb_logfile"]

# logging
logger = logging.getLogger()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
fh = logging.FileHandler(pb_logfile)
fh.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(fh)
logger.setLevel(logging.INFO)
logger.info("this is an info message")

# create a new Firefox session
driver = webdriver.Chrome("./chromedriver")
driver.implicitly_wait(3)

# check out security options at https://techdigest.sagepub.com/wp-admin/admin.php?page=aiowpsec_brute_force&tab=tab1

def login_to_digest():
    login_field_user = driver.find_element_by_id("user_login")
    login_field_password = driver.find_element_by_id("user_pass")
    login_field_button = driver.find_element_by_id("wp-submit")
    login_field_user.send_keys("IanMulvany")
    login_field_password.send_keys("1%Al21IcAe0w#K1A")
    time.sleep(2)
    login_field_button.click()


def is_logged_in():
    driver.get("https://techdigest.sagepub.com/")
    try:
        title_field = driver.find_element_by_id("site-title")
        logged_in_state = True
    except:
        logged_in_state = False
    return logged_in_state


def nav_to_new_post_page():
    driver.get("https://techdigest.sagepub.com/wp-admin/post-new.php")


def fill_new_post(title=None, body=None):
    nav_to_new_post_page()
    time.sleep(2)
    post_title = title
    post_body = body
    title_field = driver.find_element_by_id("title")
    body_field = driver.find_element_by_id("content")
    title_field.send_keys(title)
    body_field.send_keys(body)


def main(title, body):
    if is_logged_in():
        logger.info("you are already logged in")
    else:
        login_to_digest()
        fill_new_post(title=title, body=body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--title', help='Title', required=True)
    parser.add_argument('-b','--body', help='Body', required=True)
    args = parser.parse_args()
    main(args.title, args.body)
