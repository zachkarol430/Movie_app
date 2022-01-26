from bs4 import BeautifulSoup
import requests
import concurrent.futures


class video_game_get:
    def __init__(self, video_game):
        self.video_game= video_game
        self.release_date= None
        self.genre= None
        self.publisher= None
    def get_release_date(self):
        try:
            driver = requests.get("https://www.google.com/search?q=" + str(self.video_game) + " relase date")
            page = BeautifulSoup(driver.content, "html.parser")
            try:
                release_date = page.find("div", class_="BNeawe iBp4i AP7Wnd").text
            except:
                release_date = "NA"
        except:
            release_date = "Chrome crashed"
        finally:
            return release_date
    def get_publisher(self):
        try:
            driver = requests.get("https://www.google.com/search?q=" + str(self.video_game) + "  publishers")
            page = BeautifulSoup(driver.content, "html.parser")
            try: publisher = page.find("div", class_="kvKEAb").text
            except AttributeError:
                try:  publisher = page.find("div", class_="am3QBf").text
                except:
                    try: publisher = page.find("div", class_="BNeawe s3v9rd AP7Wnd").text
                    except: publisher = "NA"
            except:
                publisher = "NA"
        except:
            publisher = "NA"
        finally:
            if publisher== "Publisher(s)":
                try: publisher = page.find_all("div", class_="BNeawe s3v9rd AP7Wnd")[1].text
                except: publisher= "NA"
            return publisher
    def get_reviews(self):
        try:
            driver = requests.get("https://www.google.com/search?q=" + str(self.video_game) + " video game reviews")
            page = BeautifulSoup(driver.content, "html.parser")
            try:
                review = page.find("span", class_="oqSTJd").text ##this just grabs first revierw, but diff company have reviews. ill solve later
            except:
                review = "NA"
        except:
            review = "Chrome crashed"
        finally:
            return review
    def get_genre(self):
        try:
            driver = requests.get("https://www.google.com/search?q=" + str(self.video_game) + " video game genres")
            page = BeautifulSoup(driver.content, "html.parser")
            try: genre = page.find("div", class_="am3QBf").text
            except:
                try: genre = page.find("div", class_="BNeawe iBp4i AP7Wnd").text
                except:
                    try: genre= page.find("div", class_="BNeawe s3v9rd AP7Wnd").text
                    except: genre = "NA"
        except:
            genre = "Chrome crashed"
        finally:
            return genre
    def fix_genre(self):
        #this may be removed or fixed. Really niche
        genre=self.get_genre()
        for i in range(len(genre)-1):
            if genre[i].islower() and genre[i+1].isupper():
                genre= genre[0:i+1]
                break
        return genre
    def get_info(self):
        list_foo = [self.get_release_date, self.fix_genre, self.get_publisher]
        with concurrent.futures.ProcessPoolExecutor() as executor:
            thread = [executor.submit(foo) for foo in list_foo]
        results = [x.result() for x in thread]
        self.release_date = results[0]
        self.genre = results[1]
        self.publisher = results[2]




