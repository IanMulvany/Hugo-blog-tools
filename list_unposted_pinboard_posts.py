"""

to run:

$ set -x 

lists recent posts on pinboard 
"""
import pinboard
import subprocess
import datetime
import time
import requests
import json
import datetime
from pathlib import Path
from collections import deque
import logging
import configparser
import requests 
import tempfile
import html2text 
import tomd 
import os
import sys, tempfile, os
from subprocess import call

# from markdownify import markdownify as md

config = configparser.ConfigParser()
config.read('pin_lister_config.ini')

pb_list_logfile = config['DEFAULT']["pb_list_logfile"]
pinboard_api_token = config['DEFAULT']["pinboard_api_token"]
PINBOARD_SEARCH_DAY_RANGE = int(config['DEFAULT']["PINBOARD_SEARCH_DAY_RANGE"])
today = datetime.date.today()

logger = logging.getLogger()
handler = logging.StreamHandler()
fh = logging.FileHandler(pb_list_logfile)
fh.setLevel(logging.INFO)
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)
logger.debug(pb_list_logfile)


def get_last_blogged_pb_post_date(filepath):
    """
    find the date of the most recently posted item in the log file.
    """
    loglines = open(filepath,"r").readlines()
    if len(loglines) == 0:
        last_post_date = "1900-01-01"
    else:
        dates = list(map(lambda d: d.split()[0], loglines))
        dates.sort()
        last_post_date = dates[-1]
    return last_post_date

pb = pinboard.Pinboard(pinboard_api_token)
days_ago = datetime.datetime.now() -  datetime.timedelta(days=PINBOARD_SEARCH_DAY_RANGE)
recent = pb.posts.all(fromdt=days_ago)

last_post_day = get_last_blogged_pb_post_date(pb_list_logfile)
last_post_day_time = time.strptime(last_post_day, "%Y-%m-%d")

for i, post in enumerate(recent):
    print(str(i) + ":> "+ post.description + " | " + post.url)
print("-"*30)
print("select from: i - interactive | a - publish all | q - quit")
status = input(":> ")
check_user_input(status)

if status == "i":
    selected_post = select_post(recent)

while status != "q":
    process_option = ""
    print("current selection: " + selected_post.description)
    while process_option not in ["p", "n"]:
        print("h: preview hugo markdown, t: view tags, w: preview webpage, d: add description, p: publish, e: edit tags, n: next post")
        process_option = input(":> ")
        print("you have selected " + process_option)
        if process_option == "t":
            print(selected_post.tags)
        if process_option == "h":
            preview_hugo_post(selected_post)
        if process_option == "w":
            preview_in_marked(selected_post.url)
        if process_option == "e":
            update_tags(selected_post.tags)

    if process_option == "n": 
        selected_post = select_post(recent)

