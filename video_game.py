from Selenium_functions import requester
from selenium.webdriver.common.by import By





from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlunsplit, urlencode
from selenium.webdriver.common.by import By


obj=requester()

class videogame_getter:
    def __init__(self, game):
        self.game = str(game)
    def get_info(self):
        driver = obj.get_url("https://videogamegeek.com/")
        search = driver.find_element(By.XPATH, "(//input[@id='site-search'])")
        search.send_keys(self.game)
        search.send_keys(Keys.RETURN)
        page = BeautifulSoup(driver.page_source, "html.parser")
        div = page.find("div", class_="geekitem_linkeditems_title")
        end_of_url = str(div.find("a")['href'])
        end_of_url.split('/')[2]
        scheme = "https"
        netloc = "videogamegeek.com"
        path = "xmlapi2/thing"
        query_string = urlencode(dict(id=end_of_url.split('/')[2]))
        page = BeautifulSoup(requests.get(urlunsplit((scheme, netloc, path, query_string, ""))).content, "lxml")
        platforms = [x["value"] for x in page.find_all(type="videogameplatform")]
        genre = page.find(type="videogamegenre")["value"]
        release_date = page.find("releasedate")["value"]
        developer = page.find(type="videogamedeveloper")["value"]
        return platforms, genre, release_date, developer



















