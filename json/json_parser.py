import sys
import os

# ####WHY NOT PYCHARM USES PYTHONPATH INSTEAD OF ITS OWN INTERPRETER PATH???
scriptpath = "../collector.py"
sys.path.append(os.path.abspath(scriptpath))
import collector

import json
from pprint import pprint


class JsonParser():
    extension = ".json"

    def __init__(self):
        self.collection = set()

    def parse(self, file):
        #print(repr(file.read()))
        json_input = json.load(file)
        for s in self.id_generator(json_input):
            #print(s)
            self.collection.add(s)
            #pprint(json_input)

    def id_generator(self, json_dict):
        if isinstance(json_dict, dict):
            for k, v in json_dict.items():
                if k == "uri":
                    yield v
                elif isinstance(v, dict) or isinstance(v, list):
                    for id_val in self.id_generator(v):
                        yield id_val
        elif isinstance(json_dict, list):
            for listitem in json_dict:
                for id_val in self.id_generator(listitem):
                    yield id_val


if __name__ == "__main__":
    arg_parser = collector.setupParser('json')
    argsDict = collector.create_args_dict(arg_parser)
    collector = collector.Collector(JsonParser, argsDict['srcdir'], argsDict['destdir'],
                                    argsDict['write_separate_result_files'])
    if 'diff' in argsDict:
        collector.make_diff(argsDict['diff'])
    else:
        collector.collect_all()
        collector.create_result_file()
