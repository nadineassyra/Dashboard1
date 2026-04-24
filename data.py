import streamlit as st
import pandas as pd
import plotly.express as px

# Fungsi untuk memuat data
def load_data():
    df = pd.read_csv("dataset\covid_19_indonesia_time_series_all.csv")
    return df

def filter_data(df, year=None):
    if year:
        df = df[df['Date'].astype(str).str.contains(str(year))]
    return df

def select_year():
    return st.sidebar.selectbox(
        "Pilih Tahun 📅",
        options=[None, 2020, 2021, 2022],
        format_func=lambda x: "Semua Tahun" if x is None else str(x)
    )

# Fungsi untuk menampilkan data dalam bentuk tabel
def show_data(df):
    selected_columns = ['Location'] + list(df.loc[:, 'New Cases':'Total Recovered'].columns)
    df_selected = df[selected_columns]
    st.subheader("Data COVID-19 Indonesia 🔴⚪")
    st.dataframe(df_selected.head(10)) # Menampilkan 10 data pertama

# Total kasus
def total_case(df):
    df = load_data()
    total_kasus = df['New Cases'].sum()
    return total_kasus

# Total Death
def total_death(df):
    df = load_data()
    total_kematian = df['New Deaths'].sum()
    return total_kematian
    
# Total_sembuh
def total_recovery(df):
    df = load_data()
    total_sembuh = df['New Recovered'].sum()
    return total_sembuh

# Kolom 1
def kolom(df):
    kasus = total_case(df)
    kematian = total_death(df)
    sembuh = total_recovery(df)
    
    co11, co12, co13 = st.columns(3)
    co11.metric(label="Total Kasus 📈", value=kasus, border=True)
    co12.metric(label="Total Kematian 💀", value=kematian, border=True)
    co13.metric(label="Total Sembuh 🏋️‍♀️", value=sembuh, border=True)

# Piechart1
def pie_chart1(df):
    total_mati = total_death(df)
    total_sumbuh = total_recovery(df)
    
    data ={
        'Status' : ['Meninggal', 'Sembuh'],
        'Jumlah' : [total_mati,total_sumbuh]
        }
        
    fig = px.pie(   
        data,
        names='Status',
        values='Jumlah',
        title='Perbandingan Total Kematian VS Total Kesembuhan',
        hole=0.5,
        color_discrete_sequence=['#4de89f', '#ff6459']
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    