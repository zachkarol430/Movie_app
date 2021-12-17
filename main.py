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


obj=requester()



#you need to figure out how to integrate class and def functions to find stuff.





scope = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]


with open("movie.json") as source:
    info = json.load(source)
creds = service_account.Credentials.from_service_account_info(info)

# creds= ServiceAccountCredentials.from_json_keyfile_name("/Users/zachkarol/Movie_project/movie-project-330118-9bf05ce7085e.json", scope)
client=pygsheets.authorize(service_account_file="movie.json")



sheet=client.open("Movie_proj").sheet1



movies_list =list(sheet.get_col(1))[1:]
while("" in movies_list):
    movies_list.remove("")

#
#



class movie_get:
    def __init__(self, movie):
        self.movie= movie
    def get_actor(self):
        try:
            try:
                driver=obj.get_url("https://www.google.com/search?q=" + str(self.movie)+ " cast")
                element = driver.find_elements(By.CLASS_NAME, "JjtOHd")
                element_text = element[0].text
                return element_text
            except:
                page = requests.get("https://www.google.com/search?q=" + str(self.movie)+" cast")
                soup = BeautifulSoup(page.content, 'lxml')
                actor=soup.find("div", class_="BNeawe s3v9rd AP7Wnd").text
                return actor
        except:
            return "Na"
    def get_director(self):
        try:
            driver = obj.get_url("https://www.google.com/search?q=" + str(self.movie) + " director")
            element = driver.find_element(By.CLASS_NAME, "FLP8od")
            element_text = element.text
            return element_text
        except:
            try:
                page = requests.get("https://www.google.com/search?q=" + str(self.movie) + "director")
                soup = BeautifulSoup(page.content, 'html.parser')
                directors = soup.find_all("div", class_="BNeawe deIvCb AP7Wnd")
                director = directors[1].text
                if director != "Images":
                    return director
                else:
                    lol
            except:
                try:
                    director = soup.find("div", class_="BNeawe iBp4i AP7Wnd").text
                    return director
                except:
                    return "Na"
        return "Na"
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
            driver = obj.get_url(f"https://www.boxofficemojo.com/search/?q={movie}")
            url = driver.find_element(By.XPATH, ".//a[@class='a-size-medium a-link-normal a-text-bold']").get_attribute(
                "href")
            driver = obj.get_url(url)
            return driver.find_elements(By.CLASS_NAME, "money")[2].text
        except:
            return "NA"
    def get_actor2(self):
        driver = obj.get_url("https://www.google.com/search?q=" + str(self.movie) + " director")
            # element = driver.find_element(By.CLASS_NAME, "FLP8od")
            # element_text = element.text
        return driver.page_source




#
#
# director_list=[]
# actor_list=[]
# primary_genre_list=[]
# secondary_genre_list=[]
#
#
# #just add things you want to pretty simple. I think this sucks but small issue to add data at end.
#
# #maybe try parrell requests
#
# #maybe add row by time
# # movie=movie_get(movies_list[-1])
# #
# # primary,secondary=movie.get_genre()
# # sheet.update_row(len(movies_list)+1,[movie.get_actor(),movie.get_director(),primary,secondary,movie.get_box_office()], col_offset=5)
# box_office_list=[]
# for i in movies_list:
#     movie=movie_get(i)
#     box_office_list.append(movie.get_box_office())
#
# sheet.update_col(10,box_office_list, row_offset=1)
#
#
#
#
#     # genre=movie.get_genre()
#     # primary_genre_list.append(genre[0])
#     # secondary_genre_list.append(genre[1])
#
#
#
# for i in range(len(director_list)):
#     if director_list[i]== "":
#         director_list[i]= "NA"
#     else:
#         pass
#
#
# index_na=[i for i, e in enumerate(director_list) if e =="NA"]
# c = [ movies_list[i] for i in index_na]
#
# new_na_list=[]
# #
# for i in range(len(c)):
#     movie=movie_get(c[i])
#     director=movie.get_director()
#     new_na_list.append(director)
#
# index=0
# for i in index_na:
#     director_list[i]=new_na_list[index]
#     index=index+1
#
# list_of_attrib=director_list,actor_list,primary_genre_list, secondary_genre_list
#
#
# #LOOOKO segfs
# for i in list_of_attrib:
#     print(i)
#     #conditional format
#     # https: // pygsheets.readthedocs.io / en / stable / chart.html
#     # wks.add_conditional_formatting('A1', 'A4', 'NUMBER_BETWEEN', {'backgroundColor': {'red': 1}}, ['1', '5'])
#     # sheet.update_col(index,i)
#     index=index+1
#
