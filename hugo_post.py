from blog_post import BlogPost
import datetime
today = datetime.date.today()

class HugoPost(BlogPost):
    def __init__(self, blog_post):
        BlogPost.__init__(self, blog_post.title, blog_post.input_tags, blog_post.body)
        # super().__init__(self.post_title, self.post_tags, self.post_body)
        self.hugo_body = self.body
        self.hugo_meta = self.generate_hugo_metadata(self.title, self.output_tags)
        self.hugo_post = self.hugo_meta + "\n" + self.hugo_body
        self.hugo_post_filename = self.hugo_post_filename(self.title)

    @staticmethod
    def generate_hugo_metadata(title, tags):
        """
        create metadata for a hugo blog post.
        """
        meta = "---"
        meta = meta + "\ntitle: " + title + "\n"
        meta = meta + "url: " + today.strftime('%Y/%m/%d/') + title.replace(" ", "_") + "/\n"
        meta = meta + "date: " + today.strftime('%Y-%m-%dT%H:%M:%SZ') + "\n"
        if tags:
            meta = meta + "categories:"
            for tag in tags:
                meta = meta + "\n- " + tag # for loop implicitly adds newline
        meta = meta + "\n---"
        return meta

    def hugo_post_filename(self, title):
        hugo_filename = today.strftime('%Y-%m-%d-') + title.rstrip().replace(" ", "-") + ".md"
        return hugo_filename
