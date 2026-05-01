import streamlit as st
import pandas as pd
import plotly.express as px

# Fungsi untuk memuat data
def load_data():
    df = pd.read_csv("dataset/covid_19_indonesia_time_series_all.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def filter_data(df, year=None, locations=None):
    df = df[df['Location Level'] == 'Province']

    if year:
        df = df[df['Date'].dt.year == year]

    if locations:
        df = df[df['Location'].isin(locations)]

    return df

def select_year():
    return st.sidebar.selectbox(
        "Pilih Tahun 📅",
        options=[None, 2020, 2021, 2022],
        format_func=lambda x: "Semua Tahun" if x is None else str(x)
    )

def select_location(df):
    df_provinsi = df[df['Location Level'] == 'Province']

    return st.sidebar.multiselect(
        "Pilih Provinsi 📍",
        options=sorted(df_provinsi['Location'].dropna().unique()),
        default=[]
    )
    
# Fungsi untuk menampilkan data dalam bentuk tabel
def show_data(df):
    selected_columns = ['Location'] + list(df.loc[:, 'New Cases':'Total Recovered'].columns)
    df_selected = df[selected_columns]
    st.subheader("Data COVID-19 Indonesia 🔴⚪")
    st.dataframe(df_selected.head(10)) # Menampilkan 10 data pertama

# Total kasus
def total_case(df):
    df_last = df.sort_values('Date').groupby('Location').tail(1)
    return df_last['Total Cases'].sum()

def total_death(df):
    df_last = df.sort_values('Date').groupby('Location').tail(1)
    return df_last['Total Deaths'].sum()

def total_recovery(df):
    df_last = df.sort_values('Date').groupby('Location').tail(1)
    return df_last['Total Recovered'].sum()

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
    

def bar_chart1(df):
    df_death = (
        df.groupby('Location')['New Deaths']
        .sum()
        .reset_index()
        .sort_values('New Deaths', ascending=False)
        .head(5)
    )

    fig = px.bar(
        df_death,
        x='Location',
        y='New Deaths',
        color='New Deaths',
        color_continuous_scale='Reds',
        title='⚕️ 5 Provinsi dengan Kematian Tertinggi',
        labels={
            'Location': 'Provinsi',
            'New Deaths': 'Total Kematian'
        }
    )

    st.plotly_chart(fig, use_container_width=True)


def bar_chart2(df):
    df_recovered = (
        df.groupby('Location')['New Recovered']
        .sum()
        .reset_index()
        .sort_values('New Recovered', ascending=False)
        .head(5)
    )

    fig = px.bar(
        df_recovered,
        x='Location',
        y='New Recovered',
        color='New Recovered',
        color_continuous_scale='Greens',
        title='⚕️ 5 Provinsi dengan Kesembuhan Tertinggi',
        labels={
            'Location': 'Provinsi',
            'New Recovered': 'Total Kesembuhan'
        }
    )

    st.plotly_chart(fig, use_container_width=True)
    
    
def map_chart(df):
    df_map = (
        df.groupby(['Location', 'Latitude', 'Longitude'])['New Cases']
        .sum()
        .reset_index()
    )

    fig = px.scatter_mapbox(
        df_map,
        lat='Latitude',
        lon='Longitude',
        size='New Cases',
        color='New Cases',
        color_continuous_scale='OrRd',
        hover_name='Location',
        hover_data={'New Cases': True},
        title='Sebaran Kasus Baru Covid-19 di Indonesia',
        zoom=3.5,
        height=600
    )

    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(margin={"r":0, "t":50, "l":0, "b":0})

    st.plotly_chart(fig, use_container_width=True)