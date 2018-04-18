import subprocess
import datetime
today = datetime.date.today()

"""
A script to support creating yaml metadata for my blog posts
while using Hugo as a static blog posting engine.

Suggested workflow:

create a draft post in /Users/ianm/Dropbox/blog/drafts with the name of the post as the filename, but no date in the filename.

When I feel the post is readyish then move the filename to
partiallyattended/content/post/ with the date prepended to the blog post

publish the file to medium using ByWord

use this script to generate the yaml header
add the yaml header to the file

run hugo

post to github

Much of this could actually be automated, but for now it's a reasonable start.

Usage

> python3 create_draft.py

Produces a yaml_frontmatter.yaml file in the local direcorty, and places this front matter into the clipboard of the local computer so that it can be pasted into a blog post when that blog post is ready to be published.

# TODO
push the content of the yaml file into a filename that is determined by the post title, with a placeholder date. 

"""

def write_to_clipboard(output):
    process = subprocess.Popen(
    'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))

string = "---"

title = input("title:")
tags = input("tags (comma separated):").split(",")

# set title
string = string + "\ntitle: " + title + "\n"

# set date
# date: 2017-09-12T14:47:22+01:00
string = string + "date: " + today.strftime('%Y-%m-%dT%H:%M:%SZ') + "\n"

# set url
# date: 2017/09/12/words_from_title/
string = string + "url: " + today.strftime('%Y/%m/%d/') + title.replace(" ","_") + "/\n"

# set categories
string = string + "categories:"
for tag in tags:
    string = string + "\n- " + tag # for loop implicitly adds newline

# close out string:
string = string + "\n---"

write_to_clipboard(string)

f = open("yaml_frontmatter.yaml", "w")
f.write(string)
