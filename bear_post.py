
from blog_post import BlogPost

class BearPost(BlogPost):
    def __init__(self, post_read_path):
        self.bear_post_read_path = post_read_path
        self.bear_post_content = self.get_post_content(self.bear_post_read_path)
        self.bear_post_title = self.get_title(self.bear_post_content)
        self.bear_post_tag_line = self.get_tag_line(self.bear_post_content)
        self.bear_post_body = self.get_post_body(self.bear_post_content, self.bear_post_tag_line)
        self.bear_post_tags = self.get_tags(self.bear_post_tag_line)
        print(self.bear_post_tags)
        super().__init__(self.bear_post_title, self.bear_post_tags, self.bear_post_body)

    def get_post_content(self, post_read_path):
        content = open(post_read_path).read()
        return content

    def get_title(self, content):
        post_lines = content.split("\n")
        # assume the title is on the first line
        first_line = post_lines[0]
        # remove leading `#`  and spaces
        title = first_line.lstrip("#").lstrip()
        return title

    def get_tag_line(self, post_content):
        """
        tags are not on the first line, and are before any post body.
        they are prepended by a "#"
        they may have a / relation in them, like for example #blog/draft
        """
        # find lines that start with "#"
        lines = post_content.split("\n")

        # drop the first line as it's the title line
        # remove white space from the start of the other lines
        lstripped_lines = map(lambda x: x.lstrip(), lines[1:])

        # get rid of any empty lines
        non_empty_lstripped_lines = filter(lambda x: len(x) > 0, lstripped_lines)

        # now find lines that start with "#"
        potential_tag_lines = filter(lambda x: x[0] == "#", non_empty_lstripped_lines)

        # assume the tag line is the first one that we encouter, simple assumption, however the first line we encounter might be a heading.
        potential_tag_line = list(potential_tag_lines)[0]

        # we can tell by checking that the "#" is followed by a non empty space, indicating that it is of a '#tag' pattern
        if potential_tag_line[1].isspace() is False: # make sure that the character after the hash is not a whitespace, and if so, assume this is indeed the tag line
            tag_line = potential_tag_line
        else:
            tag_line = "" # empty tag line

        return tag_line

    def get_tags(self, tag_line):
        """
        tags are not on the first line, and are before any post body.
        they are prepended by a "#"
        they may have a / relation in them, like for example #blog/draft
        """
        potential_tags = tag_line.split()
        if len(potential_tags) > 0:
            # remove "#" and lowercase the tags
            lstripped_potential_tags = map(lambda x : x.lstrip("#").lower(), potential_tags)
            # expand out the tags if they have a "/"
            lstripped_expanded_potential_tags = map(lambda x: x.split("/"), lstripped_potential_tags)
            # unroll the list of lists
            tags = [item for sublist in lstripped_expanded_potential_tags for item in sublist] # no idea what this does
        else:
            tags = []
        return tags

    def get_post_body(self, post_content, tag_line):
        lines = post_content.split("\n")
        body_lines = lines[1:] # assuming that the title is on the first line.
        lstripped_lines = list(map(lambda x: x.lstrip(), body_lines))
        lstripped_lines.remove(tag_line)
        post_body = "\n".join(lstripped_lines)
        return post_body
