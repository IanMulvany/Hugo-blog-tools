import datetime
today = datetime.date.today()

class BlogPost:
    """
    class to contain the most generic content
    about a blog post
    """
    def __init__(self, title, tags, body):
        self.title = title
        self.input_tags = tags
        self.output_tags = self.filter_tags(self.input_tags)
        self.body = body

    def filter_tags(self, input_tags):
        filter_list = ["blog/draft", "blog/posted", "scpb", "bitchin", "toblog", "todigest", "blog", "draft", "posted"]
        filtered_tags = [x for x in input_tags if x not in filter_list]
        return filtered_tags

