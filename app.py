import os
import time
import json
import pygsheets
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
# scope = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
# with open("movie.json") as source:
#     info = json.load(source)
# creds = service_account.Credentials.from_service_account_info(info)

# creds= ServiceAccountCredentials.from_json_keyfile_name("/Users/zachkarol/Movie_project/movie-project-330118-9bf05ce7085e.json", scope)
#



import streamlit as st
from main import movie_get





# @st.cache
# def movie_sheet():
#     sheet = client.open("Movie_proj").sheet1
#     df = pd.DataFrame(sheet.get_all_records())
#     df = df.replace("", None)
#     df = df.replace(" ", None)
#     movie_data_frame = df.replace("NA", None)
#     return movie_data_frame



st.title('Zach Karol Movie Site')



rad=st.sidebar.radio("Navigation",["search","database"])



#this removes index colums

# df = pd.DataFrame(movie_sheet())
# df.fillna(0)
# df = df.iloc[:,[0, 1,5,6]]


st.markdown("""
<style>
table td:nth-child(1) {
    display: none
}
table th:nth-child(1) {
    display: none
}
</style>
""", unsafe_allow_html=True)



if rad=="search":
    text_input = st.text_input("enter movie get director")
    if(text_input==""):
        st.write("enter movie")
    else:
        movie = movie_get(str(text_input))
        ##add more stuff and fix dataframe issue. Each colums needs to be same type. Also weird issue with spaces
        d = {"movie": [str(text_input)], "actor": [movie.get_actor()], "director": [movie.get_director()], "box office": [str(movie.get_box_office())]}
        df = pd.DataFrame(data=d)
        df.replace("Na", "unknown", inplace=True)
        df.replace("Na/NA", "unknown", inplace=True)
        st.table(d)
if rad=="database":
    st.write("upcoming feature")
