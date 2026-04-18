import streamlit as st
from data import *

def judul(): 
# Judul Dashboard
    st.title("📊 Dashboard COVID-19")
    st.write("Selamat datang di dashboard interaktif untuk menganalisis data COVID-19 di Indonesia")

st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih halaman", ["Home", "Halaman Data"])

if menu == "Home":
    judul()
    # Copyright
    st.write("© Nadine Assyra - NPM: 12345678")
elif menu == "Halaman Data":
    judul()
    show_data()

