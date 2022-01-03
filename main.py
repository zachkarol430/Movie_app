from bs4 import BeautifulSoup
import requests
import time
import json
import pygsheets
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Selenium_functions import requester
import concurrent.futures






#you need to figure out how to integrate class and def functions to find stuff.



#
#
# scope = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
#
#
# with open("movie.json") as source:
#     info = json.load(source)
# creds = service_account.Credentials.from_service_account_info(info)
#
# creds= ServiceAccountCredentials.from_json_keyfile_name("/Users/zachkarol/Movie_project/movie-project-330118-9bf05ce7085e.json", scope)
# client=pygsheets.authorize(service_account_file="movie.json")
#
#
#
# sheet=client.open("Movie_proj").sheet1
#
#
#
# movies_list =list(sheet.get_col(1))[1:]
#

#
#



class movie_get:
    def __init__(self, movie):
        self.movie= movie
        self.director= None
        self.actor= None
        self.box_office= None
    def get_director(self):
        page = requests.get("https://www.google.com/search?q=" + str(self.movie) + "director")
        soup= BeautifulSoup(page.content, 'html.parser')
        try:
            director= soup.find(class_= "BNeawe iBp4i AP7Wnd").text
        except:
            try:
                director= soup.find_all(class_="BNeawe deIvCb AP7Wnd")[1].text
            except:
                director= "NA"
        if director=="Images":
            try:
                director =soup.find(class_="BNeawe s3v9rd AP7Wnd").text
            except:
                 director="NA"
        if director=="Top stories":
            director="NA"
        return director
    def get_genre(self):
        try:
            driver = obj.get_url("https://www.google.com/search?q=" + str(self.movie) + " genre")
            driver.implicitly_wait(10)
            element = driver.find_elements(By.CLASS_NAME, "bVj5Zb.FozYP")
            primary_genre = element[0].text
            secondary_genre= element[1].text
            return primary_genre,secondary_genre
        except:
            return "Na","Na"
    def get_box_office(self):
        try:
            movie = ("+".join(self.movie.split(" ")))
            driver = requests.get(f"https://www.boxofficemojo.com/search/?q={movie}")
            page = BeautifulSoup(driver.content, "html.parser")
            canonical = page.find("a", class_="a-size-medium a-link-normal a-text-bold")
            link = canonical['href']
            driver = requests.get(f"https://www.boxofficemojo.com{link}")
            page = BeautifulSoup(driver.content, "html.parser")
            money = page.find_all(class_= "money")[2].get_text()
        except:
            money= "NA"
        finally:
            return money
    def get_actor(self):
        try:
            driver = requests.get("https://www.google.com/search?q=" + str(self.movie) + " cast")
            page = BeautifulSoup(driver.content, "html.parser")
            try:
                actor = page.find_all("div", class_="BNeawe s3v9rd AP7Wnd")
                actor = actor[0].text
            except IndexError:
                page = BeautifulSoup(driver.content, "html.parser")
                actor = page.select('.JjtOHd')[0].text.strip()
        except:
            actor = "NA"
        finally:
            return actor
    def get_info(self):
        list_foo = [self.get_director, self.get_actor, self.get_box_office]
        with concurrent.futures.ProcessPoolExecutor() as executor:
            thread = [executor.submit(foo) for foo in list_foo]
        results= [x.result() for x in thread]
        self.director = results[0]
        self.actor = results[1]
        self.box_office = results[2]


