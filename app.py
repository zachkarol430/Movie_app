import os
import time
import json
import pygsheets

from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.common.by import By
import pandas as pd
import gc
import numpy as np




import streamlit as st
from main import movie_get


@st.cache
def movie_sheet():
    client = pygsheets.authorize(service_account_file="movie.json")
    sheet = client.open("Movie_proj").sheet1
    matrix = sheet.range("A:B", returnas="matrix")
    df = pd.DataFrame(matrix)
    nan_value = float("NaN")
    df.replace("", nan_value, inplace=True)
    df.dropna(how='all', axis=0, inplace=True)
    df = df.rename(columns=df.iloc[0]).drop(df.index[0])
    return df


gc.collect()

st.title('Zach Karol Movie Site')



rad=st.sidebar.radio("Navigation",["search","database"])






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


try:
    if rad=="search":
        text_input = st.text_input("enter movie")
        if(text_input==""):
            st.write("enter movie above")
        else:
            movie = movie_get(str(text_input))
            actor= movie.get_actor()
            if actor=="NA": actor=movie.get_actor()
            ##add more stuff and fix dataframe issue. Each colums needs to be same type. Also weird issue with spaces
            d = {"movie": [str(text_input)], "actor": [actor], "director": [movie.get_director()], "box office": [str(movie.get_box_office())]}
            df = pd.DataFrame(data=d)
            df.replace("Na", "unknown", inplace=True)
            df.replace("Na/NA", "unknown", inplace=True)
            st.table(d)
    if rad=="database":
        st.dataframe(data=movie_sheet(),height=700)
except:
    st.write("reload page :)")

