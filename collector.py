import os
import pprint
import argparse


class Collector:
    def __init__(self, parser, baseDir, destFile):
        self.collectorSet = set()
        self.dir = baseDir
        self.dest = destFile
        self.parser = parser
        assert self.parser.extension


    def collect_all(self):
        self.collect_links()

    def make_diff(self, baseFileToDiff):
        self.collect_links(baseFileToDiff)
        self.compare_with_file(baseFileToDiff)

    def create_result_file(self):
        file = open(os.path.join(self.dir, self.dest), 'w')
        for item in self.collectorSet:
            file.write("%s\n" % item)

    def collect_links(self, baseFileToDiff=None):
        self.collectorSet = set()
        for file in os.listdir(self.dir):
            if file.endswith(self.parser.extension):
                if ( baseFileToDiff != None and os.path.samefile(os.path.join(self.dir, file), baseFileToDiff)):
                    continue
                parser = self.parser(self.collectorSet)
                #enc='utf-8'
                enc='iso-8859-15'
                openedFile = open(os.path.join(self.dir, file), encoding=enc)
                print('current file: ' + file)
                parser.parse(openedFile)
                print("Found " + str(len(parser.myList)) + " elements in " + file)

        print('Found ' + str(len(self.collectorSet)) + " unique elements in the files above")

    def compare_with_file(self, baseFileToDiff):
        parser = self.parser(baseFileToDiff, set())
        parser.feed(open(baseFileToDiff).read())
        parser.close()

        print('Found ' + str(len(parser.mySet)) + " unique elements in " + baseFileToDiff)

        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(parser.mySet.difference(self.collectorSet))
        pp.pprint(parser.mySet)
        print("New bookmarks in all the other files: ")
        pp.pprint(self.collectorSet.difference(parser.mySet))


def check_file(file):
    if not os.path.exists(file):
        raise argparse.ArgumentError("{0} does not exist".format(file))
    return file

def setupParser(file_type):
    parser = argparse.ArgumentParser(description='Extract links from ' + file_type)
    parser.add_argument('--folder', type=check_file, required=True,
                       help='a folder where search for ' + file_type + 's takes place')
    parser.add_argument('--destfile', required=True,
                       help='destination file where result goes')

    parser.add_argument('--diff', type=check_file,
                        help='Print diffs of links from the specified ' + file_type + ' with the links from all the '+ file_type +' files in the folder')
    return parser

def create_args_dict(arg_parser):
    args = arg_parser.parse_args()
    print(args)

    argsDict = vars(args)
    ##deletes null keys
    argsDict = dict((k, v) for k, v in argsDict.items() if v)
    print("args dict: " + str(argsDict))
    return argsDict
