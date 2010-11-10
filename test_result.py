import unittest
from lapsheets import Result, Racer

class ResultTest(unittest.TestCase):
    def test_maybe_has_number(self):
        r = Result()
        r.sources = [Racer('100'), Racer('101'), Racer('10-', partial=True)]
        self.assertTrue(r.maybe_has_number('102')) # this should match the partial
        self.assertTrue(r.maybe_has_number('100')) # this should match the actual result

if __name__ == '__main__':
    unittest.main()