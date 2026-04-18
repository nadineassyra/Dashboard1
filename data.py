import streamlit as st
import pandas as pd

# Fungsi untuk memuat data
def load_data():
    df = pd.read_csv("dataset\covid_19_indonesia_time_series_all.csv")
    return df

# Fungsi untuk menampilkan data dalam bentuk tabel
def show_data():
    df = load_data()
    st.subheader("📌 Data COVID-19 Indonesia")
    st.dataframe(df.head(10)) # Menampilkan 10 data pertama
    
# Menampilkan statistik deskriptif dataset
    st.subheader("📊 Statistik Deskriptif Dataset")
    st.write(df.describe()) # Menampilan statistik deskriptif
    
# Total kasus keseluruhan
    total_cases = df["Total Cases"].sum()
    st.subheader("Total Kasus Keseluruhan")
    st.write(total_cases)
    
# Kolom location sampai total recovery
    st.subheader("Data Kolom Tertentu")
    data_kolom = df.loc[:, "Location":"Total Recovered"]
    st.dataframe(data_kolom)

# Copyright
    st.write("© Nadine Assyra - NPM: 12345678")
    
    