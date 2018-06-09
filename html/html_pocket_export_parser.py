import sys
import os
from html.parser import HTMLParser
# ####WHY NOT PYCHARM USES PYTHONPATH INSTEAD OF ITS OWN INTERPRETER PATH???
scriptpath = "../collector.py"
sys.path.append(os.path.abspath(scriptpath))
import collector


class HTMLPocketExportParser(HTMLParser):
    extension = ".html"

    def __init__(self):
        HTMLParser.__init__(self)
        self.collection = set()
        self.urls_by_category = dict()

    def parse(self, file):
        self.feed(file.read())
        self.close()

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        if tag == 'a':
            pocket_tags = dict(attrs).get('tags')
            if not pocket_tags:
                pocket_tags = 'without_tag'

            url = dict(attrs).get('href')
            self.collection.add(url)
            if pocket_tags not in self.urls_by_category:
                self.urls_by_category[pocket_tags] = set()
            self.urls_by_category[pocket_tags].add(url)

    def handle_endtag(self, tag):
        pass
        # print("Encountered an end tag :", tag)

    def handle_data(self, data):
        pass
        # print("Encountered some data  :", data)


if __name__ == "__main__":
    arg_parser = collector.setup_parser('HTML')
    argsDict = collector.create_args_dict(arg_parser)
    collector = collector.Collector(HTMLPocketExportParser, argsDict['srcdir'], argsDict['destdir'],
                                    argsDict['write_separate_result_files'])
    if 'diff' in argsDict:
        collector.make_diff(argsDict['diff'])
    else:
        collector.collect_all()
        collector.create_result_file()