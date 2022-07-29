import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

@st.cache
def grabDF1():
  df = pd.read_csv('locations1.csv')
  return df

@st.cache
def grabDF2():
  df = pd.read_csv('locations2.csv')
  return df

df1 = grabDF1()
df2 = grabDF2()

def drawMap(df1, df2):
  m = folium.Map(location=[56.0659, -118.3917], zoom_start=5)
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

m = drawMap(df1, df2)

st.title("Gas Station Locations")

station = st.selectbox("Pick a gas station to analyze", sorted(df2['address'].unique()))
pickedLat = df2[df2['address']==station]['latitude']
pickedLong = df2[df2['address']==station]['longitude']
city = df2[df2['address']=station]['city']
st.write("Station: {}".station)
st.write("City: {}".city)
st.write("Latitude: {}".pickedLat)
st.write("Longitude: {}".pickedLong)
st.write(df2[df2['address']==station].T)

# call to render Folium map in Streamlit
st_data = st_folium(m, width = 800)

st.header("Shell Locations")
st.dataframe(df1)

st.header("Couche-Tard Locations")
st.dataframe(df2)
