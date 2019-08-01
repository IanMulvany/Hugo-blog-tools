"""
A script to:

- automatically format a hugo post in /content/posts
- generate the full hugo site
- commit new changes locally to git
- push the new git commits to the remote (should go to github)

Usage

$ python3 bear_to_hugo.py -t -r `path to hugo post`
"""

import subprocess
import datetime
import logging
from subprocess import Popen, PIPE
import os
import sys
import argparse
from bear_post import BearPost
from hugo_post import HugoPost
from digest_automation import new_digest_post_driver
from markdown2 import Markdown
import configparser

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

today = datetime.date.today()


config = configparser.ConfigParser()
config.read('bear_to_hugo_config.ini')
root_path = config['DEFAULT']["root_path"]
blog_root_path = config['DEFAULT']["blog_root_path"]
partiallyattended_content_path = config['DEFAULT']["partiallyattended_content_path"]
scholarlyproductblog_content_path = config['DEFAULT']["scholarlyproductblog_content_path"]
class cd:
    """Context manager for changing the current working directory
    see https://stackoverflow.com/questions/431684/how-do-i-cd-in-python
    """
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)



def write_post(post, write_path):
    full_path = write_path + post.hugo_post_filename
    open(full_path, "w").write(post.hugo_post)

def build_commit_publish(post, post_write_path):
    """
    takes a path like 
    /Users/ianm/Documents/blog/partiallyattended/content/post/"

    and turns it into something like 
    ~/
    """
    print(post_write_path)
    commit_path = post_write_path.replace(root_path,"~/").replace("/content/post/","")
    print(commit_path)
    print("running hugo")
    with cd(commit_path):
        # we are in ~/Library
        subprocess.call("hugo")

    # commit the new content into the local git repo
    with cd(commit_path):
        print("adding changes to git")
        process = subprocess.call(["git", "add", "*"], stdout=subprocess.PIPE)

    # commit the new post
    with cd(commit_path):
        title = post.hugo_title
        print("committing changes to git")
        process = subprocess.call(["git", "commit", "-m","`new post: `"+title], stdout=subprocess.PIPE)

    # push the blog to github
    with cd(commit_path):
        print("pushing changes to github")
        process = subprocess.call(["git", "push"], stdout=subprocess.PIPE)

def create_hugo_post(new_post, post_write_path):
    write_post(new_post, post_write_path)
    build_commit_publish(new_post, post_write_path)

def create_disgest_post(new_post):
    markdowner = Markdown()
    html_post_body = markdowner.convert(new_post.hugo_body)
    new_digest_post_driver.main(new_post.hugo_title, html_post_body)

def create_post_by_tag(new_post):
    tags = new_post.input_tags
    logger.info(tags)
    if "toblog" in tags:
        post_write_path = blog_root_path + partiallyattended_content_path
        create_hugo_post(new_post, post_write_path)
    if "scpb" in tags:
        post_write_path = blog_root_path + scholarlyproductblog_content_path 
        create_hugo_post(new_post, post_write_path)
    if "todigest" in tags:
    # if "bitchin" in tags:
    #     post_write_path = "/Users/ianm/Documents/blog/scholarly-bitchin/content/post/"
    #     create_hugo_post(new_post, post_write_path)
    # if "todigest" in tags:
    #     create_disgest_post(new_post)

def route_post(new_post, args): 
    default_post_write_path = blog_root_path + partiallyattended_content_path
    if args.write_path:
        create_hugo_post(new_post, args.write_path)
    if args.to_digest:
        create_post(new_post, args.write_path)
    if args.tag_route:
        create_post_by_tag(new_post)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r','--read_path', help='Read', required=True)
    parser.add_argument('-w','--write_path', help='Write', required=False)
    parser.add_argument('-d','--to_digest', help='Write', required=False)
    parser.add_argument('-t','--tag_route', help='Tag Routing', action='store_true') 
    args = parser.parse_args()
    new_post = BearPost(args.read_path)
    route_post(new_post, args)

# DONE create a good test post for testing this against
# DONE while workling on this stop posting to github
# DONE create a main function
# DONE create a function that calls a write to partially attended
# DONE create a function that calls a write to a given hugo directory
# DONE create an arg parser to capture destinations
# TODO filter on tags for destination
# TODO create a function that does a write to digest
# TODO unlock the function that writes to github
# TODO replicate this workflow, but for posting from pinboard
