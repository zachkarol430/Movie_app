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
import concurrent.futures




import streamlit as st
from movie import movie_get
from video_game import videogame_getter

def main():
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
    df=movie_sheet()
    movie_list=list(df.loc[:, "Movie"])

    gc.collect()

    st.title('Zach Karol Movie Site')



    rad=st.sidebar.radio("Navigation",["search","movie database"])







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
        search_for = st.radio("Search for", ["Movie", "Videogame"])
        if search_for == "Videogame":
            text_input= st.text_input("enter video game")
            video_game = videogame_getter(str(text_input))
            if text_input != '':
                info = video_game.get_info()
                d = {"videogame": [str(text_input)], "release date": [info[2]],
                    "publisher": [info[3]], "genre": [info[1]], "platform": [info[0]]}
                st.table(d)
        if search_for=="Movie":
            text_input = st.text_input("enter movie, enter exact movie, don't enter star wars for example")
            if text_input=="":
                st.write("enter movie above")
            else:
                movie = movie_get(str(text_input))
                movie.get_info()
                # # #no commment lol while loop memory leak
                # # ##add more stuff and fix dataframe issue. Each colums needs to be same type. Also weird issue with spaces
                d = {"movie": [str(text_input)], "actor": [movie.actor],
                     "director": [movie.director], "box office": [movie.box_office]}
                st.table(d)
                if text_input.lower() in (i.lower().strip() for i in movie_list):
                    index=df[df['Movie'].str.lower().str.strip() == str(text_input).lower()].index[0]
                    rating=df.iloc[:,1].iloc[index-1]
                    st.write(f"Zach Karol gave this movie a {rating}")

    if rad=="movie database":
        st.dataframe(data=df,height=700)

if __name__ == "__main__":
    main()