import sys
import os

# ####WHY NOT PYCHARM USES PYTHONPATH INSTEAD OF ITS OWN INTERPRETER PATH???
scriptpath = "../collector.py"
sys.path.append(os.path.abspath(scriptpath))
import collector

import re

"""
Can be used to parse URLs from .url files
"""
class UrlFileParser():
    extension = '.url'
    url_regex_http_https = '.*(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+).*'

    def __init__(self):
        self.collection = set()


    def parse(self, file):
        pattern = re.compile(UrlFileParser.url_regex_http_https)
        for i, line in enumerate(file):
            for match in re.finditer(pattern, line):
                print('Found on line {0}: {1}'.format(i + 1, match.groups()))
                self.collection.add(match.group(1))


if __name__ == "__main__":
    arg_parser = collector.setupParser('txt')
    argsDict = collector.create_args_dict(arg_parser)
    collector = collector.Collector(UrlFileParser, argsDict['srcdir'], argsDict['destdir'],
                                    argsDict.get('write_separate_result_files'))
    if 'diff' in argsDict:
        collector.make_diff(argsDict['diff'])
    else:
        collector.collect_all()
        collector.create_result_file()
