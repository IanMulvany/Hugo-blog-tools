"""
conversts pinboard posts into blog posts and posts ready to go into
SAGE tech digest.

restricts search to posts in the last PINBOARD_SEARCH_DAY_RANGE

looks for the following tags to decide on how to route the pinboard post

toblog todigest scpd bitchin

"""
import pinboard
import datetime
import time
import requests
import json
import datetime
from pathlib import Path
from collections import deque
import logging
import configparser

#TODO: parse tags for "toblog" tags, and only add those to the blog

config = configparser.ConfigParser()
config.read('pin_to_hugo_config.ini')

path_to_hugo_post_dir = config['DEFAULT']["path_to_hugo_post_dir"]
path_to_tech_digest_dir = config['DEFAULT']["path_to_tech_digest_dir"]
path_to_bitchin_dir = config['DEFAULT']["path_to_bitchin_dir"]
path_to_scpb_dir = config['DEFAULT']["path_to_scpb_dir"]
pb_logfile = config['DEFAULT']["pb_logfile"]
pinboard_api_token = config['DEFAULT']["pinboard_api_token"]
PINBOARD_SEARCH_DAY_RANGE = int(config['DEFAULT']["PINBOARD_SEARCH_DAY_RANGE"])
today = datetime.date.today()


logger = logging.getLogger()
handler = logging.StreamHandler()
fh = logging.FileHandler(pb_logfile)
fh.setLevel(logging.INFO)
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

logger.debug(pb_logfile)

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
    dates = list(map(lambda d: d.split()[0], loglines))
    dates.sort()
    last_post_date = dates[-1]
    return last_post_date

def write_post(post_content, write_path):
    open(write_path, "w").write(post_content)

pb = pinboard.Pinboard(pinboard_api_token)
days_ago = datetime.datetime.now() -  datetime.timedelta(days=PINBOARD_SEARCH_DAY_RANGE)
recent = pb.posts.all(fromdt=days_ago)

last_post_day = get_last_blogged_pb_post_date(pb_logfile)
last_post_day_time = time.strptime(last_post_day, "%Y-%m-%d")
for post in recent:
    post_day = str(post.time).split()[0]
    post_day_time = time.strptime(post_day, "%Y-%m-%d")
    if post_day_time > last_post_day_time:
        hugo_post = HugoPostFromPinboardPost(post)
        digest_post = DigestPostFromPinboardPost(post)
        tags = post.tags
        if "toblog" in tags:
            print(tags)
            print("route to partiallyattended")
            hugo_path = path_to_hugo_post_dir + "/" + hugo_post.hugo_post_filename
            write_post(hugo_post.hugo_post, hugo_path)
            logger.info(post_day + " " + post.description)
        if "todigest" in tags:
            print(tags)
            print("route to digest")
            digest_path = path_to_tech_digest_dir + "/" + hugo_post.hugo_post_filename
            write_post(digest_post.digest_body, digest_path)
            logger.info(post_day + " " + post.description)
        if "bitchin" in tags:
            print(tags)
            print("route to bitchin")
            bitchin_path = path_to_bitchin_dir + "/" + hugo_post.hugo_post_filename
            write_post(hugo_post.hugo_post, bitchin_path)
            logger.info(post_day + " " + post.description)
        if "scpb" in tags:
            print(tags)
            print("route to scpb")
            scpb_path = path_to_scpb_dir + "/" + hugo_post.hugo_post_filename
            write_post(hugo_post.hugo_post, scpb_path)
            logger.info(post_day + " " + post.description)

    # post_day = str(post.time).split()[0]
    # post_day_time = time.strptime(post_day, "%Y-%m-%d")
    # if post_day_time > last_post_day_time:
    #     hugo_post = HugoPostFromPinboardPost(post)
    #     digest_post = DigestPostFromPinboardPost(post)
    #     hugo_path = path_to_hugo_post_dir + "/" + hugo_post.hugo_post_filename
    #     digest_path = path_to_tech_digest_dir + "/" + hugo_post.hugo_post_filename
    #     write_post(hugo_post.hugo_post, hugo_path)
    #     write_post(digest_post.digest_body, digest_path)
    #     logger.info(post_day + " " + post.description)
