"""
return a list of unposted recent bear posts
"""
import glob
import configparser
import logging


path_to_bear_posts = "/Users/ianm/Dropbox/blog/bear_to_blog/"


config = configparser.ConfigParser()
config.read('bear_lister_config.ini')

bear_list_logfile = config['DEFAULT']["bear_list_logfile"]

logger = logging.getLogger()
handler = logging.StreamHandler()
fh = logging.FileHandler(bear_list_logfile)
fh.setLevel(logging.INFO)
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)
logger.debug(bear_list_logfile)


def get_logged_posts():
    logged_posts = []
    return logged_posts

def get_exported_posts(path_to_bear_posts):
    print(path_to_bear_posts) 
    exported_posts = glob.glob(path_to_bear_posts+"*")
    print(exported_posts)
    return exported_posts

def get_unblogged_posts(logged_posts, exported_posts):
    unblogged_posts = exported_posts - logged_posts
    return unblogged_posts 

logged_posts = get_logged_posts()
exported_posts = get_exported_posts()
unblogged_posts = get_unblogged_posts(logged_posts, exported_posts)

print(unblogged_posts) 
