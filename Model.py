class Blog:
    def __init__(self, url, name, description):
        self.url = url
        self.name = name
        self.description = description

class Article:
    def __init__(self, blog, url, name, timestamp):
        self.blog = blog
        self.url = url
        self.name = name
        self.timestamp = timestamp
