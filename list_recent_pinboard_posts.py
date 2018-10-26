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

class HugoPostFromPinboardPost:
    def __init__(self, pinboard_post):
        self.title = self.sanitise(pinboard_post.description)
        self.tags = pinboard_post.tags
        self.hugo_body = self.generate_hugo_body(pinboard_post.extended, pinboard_post.url)
        self.hugo_meta = self.generate_hugo_metadata(self.title, self.tags)
        self.hugo_post = self.hugo_meta + "\n" + self.hugo_body
        self.hugo_post_filename = self.hugo_post_filename(self.title)

    def generate_hugo_body(self, post_body, url):
        body = post_body + "\n\n"
        body = body + "<a href="+url+">"+url+"</a>"
        return body

    def generate_hugo_metadata(self, title, tags):
        meta = "---"
        meta = meta + "\ntitle: " + title + "\n"
        meta = meta + "url: " + today.strftime('%Y/%m/%d/') + title.replace(" ","_") + "/\n"
        meta = meta + "date: " + today.strftime('%Y-%m-%dT%H:%M:%SZ') + "\n"
        strip_tags = ["bitchin", "toblog", "todigest", "scpb"]
        if len(tags) > 0:
            meta = meta + "categories:"
            for tag in tags:
                if tag not in strip_tags:
                    meta = meta + "\n- " + self.sanitise(tag) # for loop implicitly adds newline
        meta = meta + "\n---"
        return meta

    def hugo_post_filename(self, title):
        hugo_filename = today.strftime('%Y-%m-%d-') + title.rstrip().replace(" ","-") + ".md"
        return hugo_filename

    def sanitise(self, text):
        """
        remove any problematic characters for the Hugo MD engine
        """
        clean_text = text.replace(":","")
        return clean_text

class DigestPostFromPinboardPost:
    def __init__(self, pinboard_post):
        self.digest_body = self.generate_hugo_body( pinboard_post.description, pinboard_post.extended, pinboard_post.url)

    def generate_hugo_body(self, title, post_body, url):
        body = title + "\n\n"
        body = body + post_body + "\n\n"
        body = body + "<a href="+url+">"+url+"</a>"
        return body

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

def write_post(post_content, write_path):
    open(write_path, "w").write(post_content)


def write_to_clipboard(output): 
    """
    we use this function to push data into the clipboard, so that we can open the clipboard data in marked2 
    """
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))


def preview_in_marked(url):
    """
    take the content of a page and convert it to markdown, then open it in marked2 via a url handler that reads the content from the 
    system clipboard 
    """
    content = requests.get(url).content 
    marked = tomd.convert(content.decode('utf-8'))
    write_to_clipboard(marked)
    os.system('open "x-marked://paste"')

def check_user_input(user_input):
    if user_input not in ["i","a","q","h","t","w","d","p","e"]:
        raise 


def select_post(post_list):
    for i, post in enumerate(post_list):
        print(str(i) + ":> "+ post.description + " | " + post.url)
    print("-"*30)
    num = input("pick a number :> ")
    post = post_list[int(num)]
    return post 


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
            hugo_post = HugoPostFromPinboardPost(selected_post)
            print(hugo_post)
        if process_option == "w":
            preview_in_marked(selected_post.url)
        if process_option == "e":
            print("about to edit tags")

    if process_option == "n": 
        selected_post = select_post(recent)

