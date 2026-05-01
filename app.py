import streamlit as st
from data import *

def judul(): 
# Judul Dashboard
    st.title("😷 Dashboard COVID-19")
    st.write("Selamat datang di dashboard interaktif untuk menganalisis data COVID-19 di Indonesia")

st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih halaman", ["Home", "Halaman Data"])

st.sidebar.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 10px;
        left: 10px;
        width: 200px;
        font-size: 12px;
        color: gray;
    }
    </style>

    <div class="footer">
        © Nadine Assyra - NPM: 12345678
    </div>
    """,
    unsafe_allow_html=True
)

if menu == "Home":
    judul()
    # Load & filter data
    df = load_data()
    # Pilih tahun
    year = select_year()
    locations = select_location(df)
    df_filtered = filter_data(df, year, locations)
    kolom(df_filtered)
    pie_chart1(df_filtered)
    
    # Bar chart
    bar_chart1(df_filtered)
    bar_chart2(df_filtered)
    map_chart(df_filtered)
    
    # Copyright
    st.write("© Nadine Assyra - NPM: 12345678")
    
elif menu == "Halaman Data":
    judul()
    year = select_year()
    df = load_data()
    df_filtered = filter_data(df, year)
    show_data(df_filtered)
    
    st.write("© Nadine Assyra - NPM: 12345678")

