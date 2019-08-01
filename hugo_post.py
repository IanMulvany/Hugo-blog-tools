
import datetime
today = datetime.date.today()

class HugoPost:
    def __init__(self, title, tags, body):
        self.hugo_title = title
        self.input_tags = tags
        self.hugo_tags = self.filter_tags(self.input_tags)
        self.hugo_body = body
        self.hugo_meta = self.generate_hugo_metadata(self.hugo_title, self.hugo_tags)
        self.hugo_post = self.hugo_meta + "\n" + self.hugo_body

    @staticmethod
    def generate_hugo_metadata(title, tags):
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
