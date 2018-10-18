"""
A script to:

- automatically format a hugo post in /content/posts
- generate the full hugo site
- commit new changes locally to git
- push the new git commits to the remote (should go to github)

Usage

$ python3 transform_to_hugo_format.py path_to_source_post
"""

import subprocess
import datetime
import logging
from subprocess import Popen, PIPE
import os
import sys
import argparse
from hugo_post import HugoPost 
from digest_automation import new_digest_post_driver
from markdown2 import Markdown

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

today = datetime.date.today()


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


class BearPost(HugoPost):
    def __init__(self, post_read_path):
        self.post_read_path = post_read_path
        self.post_content = self.get_post_content(self.post_read_path)
        self.post_title = self.get_title(self.post_content)
        self.post_tag_line = self.get_tag_line(self.post_content)
        self.post_body = self.get_post_body(self.post_content, self.post_tag_line)
        self.post_tags = self.get_tags(self.post_tag_line)
        super().__init__(self.post_title, self.post_tags, self.post_body)

    def get_post_content(self, post_read_path):
        content = open(post_read_path).read()
        return content

    def get_title(self, content):
        post_lines = content.split("\n")
        # assume the title is on the first line
        first_line = post_lines[0]
        # remove leading `#`  and spaces
        title = first_line.lstrip("#").lstrip()
        return title

    def get_tag_line(self, post_content):
        """
        tags are not on the first line, and are before any post body.
        they are prepended by a "#"
        they may have a / relation in them, like for example #blog/draft
        """
        # find lines that start with "#"
        lines = post_content.split("\n")

        # drop the first line as it's the title line
        # remove white space from the start of the other lines
        lstripped_lines = map(lambda x: x.lstrip(), lines[1:])

        # get rid of any empty lines
        non_empty_lstripped_lines = filter(lambda x: len(x) > 0, lstripped_lines)

        # now find lines that start with "#"
        potential_tag_lines = filter(lambda x: x[0] == "#", non_empty_lstripped_lines)

        # assume the tag line is the first one that we encouter, simple assumption, however the first line we encounter might be a heading.
        potential_tag_line = list(potential_tag_lines)[0]

        # we can tell by checking that the "#" is followed by a non empty space, indicating that it is of a '#tag' pattern
        if potential_tag_line[1].isspace() is False: # make sure that the character after the hash is not a whitespace, and if so, assume this is indeed the tag line
            tag_line = potential_tag_line
        else:
            tag_line = "" # empty tag line

        return tag_line

    def get_tags(self, tag_line):
        """
        tags are not on the first line, and are before any post body.
        they are prepended by a "#"
        they may have a / relation in them, like for example #blog/draft
        """
        potential_tags = tag_line.split()
        if len(potential_tags) > 0:
            # remove "#" and lowercase the tags
            lstripped_potential_tags = map(lambda x : x.lstrip("#").lower(), potential_tags)
            # expand out the tags if they have a "/"
            lstripped_expanded_potential_tags = map(lambda x: x.split("/"), lstripped_potential_tags)
            # unroll the list of lists
            tags = [item for sublist in lstripped_expanded_potential_tags for item in sublist] # no idea what this does
        else:
            tags = []
        return tags

    def get_post_body(self, post_content, tag_line):
        lines = post_content.split("\n")
        body_lines = lines[1:] # assuming that the title is on the first line.
        lstripped_lines = list(map(lambda x: x.lstrip(), body_lines))
        lstripped_lines.remove(tag_line)
        post_body = "\n".join(lstripped_lines)
        return post_body

def write_post(post, write_path):
    full_path = write_path + post.hugo_post_filename
    open(full_path, "w").write(post.hugo_post)

def build_commit_publish(post, post_write_path):
    commit_path = post_write_path.replace("/Users/ianm/Dropbox","~").replace("/content/post/","")
    with cd(commit_path):
        # we are in ~/Library
        subprocess.call("hugo")

    # commit the new content into the local git repo
    with cd(commit_path):
        process = subprocess.call(["git", "add", "*"], stdout=subprocess.PIPE)

    # commit the new post
    with cd(commit_path):
        title = post.hugo_title
        process = subprocess.call(["git", "commit", "-m","`new post: `"+title], stdout=subprocess.PIPE)

    # # push the blog to github
    # with cd(commit_path):
    #    process = subprocess.call(["git", "push"], stdout=subprocess.PIPE

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
        post_write_path = "/Users/ianm/Dropbox/blog/partiallyattended/content/post/"
        create_hugo_post(new_post, post_write_path)
    if "scpb" in tags:
        post_write_path = "/Users/ianm/Dropbox/blog/scholarlyproductblog/content/post/"
        create_hugo_post(new_post, post_write_path)
    if "bitchin" in tags:
        post_write_path = "/Users/ianm/Dropbox/blog/scholarly-bitchin/content/post/"
        create_hugo_post(new_post, post_write_path)
    if "todigest" in tags:
        create_disgest_post(new_post)

def route_post(new_post, args): 
    default_post_write_path = "/Users/ianm/Dropbox/blog/partiallyattended/content/post/"
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
