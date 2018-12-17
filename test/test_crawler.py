import sys
import unittest
from datetime import datetime
from os import path

sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from apps.modules import crawler

class TestCrawler(unittest.TestCase):

    def test_get_now_playing_movies(self):
        result = crawler.Crawler().get_now_playing_movies()
        self.assertTrue(isinstance(result, list))
        self.assertTrue(len(result )> 0 )
    #end def

    def test_get_cinemas(self):
        result = crawler.Crawler().get_cinemas()
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(len(result["cities"])> 0 )
        self.assertTrue(len(result["cinemas"])> 0 )
    #end def

    def test_get_movie_schedules(self):
        current_date = datetime.utcnow()
        result = crawler.Crawler().get_movie_schedules("002", current_date)
        self.assertTrue(isinstance(result, list))
        self.assertTrue(len(result) > 0)

    def test_get_movie_schedule_untils(self):
        result = crawler.Crawler().get_movie_schedule_untils("002", 3)

#end class

if __name__ == "__main__":
    unittest.main(verbosity=2)
