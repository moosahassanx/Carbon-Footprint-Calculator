import streamlit as st
import os
from predict_page import show_predict_page
from explore_page import show_explore_page

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
page = st.sidebar.selectbox("Menu", ("Carbon Footprint Calculator", "ML Model"))

if page == "ML Model":
    show_predict_page()
else:
    show_explore_page()