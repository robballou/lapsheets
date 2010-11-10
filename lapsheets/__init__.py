import os
import re
import sys
import Levenshtein

class Racer(object):
    def __init__(self, number, partial=False, unknown=False):
        self.number = number
        self.partial = partial
        self.unknown = unknown
    
    def match_reliability(self, number):
        return Levenshtein.ratio(self.number, number)

class Result(object):
    """
    This is a single 'slot' in a race (e.g. signifies that a race has crossed the line).
    
    The result may be a racer number, an x (to signify an unknown racer passed), or a partial
    number.
    """
    
    def __init__(self):
        self.sources = []
        self.reliability = 0.0
        self.guess = ''
    
    def __str__(self):
        return "%s (%s)" % (self.best_guess(), self.relability) 
    
    def best_guess(self):
        guess = ''
        for source in self.sources:
            if guess == '': 
                guess = source.number
                self.reliability += 1.0 / len(self.sources)
            elif source.number == guess and not source.partial:
                self.reliability += 1.0 / len(self.sources)
            elif source.partial:
                match = source.match_reliability(guess)
                if match > 0.0: self.reliability += match / len(self.sources)
        self.guess = guess
        return guess
    
    def certainty(self):
        return self.reliability
    
    def has_number(self, number):
        for source in self.sources:
            if source.number == number:
                return True
    
    def maybe_has_number(self, partial):
        for source in self.sources:
            if source.number == partial: return True
            if source.partial:
                if re.match(source.number.replace('-', '\d'), partial): return True
        return False
    
    # def best_guess(self):
    #     answers = {}
    #     for source in self.sources:
    #         if not answers.has_key(source):
    #             answers[source] = 1
    #         else:
    #             answers[source] = answers[source] + 1
    #     answer = None
    #     answer_reliability = 0
    #     for key in answers.keys():
    #         if answer == None: 
    #             answer = key
    #             answer_reliability = answers[key]
    #         elif answers[key] > answer_reliability:
    #             answer = key
    #             answer_reliability = answers[key]
    #     return answer

class Results(object):
    """ 
    This is a set of results and signifies a single race.
    
    A single race has a set of sources: the lap sheets and a set of Result objects
    for each time a racer crosses the line.
    """
    def __init__(self, racers=[]):
        self.racers = []
        self.results = [[]]
        self.sources = []
    
    def final_placement(self):
        """Return the final placement of racers"""
        pass
    
    def in_lap(self, lap, number):
        """Figure out if a racer number is in a lap"""
        
        # make sure the lap exists
        if len(self.results) <= lap: return False
        
        # check all the results in the lap
        for result in self.results[lap - 1]:
            if result.has_number(number):
                return True
        
        return False
    
    def merge(self):
        """
        Actually merge the sources into a single source. The results list is a
        list comprised of Result objects for each lap. So self.results[0] is lap 1,
        etc.
        """
        pass
    
    def print_summary(self):
        """Create a simple text based result summary"""
        pass

def create_results(files):
    final_results = Results()
    for f in files:
        final_results.sources.append(parse_file(f))
    return final_results

def find_files(name, directory="data"):
    files = []
    if os.path.exists(directory):
        d = os.listdir(directory)
        for entry in d:
            if entry.startswith(name):
                files.append("%s/%s" % (directory, entry))
    return files

def merge_files(files):
    final_results = create_results(files)
    final_results.merge()
    return final_results

def parse_file(f):
    """Parse the file for results"""
    raw_data = open(f).read().splitlines()
    data = []
    for line in raw_data:
        if not line.startswith('#'):
            data.append(line)
    return data
