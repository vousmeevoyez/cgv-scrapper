import base64
from urllib             import request
from io                 import BytesIO
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4                import BeautifulSoup
from urllib             import request
from io                 import BytesIO
from datetime           import datetime, date, timedelta

import sys
from os import path

sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from config import config

class Crawler:

    CGV_CONFIG = config.CGV_CONFIG

    def __init__(self):
        opts = Options()
        opts.add_argument("headless")
        self.browser = Chrome(options=opts)
    #end def

    def _download_img(self,url):
        try:
            img = request.urlopen(url).read()
            img = BytesIO(img)
        except:
            return False
        return img.read()
    #end def

    def get_now_playing_movies(self):
        # open url
        self.browser.get(self.CGV_CONFIG["URL"]["NOW_PLAYING"])
        # load it to beautiful soup
        html_soup = BeautifulSoup(self.browser.page_source, features="lxml")
        # find movies 
        movies = html_soup.find("div",{ "class" : "movie-list-body"}).find("ul").findAll("li")

        now_playing = []

        for movie in movies:
            # extract movie code from href link
            movie_link = movie.a["href"]
            movie_link_split = movie_link.split("/")
            movie_code = movie_link_split[4]

            # extract movie poster image url
            movie_poster_url = "https://cdn.cgv.id/uploads/movie/compressed/{}.jpg".format(movie_code)

            # download images
            print(movie_poster_url)
            img = self._download_img(movie_poster_url)
            if img == False:
                print("Download Movie Post Failed")
            #end if

            now_playing.append({
                "movie_code" : movie_code,
                "movie_poster" : movie_poster_url
            })

        #end for
        return now_playing
    #end def

    def get_cinemas(self):
        result = {
            "cities"  : None,
            "cinemas" : None,
        }

        # open url
        self.browser.get(self.CGV_CONFIG["URL"]["CINEMAS"])
        # load it to beautiful soup
        html_soup = BeautifulSoup(self.browser.page_source, features="lxml")
        # get all city first
        cities = html_soup.find("div",{ "class" : "sect-city" }).find_all("li")

        all_cities = []
        # iterate through each city and get all cinemas information there
        for city in cities:
            city_info = city.find("a" , {"href" : "javascript:void(0);"})

            if city_info != None:
                city_name = city_info.string
                # create custom city code here as identifier
                city_code = (city_name.replace(" ","_")).upper()

                # find all cinema in a city
                cinemas = city.find_all("a", { "class" : "cinema_fav" })

                city_cinemas = []
                for cinema in cinemas:
                    cinema_name = cinema.string
                    cinema_id = cinema["id"]

                    city_cinemas.append({
                        "cinema_name" : cinema_name,
                        "city_code"   : city_code,
                        "cinema_id"   : cinema_id,
                    })
                #end for
                print(city_cinemas)
            #end if
            all_cities.append({
                "city_name" : city_name,
                "city_code" : city_code
            })
        #end for
        result["cities" ] = all_cities
        result["cinemas"] = city_cinemas
        return result
    #end def

    def get_movie_schedules(self, cinema_id, current_date):
        url_date  = current_date.strftime("%y-%m-%d")

        # open url
        self.browser.get(self.CGV_CONFIG["URL"]["CINEMAS"] + "/" + cinema_id + "/" + url_date)
        # load it to beautiful soup
        html_soup = BeautifulSoup(self.browser.page_source, features="lxml")

        schedules = html_soup.find("div",{"class" : "schedule-lists"})
        schedules = schedules.ul.find_all("li")

        show_time_schedule = []
        for schedule in schedules:
            try:
                schedule_info = schedule.div
                movie_name = schedule_info.a.text
                movie_link = schedule_info.a.get("href")
                movie_id = movie_link.split("/")[4]

                # iterate through movie show time
                movie_schedules = schedule.ul.find_all("a", { "class" : "active"})
                for movie_schedule in movie_schedules:
                    if movie_schedule != None:
                        movie_class = movie_schedule["attr-fmt"]
                        schedule_id = movie_schedule["id"]
                        time        = movie_schedule.string
                        show_time_schedule.append({
                            "movie_id"   : movie_id,
                            "schedule_id": schedule_id,
                            "movie_class": movie_class,
                            "time"       : time
                        })
                    #end if
                #end for
            except:
                pass
            #end try
        #end for
        return show_time_schedule
    #end def

    def get_movie_schedule_untils(self, cinema_id, days):
        # genereate date list
        date_list = [ (date.today() + timedelta(days=x)) for x in range(0, days) ]

        schedule_list = []
        for current_date in date_list:
            schedule = self.get_movie_schedules(cinema_id, current_date)
            schedule_list.append({
                "date" : current_date,
                "schedule" : schedule
            })
        #end for
        return schedule_list
    #end def
#end class
