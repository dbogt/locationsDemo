import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

df1 = pd.read_csv('locations1.csv')

m = folium.Map(location=[56.0659, -118.3917], zoom_start=16)
# folium.Marker(
#   [39.949610, -75.150282], 
#   popup="Liberty Bell", 
#   tooltip="Liberty Bell"
# ).add_to(m)


# Creating the map and adding points to it

for index, location_info in df1.iterrows():
    folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["name"]).add_to(m)

st.title("Gas Station Locations")
# call to render Folium map in Streamlit
st_data = st_folium(m, width = 725)

st.dataframe(df1)
