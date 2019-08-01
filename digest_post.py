from blog_post import BlogPost
import datetime
today = datetime.date.today()

class DigestPost(BlogPost):
    def __init__(self, blog_post):
        BlogPost.__init__(self, blog_post.title, blog_post.input_tags, blog_post.body)
        self.digest_body = self.body
        self.digest_meta = self.generate_digest_metadata(self.title, self.output_tags)
        self.digest_post = self.digest_meta + "\n" + self.digest_body

    @staticmethod
    def generate_digest_body(self.body):
        """
        create metadata for a digest blog post.
        """
        # return the html version of the body
        # we assume that the body text is coming in as markdown 
        markdowner = Markdown()
        html_post_body = markdowner.convert(self.body)
        return html_post_body

