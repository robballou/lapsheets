import unittest
from lapsheets import Result, Racer

class ResultTest(unittest.TestCase):
    def test_best_guess_when_all_same(self):
        r = Result()
        r.sources = [Racer('100'), Racer('100'), Racer('100')]
        self.assertEqual(r.best_guess(), '100')
        self.assertEqual(r.certainty(), 1.0)
    
    def test_best_guess_when_majority_rule(self):
        r = Result()
        r.sources = [Racer('100'), Racer('100'), Racer('101')]
        self.assertEqual(r.best_guess(), '100')
        self.assertEqual(r.certainty(), 2.0  / 3.0)
    
    def test_best_guess_with_partials(self):
        r = Result()
        r.sources = [Racer('100'), Racer('100'), Racer('10-', partial=True)]
        self.assertEqual(r.best_guess(), '100')
        
        # certainty would be 2/3 + (2/3 of 1/3)
        self.assertEqual(r.certainty(), (2.0 / 3.0) + (2.0 / 9.0))
    
    def test_has_number(self):
        r = Result()
        r.sources = [Racer('100'), Racer('101'), Racer('10-', partial=True)]
        self.assertTrue(r.has_number('100'))
    
    def test_maybe_has_number(self):
        r = Result()
        r.sources = [Racer('100'), Racer('101'), Racer('10-', partial=True)]
        self.assertTrue(r.maybe_has_number('102')) # this should match the partial
        self.assertTrue(r.maybe_has_number('100')) # this should match the actual result

if __name__ == '__main__':
    unittest.main()