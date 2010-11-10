import sys
import os

def find_files(name, directory="data"):
    files = []
    if os.path.exists(directory):
        d = os.listdir(directory)
        for entry in d:
            if entry.startswith(name) and entry != "%s.txt" % name:
                files.append("%s/%s" % (directory, entry))
    return files

def merge_files(files):
    final_results = Results()
    for f in files:
        final_results.sources.append(parse_file(f))
    final_results.merge()
    return final_results

def parse_file(f):
    raw_data = open(f).read().splitlines()
    data = []
    for line in raw_data:
        if not line.startswith('#'):
            data.append(line)
    return data

if __name__ == '__main__':
    files = find_files('race001')
    results = merge_files(files)
    results.print_summary()