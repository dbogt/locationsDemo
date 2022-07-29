import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

df1 = pd.read_csv('locations1.csv')

@st.cache
def drawMap():
  m = folium.Map(location=[56.0659, -118.3917], zoom_start=16)
  for index, location_info in df1.iterrows():
    folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["name"], icon=folium.Icon(color="red")).add_to(m)
  for index, location_info in df2.iterrows():
    city =location_info['city']
    address =location_info['address']
    pop = """<b>Couche-Tard</b></br>
    {}
    """.format(address)
    folium.Marker([location_info["latitude"], location_info["longitude"]], popup=pop, icon=folium.Icon(color="blue")).add_to(m)

      
  return m

m = drawMap()

st.title("Gas Station Locations")
# call to render Folium map in Streamlit
st_data = st_folium(m, width = 800)

st.header("Shell Locations")
st.dataframe(df1)

st.header("Couche-Tard Locations")
st.dataframe(df2)
