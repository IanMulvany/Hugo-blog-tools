import subprocess
import datetime
import logging
from subprocess import Popen, PIPE
import os
import sys

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

today = datetime.date.today()

"""
A script to:

- automatically format a hugo post in /content/posts
- generate the full hugo site
- commit new changes locally to git
- push the new git commits to the remote (should go to github)

Usage

$ python3 transform_to_hugo_format.py path_to_source_post
"""

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


class Post:
    def __init__(self, post_read_path):
        self.post_read_path = post_read_path
        self.post_content = self.get_post_content(self.post_read_path)
        self.title = self.get_title(self.post_content)
        self.tag_line = self.get_tag_line(self.post_content)
        self.tags = self.get_tags(self.tag_line)
        self.hugo_meta = self.generate_hugo_metadata(self.title, self.tags)
        self.hugo_body = self.get_post_body(self.post_content, self.tag_line)
        self.hugo_post = self.hugo_meta + "\n" + self.hugo_body
        self.hugo_post_filename = self.hugo_post_filename(self.title)

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

            # filter out blog/draft and blog/posted as they are "bear" specific tags
            lstripped_expanded_potential_tags_f1 = filter(lambda x: x != "blog/posted", lstripped_potential_tags)
            lstripped_expanded_potential_tags_f2 = filter(lambda x: x != "blog/draft", lstripped_expanded_potential_tags_f1)

            # expand out the tags if they have a "/"
            lstripped_expanded_potential_tags = map(lambda x: x.split("/"), lstripped_expanded_potential_tags_f2)

            # unroll the list of lists
            tags = [item for sublist in lstripped_expanded_potential_tags for item in sublist]
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

    def generate_hugo_metadata(self, title, tags):
        meta = "---"
        meta = meta + "\ntitle: " + title + "\n"
        meta = meta + "url: " + today.strftime('%Y/%m/%d/') + title.replace(" ","_") + "/\n"
        meta = meta + "date: " + today.strftime('%Y-%m-%dT%H:%M:%SZ') + "\n"
        if len(tags) > 0:
            meta = meta + "categories:"
            for tag in tags:
                meta = meta + "\n- " + tag # for loop implicitly adds newline
        meta = meta + "\n---"
        return meta

    def hugo_post_filename(self, title):
        hugo_filename = today.strftime('%Y-%m-%d-') + title.rstrip().replace(" ","-") + ".md"
        return hugo_filename

def write_post(post, write_path):
    full_path = write_path + post.hugo_post_filename
    open(full_path, "w").write(post.hugo_post)

if len(sys.argv) == 1:
    post_read_path = "/Users/ianm/Dropbox/blog/drafts/scholarly comms product meetup - V2 - announcement.md"
else:
    post_read_path = sys.argv[1]

post_write_path = "/Users/ianm/Dropbox/blog/partiallyattended/content/post/"

# create the hugo post object
new_post = Post(post_read_path)

# write the hugo post
write_post(new_post, post_write_path)

# try to generate the blog post
# generate the new blog content
with cd("~/blog/partiallyattended"):
    # we are in ~/Library
    subprocess.call("hugo")

# commit the new content into the local git repo
with cd("~/blog/partiallyattended"):
    process = subprocess.call(["git", "add", "*"], stdout=subprocess.PIPE)

# commit the new post
with cd("~/blog/partiallyattended"):
    title = new_post.title
    process = subprocess.call(["git", "commit", "-m","`new post: `"+title], stdout=subprocess.PIPE)

# push the blog to github
with cd("~/blog/partiallyattended"):
   process = subprocess.call(["git", "push"], stdout=subprocess.PIPE)
