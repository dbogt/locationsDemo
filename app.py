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

def drawMap(df1, df2, lat, long, radiusM):
  m = folium.Map(location=[lat, long], zoom_start=10)
  for index, location_info in df1.iterrows():
    folium.Marker([location_info["lat"], location_info["lng"]], popup=location_info["name"], icon=folium.Icon(color="red")).add_to(m)
  for index, location_info in df2.iterrows():
    city =location_info['city']
    address =location_info['address']
    pop = """<b>Couche-Tard</b></br>
    {}
    """.format(address)
    folium.Marker([location_info["latitude"], location_info["longitude"]], popup=pop, icon=folium.Icon(color="blue")).add_to(m)

  folium.Circle(
    radius=radiusM,
    location=[lat, long],
    popup="The Waterfront",
    color="crimson",
    fill=False,
).add_to(m)

  return m



st.title("Gas Station Locations")

station = st.selectbox("Pick a gas station to analyze", sorted(df2['address'].unique()))
number = st.number_input('Insert a radius (m)', value=1000)
pickedLat = df2[df2['address']==station]['latitude']
pickedLong = df2[df2['address']==station]['longitude']
m = drawMap(df1, df2, pickedLat, pickedLong, number)
city = df2[df2['address']==station]['city']
# st.write("Station: {}".format(station))
# st.write("City: {}".format(city))
# st.write("Latitude: {}".pickedLat)
# st.write("Longitude: {}".pickedLong)
st.write(df2[df2['address']==station])

# call to render Folium map in Streamlit
st_data = st_folium(m, width = 800)

st.header("Shell Locations")
st.dataframe(df1)

st.header("Couche-Tard Locations")
st.dataframe(df2)
