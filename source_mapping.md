# inputs

- via pinboard api 
- export from bear 
- raw markdown 
- maybe from command line


# outputs

- hugo markdown format, with pre-matter
- html file locally 
- maybe pushed to wordpress via browswer automation 


# common representation 

- title
- tags 
- post body 
- some tag filtering 


# pseudo control flow 

read source 
create intermedite representation 
have some control flow based on tags or manual input 
based on control choose which output format to create 

could try the following pattern

class blog():
    self.title = title
    self.tags = tags 

bg = Blog()

class HugoPost(blog)
    self.title = blog.title
    self.tags = blog.tags
    self.hugo_post = gen_hugo_post(self.title)

h_post = HugoPost(bg)

one problem that I have is that I may want to call h_post.parent_method, which I can't do if I create h_post by passing in an instance of a class :/ 
I also don't want to wait on what my output is going to be before parsing my input, as I might not know yet. 

I could try to do both, it might be OK. Let's see! 

# Ideas for managing blogging while code is running on AWS 

- keep the log file in an s3 bucket but make it world readable 
- have that log file synced locally to the mac, and run an s3 sync file before and after running a logging process
- have a cron job running on lambda to look at pinboard 
- daily when there is a new post with a specific tag on pinboard run the processes to turn it into a blog post 
- update the log file 
- from pythonista read the log file in the s3 bucket 
- present a list of pinboard posts that have not beed turned into blog posts 
- provide an option to preview and edit 
- add the special tag and then the lambda function will run 
- (alternativly call the lambda function with some wait parameter) 
- for bear posts, find a way to push an exported file to an s3 bucket via something like icloud, or some such 
