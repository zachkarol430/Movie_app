import gspread
from bs4 import BeautifulSoup
import requests
import time
import json
import pygsheets
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.common.by import By
from random import uniform
from Selenium_functions import requester
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from selenium.webdriver.common.action_chains import ActionChains


obj=requester()

scope = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]


with open("/Users/zachkarol/Movie_project/movie-project-330118-9bf05ce7085e.json") as source:
    info = json.load(source)
creds = service_account.Credentials.from_service_account_info(info)

# creds= ServiceAccountCredentials.from_json_keyfile_name("/Users/zachkarol/Movie_project/movie-project-330118-9bf05ce7085e.json", scope)
client=pygsheets.authorize(service_account_file="/Users/zachkarol/Movie_project/movie-project-330118-9bf05ce7085e.json")

sheet=client.open("Jojo_info").sheet1

class cancer_info:
    def __init__(self, cancer_type):
        self.cancer_type= cancer_type

    def reach_page(self,gene):
        driver = obj.get_url("https://www.proteinatlas.org/search/" + str(gene))
        element = driver.find_element(By.XPATH, ".//td[@class='wrap maxwidth']/a").get_attribute("href")
        url= (F"{element}/pathology/{self.cancer_type}")
        return url

    def make_table(self, gene):
        #PASS in url from reach page
        driver=obj.get_url(self.reach_page(gene))
        element = driver.find_elements(By.CLASS_NAME, "nowrap")
        button2 = driver.find_element(By.CLASS_NAME, "show_hidden.grey")
        element[0].location_once_scrolled_into_view
        #need better way to press show all but suffice for now
        button2.click()
        id_tags = []
        for i in range(len(element)):
                element_text = element[((3 * i))].text, element[((3 * i) + 1)].text, element[((3 * i) + 2)].text
                if element[((3 * i))].text=="  High":break
                id_tags.append(element_text)
        df = np.array([np.array(xi) for xi in id_tags])
        data_frame= pd.DataFrame(df, columns=[f"{self.cancer_type} sample","descrip","fpkm"])
        return data_frame
    def two_gene(self, gene1, gene2):
        col_name= f"{self.cancer_type} sample"
        df1=self.make_table(gene1)
        df2=self.make_table(gene2)
        df4=pd.merge(df1[[col_name,"fpkm"]],df2[[col_name,"fpkm"]], how="inner", on=col_name,suffixes=(" "+str(gene1)," "+ str(gene2)))
        return df4
    def update(self, dataframe,col_number):
        dataframe.loc[-1] = list(dataframe.columns.values)
        dataframe.index = dataframe.index + 1
        dataframe = dataframe.sort_index()
        df= dataframe.transpose()
        df= df.values.tolist()
        sheet.update_col(col_number, df)




#sort list alphabetically than match ids and graph fpkm
pd.set_option('display.max_columns',10)
cancer=cancer_info("melanoma")
df=cancer.make_table("VIP")
cancer.update(df,5)











