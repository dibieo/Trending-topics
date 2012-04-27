from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    '''
    takes an html text and removes it's html tags
    '''
    s = MLStripper()
    s.feed(html)
    return s.get_data()