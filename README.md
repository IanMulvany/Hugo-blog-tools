# Blog Tools

A set of python scripts to help me manage my blog posting workflow.

# Usage


```
$ python monitor_posts.py
```

a test script that shows the watchdog library in operation.



```
$ login tech_digest.py
```

log in to the tech digest wordpress blog -- not currently working.



```
$ python3 bear_to_hugo.py path_to_source_post
```

point at a markdown file, and creates a hugo post in partially attended, and creates that post, and git commits it.


```
$python pinboard_to_hugo.py
```

This is not 100% clear to me, need to re-read and re-write some of this code :(





# TODO

- simple script to list posts in pinboar, try date, title, tags
- saved bear post to tech digest-ready post
- saved bear post to publish in hugo with routing
- pinboard to tech digest ready post  -- with logging
- pinboard to hugo-ready post  -- with logging 
- single script to pubilish from all directories
- script to preview which posts I have in pinboard ready to go
- integrate the folder watch script with the transform_to_hugo_format.py script so that posts saved from bear into a location automatically get posted to the web.
