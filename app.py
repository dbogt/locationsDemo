#%% Import Packages
import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from math import pi, acos, sin, cos, sqrt, atan2, radians

#%% Functions
#Grabbing Data
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

#Mapping
def drawMap(df1, df2, lat, long, radiusM):
  m = folium.Map(location=[lat, long], zoom_start=12)
  #Plot Shell Canada
  for index, location_info in df1.iterrows():
    pop = """<b>Shell Canada</b></br>
    {}
    """.format(location_info["name"])
    folium.Marker([location_info["lat"], location_info["lng"]], popup=pop, icon=folium.Icon(color="red")).add_to(m)
  
  #Plot Couche-Tard
  for index, location_info in df2.iterrows():
    city =location_info['city']
    address =location_info['address']
    pop = """<b>Couche-Tard</b></br>
    {}
    """.format(address)
    folium.Marker([location_info["latitude"], location_info["longitude"]], popup=pop, icon=folium.Icon(color="blue")).add_to(m)

  #Plot Radius
  folium.Circle(
    radius=radiusM,
    location=[lat, long],
    popup="{} m radius".format(radiusM),
    color="crimson",
    fill=False,
).add_to(m)

  return m

#Distance Calculations
def distCoord(Lat_place_1, Lon_place_1, Lat_place_2, Lon_place_2):
  lat1 = radians(Lat_place_1) # same as * pi / 180
  lat2 = radians(Lat_place_2)
  lon1 = radians(Lon_place_1)
  lon2 = radians(Lon_place_2)
  piNum = pi
  #distance in nautical miles
  distNM = acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1)) * 3443.8985
  return distNM

def distCoordKM(lat1, lon1, lat2, lon2):
  distKM = distCoord(lat1, lon1, lat2, lon2) * 1.852
  return distKM

st.title("Gas Station Locations")

station = st.selectbox("Pick a gas station to analyze", sorted(df2['address'].unique()))
station2 = st.selectbox("Pick a second gas station to analyze", sorted(df2['address'].unique()))
number = st.number_input('Insert a radius (m)', value=1000)
pickedLat = float(df2[df2['address']==station]['latitude'])
pickedLong = float(df2[df2['address']==station]['longitude'])
pickedLat2 = df2[df2['address']==station2]['latitude']
pickedLong2 = df2[df2['address']==station2]['longitude']

m = drawMap(df1, df2, pickedLat, pickedLong, number)
city = df2[df2['address']==station]['city']
# st.write("Station: {}".format(station))
# st.write("City: {}".format(city))
st.write(pickedLat)
st.write(pickedLong)

st.write(df2[df2['address']==station])
st.write(df2[df2['address']==station2])
st.write("""Gas Station 1: {}
            Lat:{}
            Lon:{}""".format(station, pickedLat, pickedLong))
st.write("Gas Station 2: {} \nLat:{}\nLon:{}".format(station2, pickedLat2, pickedLong2))
distKM = distCoordKM(pickedLat, pickedLong, pickedLat2, pickedLong2)
st.write("Distance in KM: {:,.2f}".format(distKM))

# call to render Folium map in Streamlit
st_data = st_folium(m, width = 800)

st.header("Shell Locations")
st.dataframe(df1)

st.header("Couche-Tard Locations")
st.dataframe(df2)
