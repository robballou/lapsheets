import unittest
import lapsheets

class ResultsTest(unittest.TestCase):
    def testResultsSetup(self):
        files = lapsheets.find_files('race001')
        
        # add the sources
        results = lapsheets.create_results(files)
        
        # add the list of racers
        racers = lapsheets.parse_file('data/race001.txt')
        results.racers = racers
        
        # merge the results, storing the results
        results.merge()
        
        # we should have the total number of racers in the final placement as in
        # race (no one DNFd)
        self.assertEqual(len(racers), len(results.final_placement()))        

if __name__ == '__main__':
    unittest.main()