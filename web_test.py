from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from selenium.webdriver.common.proxy import Proxy,ProxyType


# proxy_list=[]
#
# proxy_ip_port= "fe80::aede:48ff:.49159"
# proxy=Proxy()
# proxy.proxy_type= ProxyType.MANUAL
# proxy.http_proxy=proxy_ip_port
# proxy.ssl_proxy=proxy_ip_port
#
# capabilities = webdriver.DesiredCapabilities.CHROME
# proxy.add_to_capabilities(capabilities)



#ADD DESIRED CAPBILITY IF WANT TO USE PROXY AGAIN> ADD TO DRIBER IN GET URL



from selenium import webdriver


from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

# you can also import SoftwareEngine, HardwareType, SoftwareType, Popularity from random_user_agent.params
# you can also set number of user agents required by providing `limit` as parameter

chrome_options = webdriver.ChromeOptions()
import random



class requester:
    def __init__(self):
        path = "/Users/zachkarol/Downloads/chromedriver 2"
        self.s = Service(path)
    def get_user_agent(self):
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value,OperatingSystem.MACOS.value]
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
        user_agents = user_agent_rotator.get_user_agents()
        user_agent = user_agent_rotator.get_random_user_agent()
        return user_agent
    def add_options(self):
        user_agent = self.get_user_agent()
        chrome_options.add_argument("--incognito")
        # chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument(f"user-agent={user_agent}")
        chrome_options.add_argument("--disable-dev-shm-usage")
    def get_url(self,url):
        self.add_options()
        driver = webdriver.Chrome(service=self.s, options=chrome_options)##add desired capbilites for proxt
        driver.get(url)
        return driver








from bs4 import BeautifulSoup
import requests
import concurrent.futures
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlunsplit, urlencode
obj = requester()

class video_game:
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
        publisher = page.find(type="videogamepublisher")["value"]
        return platforms, genre, release_date, publisher

video= video_game("overwatch")

print(video.get_info())












# url= "https://videogamegeek.com"+ end_of_url
# page =requests.get(url)
# page= BeautifulSoup(page.content, "html.parser")
# info_table= page.find_all("table", class_="geekitem_infotable")[0]
# print(info_table.find_all('tr')[2])
# print(page)








