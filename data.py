import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Fungsi untuk memuat data
def load_data():
    file_path = Path(__file__).parent / "dataset" / "covid_19_indonesia_time_series_all.csv"
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df['Location'] != 'Indonesia']
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

# Fungsi untuk total kasus
def total_case(df):
    total_kasus = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_kasus['Total Cases'].sum()


# Fungsi untuk total kematian
def total_death(df):
    total_kematian = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_kematian['Total Deaths'].sum()


# Fungsi untuk total sembuh
def total_recovery(df):
    total_sembuh = df.sort_values('Date').groupby('Location', as_index=False).last()
    return total_sembuh['Total Recovered'].sum()

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
    
# Barchart1
def bar_chart1(df):
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    top5 = df_last.nlargest(5, 'Total Deaths')

    fig = px.bar(
        top5,
        x='Location',
        y='Total Deaths',
        color='Total Deaths',
        color_continuous_scale='Reds',
        title='⚕️ 5 Provinsi dengan Kematian Tertinggi',
        labels={'Total Deaths': 'Total Kematian', 'Location': 'Provinsi'}
    )

    fig.update_layout(
        xaxis_title='Provinsi',
        yaxis_title='Total Kematian',
        title_x=0.5
    )

    st.plotly_chart(fig, use_container_width=True)


#Barchart2
def bar_chart2(df):
    df_last = df.sort_values('Date').groupby('Location', as_index=False).last()
    top5 = df_last.nlargest(5, 'Total Recovered')

    fig = px.bar(
        top5,
        x='Location',
        y='Total Recovered',
        color='Total Recovered',
        color_continuous_scale='Greens',
        title='⚕️ 5 Provinsi dengan Kesembuhan Tertinggi',
        labels={'Total Recovered': 'Total Kesembuhan', 'Location': 'Provinsi'}
    )

    fig.update_layout(
        xaxis_title='Provinsi',
        yaxis_title='Total Kesembuhan',
        title_x=0.5
    )

    st.plotly_chart(fig, use_container_width=True)


#Mapchart
def map_chart(df, year=None):
    df['Date'] = pd.to_datetime(df['Date'])

    if year:
        df = df[df['Date'].dt.year == year]

    df_agg = df.groupby(
        ['Location', 'Latitude', 'Longitude'],
        as_index=False
    )['New Cases'].sum()

    df_map = df_agg.dropna(subset=['Latitude', 'Longitude', 'New Cases'])

    if df_map.empty:
        st.info("⚠️ Tidak ada data untuk ditampilkan di peta.")
        return

    fig = px.scatter_mapbox(
        df_map,
        lat='Latitude',
        lon='Longitude',
        size='New Cases',
        color='New Cases',
        hover_name='Location',
        zoom=3,
        center={"lat": -2.5, "lon": 118},
        size_max=20,
        opacity=0.7,
        color_continuous_scale="OrRd",
        title=f"Sebaran Kasus Baru Covid-19 di Indonesia ({year if year else 'Semua Tahun'})"
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        height=600,
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )

    st.plotly_chart(fig, use_container_width=True)