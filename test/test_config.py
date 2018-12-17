import unittest
import sys
from os import path

sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from apps.config import config

class TestConfig(unittest.TestCase):

    CGV_CONFIG = config.CGV_CONFIG

    def test_configuration(self):
        self.assertEqual(self.CGV_CONFIG["URL"]["NOW_PLAYING"], "https://www.cgv.id/en/movies/now_playing")
        self.assertEqual(self.CGV_CONFIG["URL"]["CINEMAS"], "https://www.cgv.id/en/schedule/cinema")
        self.assertEqual(self.CGV_CONFIG["URL"]["MOVIE_INFO"], "https://www.cgv.id/en/movies/info")

if __name__ == "__main__":
    unittest.main(verbosity=2)
