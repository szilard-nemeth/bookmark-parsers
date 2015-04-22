import os
import pprint
import argparse


class Collector:
    def __init__(self, parser, src_dir, dest_dir, write_separate_result_files):
        self.collectorSet = set()
        self.src_dir = src_dir
        self.dest_dir = dest_dir
        self.parser = parser
        self.write_separate_result_files = write_separate_result_files
        assert self.parser.extension


    def collect_all(self):
        self.collect_links()

    def make_diff(self, baseFileToDiff):
        self.collect_links(baseFileToDiff)
        self.compare_with_file(baseFileToDiff)

    def create_result_file(self):
        file = open(os.path.join(self.dest_dir, 'summary.txt'), 'w')
        for item in self.collectorSet:
            file.write("%s\n" % item)

        if self.write_separate_result_files:
            #write separate result files if required
            for filename, urls in self.dict_of_items_by_file.items():
                file = open(os.path.join(self.dest_dir, filename + '_extracted_urls'), 'w')
                for url in urls:
                    file.write("%s\n" % url)

    def collect_links(self, baseFileToDiff=None):
        self.collectorSet = set()
        self.dict_of_items_by_file = {}
        for file in os.listdir(self.src_dir):
            if file.endswith(self.parser.extension):
                if baseFileToDiff is not None and os.path.samefile(os.path.join(self.src_dir, file), baseFileToDiff):
                    continue
                parser = self.parser()
                enc = 'iso-8859-15'
                openedFile = open(os.path.join(self.src_dir, file), encoding=enc)
                print('Processing file: ' + file)
                parser.parse(openedFile)
                print("Found " + str(len(parser.collection)) + " elements in " + file)

                self.dict_of_items_by_file[file] = parser.collection
                set_len = len(self.collectorSet)
                self.collectorSet.update(parser.collection)
                new_set_len = len(self.collectorSet)
                print('Updated collectorset, length {0} --> {1}'.format(set_len, new_set_len))

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
    parser.add_argument('--srcdir', type=check_file, required=True,
                        help='a folder where search for ' + file_type + 's takes place')
    parser.add_argument('--destdir', required=True,
                        help='destination dir where result files will be created')

    parser.add_argument('--diff', type=check_file,
                        help='Print diffs of links from the specified ' + file_type + ' with the links from all the ' + file_type + ' files in the folder')

    parser.add_argument('--write_separate_result_files', required=False, action='store_true')

    return parser


def create_args_dict(arg_parser):
    args = arg_parser.parse_args()
    print(args)

    argsDict = vars(args)
    # #deletes null keys
    argsDict = dict((k, v) for k, v in argsDict.items() if v)
    print("args dict: " + str(argsDict))
    return argsDict
