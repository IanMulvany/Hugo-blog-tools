# Blog Tools

A set of python scripts to help me manage my blog posting workflow.

# how to blog (as of 2019-07-31)


pushing blog posts exported from bear: 
$ python3 bear_to_hugo.py -t -r `path to hugo post`


# current scripts 


# TODO List 

#TODO: get any scripts working under new code organisation
#TODO: write up known issues with these scritps 
#TODO: move hugo engine into AWS 
#TODO: move blogging hosting to AWS with https 


## Thoughts about the architecture of these scripts

- have a script that allows me to preview tags, and content, and publish from a
variety of sources, pinbord, bear, new post. 
- needs to pull in a class representation of where we are publishing to
- needs to pull in an general class representation of a blog post 
- needs to have logging for pinboard 
- needs to pull in the code to push to digest
- if i can't push to digest now, that code could at least create the html for a
digest post


## Goal

Goal of the project is to create a tool that allows me to:

- route a blog post written in markdown to a number of differnt destinations, based on tags
- preview links added to both pinboard and to hypothesesis, modify them, and then route them 
- make it easier to create weekly summaries of my blog posts into our internal SAGE wordpress site 


## What's next? 

Given the scripts I have created to date, the following seems to make sense: 

- get scripts that use hugo clasess to import from the same class
- introduce a class representing a digest post 
- make sure that there is a log file for pinboard posts that we have published, so 
	that we only see new unpublished posts
- get all settings using simple settings 
- integrate the ability to be able to publish to a wordpress site from a markdown file 
- create the utility scripts to allow myself to quickly be able to work on creting weekly digests 

The thing that will create most immediate value are:
- unifying my class hirarcy 
- getting evryting to using simpole settings 
- maybe adding some type hinting 
- working on the rss aspect


### What is annying with this process

- the main two things are:
	1. too much code lying around the place ina very disorgasinsed way 
	2. speed of working with chromediver is a pain in the butt 



# Exsting scripts as of 2019-02-19:

bear_to_hugo.py

	has some code to take a markdown post and convert it to hugo format
	will also route the hugo post to the given git repo based on tags and 
	publish that repo. Importantly has a class that represetnst the hugo post


digest_settings.py

	simple settings file containing log in details for digest 

	
hugo_post.py

	just contains the class the represetnst a hugo post


list_recent_pinboard_posts.py

	some odd classess - HugoPostfromPinboard post ??
		- DigestPostfromPinboardPost ??
	can show recent pinboard posts 
	can preview them in marked 
	can modify the in-memory version 
	can create a hugo template from the post 
	I think it can create a html represetnation 
	write_post just writes to a local directory, does nothing else 


login_tech_digest.py

	shows how to use chromedriver, but taking variables from simple settings 


monitor_posts.py

	shows how to monitor changes in the local file system and trigger a python script on the back of that 



open_md.py

	shows how to open marked, pushing some markdown to it 


pinboard_to_hugo.py

	seems to want to greate hugo posts from pinboard posts by pushing into 
	the different requried git repos.
	has a sense of time, in terms of looking for last posted items
	has custom class again. 


publish_new_posts.py

	shows how to jump in and out of directories and pushlish new posts from them 


python_vim_input.py

	get input from a vim session - useful for modifyig content within the control flow of a program. 


vim_test_list_recent_pinboard_posts.py

	like list recent pinboard posts, but with the abilty to modfiy in memory with vim



digest_automation/digest_login.py
digest_automation/new_digest_post_driver.py
digest_automation/sage_digest_login.py
digest_automation/test_filter.py




---

# Usage


```
$ python monitor_posts.py
```

a test script that shows the watchdog library in operation.



```
$ login tech_digest.py
```

login to the wordpress blog, uses chrome driver. 
Also uses simple settings to make it possible to keep the 
actual log details separate form the script. 

In fish shell you have to setup the settings file like this: 

`set -x SIMPLE_SETTINGS digest_settings`

You can then try:

`$ python4 login_tech_digest.py`

the digest_automation directory there is a hard coded version of this script that is worling, but it's not working in the root directory of the blog tools project, and I'm not sure why that is that case? 




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


# Logbook 

## 2019-08-01

Lot's of success today.  
- refactored the bear to hugo script to set paths via config  
- refactored the class system to make some of the class property names be cleaarer  
- discovered some templates had gone missing for the schol comms blog, and got them working again   
- got posting to github working again, and fixed a CNAME issue  
- actually blogged something  

Also am starting to see the structure of my original idea. In a nutshell I want to create a 
number of simple single purpose modeles and then compose them together to support 
the overarching blogging workflow.  


## 2019-07-30
Picking this up again, no progress since last time. 
Looks like there is some fairly good class refactoring that I need to do here, 
key is to understand super and some other issues 
also factor out BearPost into it's own module,


## 2019-07-05 

Picked this up after four months. I think I have not finished the refactoring of creaating 
a general "blog post" class. 

I need to quickly re-reaad the code and get a sense of the code structure. 

Goal here is to get to a place where I can post blog posts again. 


