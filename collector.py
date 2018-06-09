import os
import pprint
import argparse


class Collector:
    def __init__(self, parser, src_dir, dest_dir, write_separate_result_files):
        self.single_items_by_file = {}
        self.grouped_items_by_file = {}
        self.collectorSet = set()
        self.src_dir = src_dir
        self.dest_dir = dest_dir
        self.parser = parser
        self.write_separate_result_files = write_separate_result_files
        assert self.parser.extension

    def collect_all(self):
        self.collect_links()

    def make_diff(self, base_file_to_diff):
        self.collect_links(base_file_to_diff)
        self.compare_with_file(base_file_to_diff)

    def create_result_file(self):
        filename = os.path.join(self.dest_dir, 'summary.txt')
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        self.write_single_values_to_file(filename)
        self.write_grouped_values_to_files()

        if self.write_separate_result_files:
            self.write_single_values_to_separate_files()

    def write_single_values_to_file(self, filename):
        with open(filename, "w", encoding='utf-8') as file:
            for item in self.collectorSet:
                file.write("%s\n" % item)

    def write_grouped_values_to_files(self):
        if self.grouped_items_by_file:
            for src_file_name, grouped_items in self.grouped_items_by_file.items():
                if not grouped_items:
                    continue
                for group_name, items in grouped_items.items():
                    dest_filename = os.path.join(self.dest_dir, src_file_name + '_' + group_name + '.txt')
                    with open(dest_filename, "a", encoding='utf-8') as file:
                        for item in items:
                            file.write("%s\n" % item)

    def write_single_values_to_separate_files(self):
        for filename, urls in self.single_items_by_file.items():
                file = open(os.path.join(self.dest_dir, filename + '_extracted_urls.txt'), 'w')
                for url in urls:
                    file.write("%s\n" % url)

    def collect_links(self, base_file_to_diff=None):
        self.collectorSet = set()
        for file in os.listdir(self.src_dir):
            if file.endswith(self.parser.extension):
                if base_file_to_diff is not None and os.path.samefile(os.path.join(self.src_dir, file),
                                                                      base_file_to_diff):
                    continue
                parser = self.parser()
                file_obj = open(os.path.join(self.src_dir, file), encoding='utf-8')
                print('Processing file: ' + file)
                parser.parse(file_obj)
                print("Found " + str(len(parser.collection)) + " elements in " + file)

                file_without_ext = os.path.splitext(file)[0]
                self.single_items_by_file[file_without_ext] = parser.collection

                if hasattr(parser, 'urls_by_category'):
                    self.grouped_items_by_file[file_without_ext] = parser.urls_by_category

                set_len = len(self.collectorSet)
                self.collectorSet.update(parser.collection)
                new_set_len = len(self.collectorSet)
                print('Updated collectorset, length {0} --> {1}'.format(set_len, new_set_len))

        print('Found ' + str(len(self.collectorSet)) + " unique elements in the files above")

    def compare_with_file(self, base_file_to_diff):
        parser = self.parser(base_file_to_diff, set())
        parser.feed(open(base_file_to_diff).read())
        parser.close()

        print('Found ' + str(len(parser.mySet)) + " unique elements in " + base_file_to_diff)

        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(parser.mySet.difference(self.collectorSet))
        pp.pprint(parser.mySet)
        print("New bookmarks in all the other files: ")
        pp.pprint(self.collectorSet.difference(parser.mySet))


def check_file(file):
    if not os.path.exists(file):
        raise argparse.ArgumentError("{0} does not exist".format(file))
    return file


def setup_parser(file_type):
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

    args_dict = vars(args)
    # deletes null keys
    args_dict = dict((k, v) for k, v in args_dict.items() if v)
    print("args dict: " + str(args_dict))
    return args_dict
