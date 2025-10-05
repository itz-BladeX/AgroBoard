import streamlit as st
# import weather
import supplementary as sup
import shelve
import streamlit_option_menu as om
import time
from streamlit_javascript import st_javascript
st.set_page_config(page_title="AGRO-BOARD", layout="wide", )
st.logo("logo.png")

width = st_javascript("window.innerWidth", key="main_width")
sup.render_nav("main", width)
time.sleep(0.5)

st.markdown("""
<style>
    /* Target the default nav section in sidebar */
    [data-testid="stSidebar"] > div > div > div > section > div:first-child {
        display: none !important;
    }
    /* Alternative selector if above doesn't catch it (more broad) */
    /* section[data-testid="stSidebar"] nav { display: none !important; } */
</style>
""", unsafe_allow_html=True)


crop = "crop_database"
livestock = "livestock_database"
inventory = "inventory_database"

with st.container():  # Weather Section
    st.markdown("""   
    <style text-align: center>
    [data-testid="stMetricLabel"],
    [data-testid="stTitle"],
    [data-testid="stMetric"] {
        text-align: center !important;
        display: block !important;
    }
    </style>          
    <h1 style="color: white; text-align: center; font-family: Arial, sans-serif;"> Today's Weather Report </h1>
    """, unsafe_allow_html=True)  # CSS Styling for the st.metric and Title

    st.divider()
    matric_col1, matric_col2, matric_col3, matric_col4 = st.columns(4)
    st.set_page_config(page_title="AGRO-BOARD", layout="wide")
    with st.spinner("Fetching Weather Data..."):
        with matric_col1:
            st.metric(label="Temperature", value=sup.get_weather('temp'), border=True)
        with matric_col2:
            st.metric("Wind Speed", sup.get_weather('wind'), border=True)
        with matric_col3:
            st.metric("Precipitation", sup.get_weather('rainfall'), border=True)
        with matric_col4:
            st.metric("Weather Station", sup.get_weather('station'), border=True)

    st.divider()

# Widgets

st.markdown("""

<h1 style="color: white; text-align: center; font-family: Arial, sans-serif;"> Statistics and Data </h1>


""", unsafe_allow_html=True)
# Crop
with st.expander("See Crop Data"):
    st.markdown("""
<h1 style="color: white; text-align: center; font-family: Arial, sans-serif;"> Crops </h1>
""", unsafe_allow_html=True)
    heights = [200,260, 200, 260]
    with shelve.open(crop) as db:
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]
        i = 0
        for id in db.keys():
            height = heights[i]
            with cols[i]:
                with st.container(border=True):
                    left, right = st.columns(2)
                    with left:
                        st.metric(label=" ", value=f"ID: {db[id].id}", delta=f"{sup.percent_complete(id, crop)} %")
                    with right:
                        st.metric(label=" ", value=db[id].type)
                    st.altair_chart(sup.alter_graph(id, crop, height), use_container_width=True)
            if i >= 3:
                i = 0
                heights = heights[::-1]
            else:
                i += 1
            
    # Livestock

with st.expander("See LiveStock Data"):
    st.markdown("""<h1 style=" color: white; text-align: center; font-family: Arial, sans-serif;"> LiveStocks </h1>""", unsafe_allow_html=True)
    heights = [200,260, 200, 260]
    with shelve.open(livestock) as db:
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]
        i = 0
        for id in db.keys():
            height = heights[i]
            with cols[i]:
                with st.container(border=True):
                    left, right = st.columns(2)
                    with left:
                        st.metric(label=" ", value=f"ID: {db[id].id}", delta=f"{sup.percent_complete(id, livestock)} %")
                    with right:
                        st.metric(label=" ", value=db[id].type)
                    st.altair_chart(sup.alter_graph(id, livestock, height), use_container_width=True)
            if i >= 3:
                i = 0
                heights = heights[::-1]
            else:
                i += 1
            
