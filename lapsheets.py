import sys
import os

class Result(object):
    """
    This is a single 'slot' in a race (e.g. signifies that a race has crossed the line).
    
    The result may be a racer number, an x (to signify an unknown racer passed), or a partial
    number.
    """
    def __init__(self):
        self.sources = []
        self.reliability = 0
    
    def __str__(self):
        return "%s (%s)" % (self.best_guess(), self.relability) 
    
    def best_guess(self):
        answers = {}
        for source in self.sources:
            if not answers.has_key(source):
                answers[source] = 1
            else:
                answers[source] = answers[source] + 1
        answer = None
        answer_reliability = 0
        for key in answers.keys():
            if answer == None: 
                answer = key
                answer_reliability = answers[key]
            elif answers[key] > answer_reliability:
                answer = key
                answer_reliability = answers[key]
        return answer

class Results(object):
    """ 
    This is a set of results and signifies a single race.
    
    A single race has a set of sources: the lap sheets and a set of Result objects
    for each time a racer crosses the line.
    """
    def __init__(self):
        self.results = [[]]
        self.sources = []
    
    def merge(self):
        """Actually merge the sources into a single source"""
        
        for source in self.sources:
            racers = 0
            for line in source:
                # if len(self.results) < lap: self.results[lap] = []
                
                # find out which lap this person is on
                lap = 1
                found = False
                while not found:
                    if len(self.results) <= lap: self.results.append([])
                    if not in_lap(lap, line):
                        # self.results[lap].appned
                    try:
                        self.results[lap].index(line)
                        # racer exists in this lap, add them to the next
                        lap = lap + 1
                    except ValueError, e:
                        
                        self.results[lap].append()
                        found = True
    
    def print_summary(self):
        count = 0
        for result in self.results:
            if count == 0: 
                count = count + 1
                continue
            print result
            count = count + 1

def find_files(name):
    files = []
    if os.path.exists("data"):
        d = os.listdir("data")
        for entry in d:
            if entry.startswith(name):
                files.append("%s/%s" % ("data", entry))
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