from crawler import MarriotReviewsScraper
import unittest

class TestMarriottReviewsCrawler(unittest.TestCase):

    def test__to_float(self):
        self.assertEqual(
            MarriotReviewsScraper._to_float(None, ''),
            None
        )

        self.assertEqual(
            MarriotReviewsScraper._to_float(None, '3.1'),
            3.1
        )
