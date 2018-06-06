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

- generate the full hugo site
- commit new changes locally to git
- push the new git commits to the remote (should go to github)

Usage

$ python3 publish_new_poss.py
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
    process = subprocess.call(["git", "commit", "-m","`new posts"], stdout=subprocess.PIPE)

# push the blog to github
with cd("~/blog/partiallyattended"):
   process = subprocess.call(["git", "push"], stdout=subprocess.PIPE)
