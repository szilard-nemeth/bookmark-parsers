import json
from pprint import pprint

__author__ = 'eszinme'


class JsonParser():

    def __init__(self):
        pass

    def parse_file(self):
        f = open('/home/eszinme/_dropbox/Dropbox/___PENDING/__BOOKMARK/json/Bookmarks 2010-11-11.json','r')
        print(repr(f.read()))
        #json_input = json.load(f)
        #pprint(json_input)

if __name__ == "__main__":
    JsonParser().parse_file()
