import sys
import os

#####WHY NOT PYCHARM USES PYTHONPATH INSTEAD OF ITS OWN INTERPRETER PATH???
scriptpath = "../collector.py"
sys.path.append(os.path.abspath(scriptpath))
import collector

import json
from pprint import pprint
class JsonParser():
    extension = ".json"

    def __init__(self, set):
        self.mySet = set
        self.myList = list()

    def parse(self, file):
        #print(repr(file.read()))
        json_input = json.load(file)
        pprint(json_input)

if __name__ == "__main__":
    arg_parser = collector.setupParser('HTML')
    argsDict = collector.create_args_dict(arg_parser)
    collector = collector.Collector(JsonParser, argsDict['folder'], argsDict['destfile'])
    if ('diff' in argsDict):
        collector.make_diff(argsDict['diff'])
    else:
        collector.collect_all()
        collector.create_result_file()
