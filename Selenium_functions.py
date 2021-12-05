from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from selenium.webdriver.common.proxy import Proxy,ProxyType
import os
from selenium import webdriver


from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

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

path= "/Users/zachkarol/Downloads/chromedriver 2"
s=Service(os.environ.get('CHROMEDRIVER_PATH'))


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')


# you can also import SoftwareEngine, HardwareType, SoftwareType, Popularity from random_user_agent.params
# you can also set number of user agents required by providing `limit` as parameter





class requester:
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
        chrome_options.add_argument("window-size=1400,900")
        chrome_options.add_argument(f"user-agent={user_agent}")
        chrome_options.add_argument("--disable-dev-shm-usage")
    def get_url(self,url):
        self.add_options()
        driver = webdriver.Chrome(service=s, options=chrome_options)##add desired capbilites for proxt
        driver.get(url)
        return driver

