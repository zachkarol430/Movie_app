import os
import time
import json
import pygsheets

from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np

client=pygsheets.authorize(service_account_file="movie.json")

import streamlit as st
from main import movie_get




#
# @st.cache
# def movie_sheet():
#     sheet = client.open("Movie_proj").sheet1
#     matrix = sheet.range("A:B", returnas="matrix")
#     df = pd.DataFrame(matrix)
#     nan_value = float("NaN")
#     df.replace("", nan_value, inplace=True)
#     df.dropna(how='all', axis=0, inplace=True)
#     df = df.rename(columns=df.iloc[0]).drop(df.index[0])
#     return df




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
    st.write("lol")
