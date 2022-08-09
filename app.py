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

station = st.selectbox("Pick a Couche-Tard gas station to analyze", df2['address'].unique())
station2 = st.selectbox("Pick a Shell gas station to analyze", df1['name'].unique())

pickedLat = float(df2[df2['address']==station]['latitude'])
pickedLong = float(df2[df2['address']==station]['longitude'])
pickedLat2 = float(df1[df1['name']==station2]['lat'])
pickedLong2 = float(df1[df1['name']==station2]['lng'])

st.write("""Couche-Tarde Gas Station: {}  \n Lat: {}  \n Lon: {}""".format(station, pickedLat, pickedLong))
st.write(df2[df2['address']==station])
st.write("""Shell Gas Station: {}  \n Lat: {}  \n Long: {}""".format(station2, pickedLat2, pickedLong2))
st.write(df1[df1['name']==station2])
distKM = distCoordKM(pickedLat, pickedLong, pickedLat2, pickedLong2)
st.write("Distance between gas stations in KM: **{:,.2f}**".format(distKM))

st.header("Find Closest Gas Stations")
brand = st.radio("Pick the gas station to analyze", ('Couche-Tard', 'Shell'))
radius = st.number_input('Insert a radius (metres)', value=2500)
if brand == 'Couche-Tard':
  mainStation = station
  lat = pickedLat
  lon = pickedLong
else:
  mainStation = station2
  lat = pickedLat2
  lon = pickedLong2

df1['Distance KM'] = df1.apply(lambda x: distCoordKM(lat, lon, x['lat'], x['lng']), axis=1)
df2['Distance KM'] = df2.apply(lambda x: distCoordKM(lat, lon, x['latitude'], x['longitude']), axis=1)

df1 = df1.sort_values('Distance KM')
df2 = df2.sort_values('Distance KM')
cols = ['Distance KM'] + list(df1.columns[0:-1])
st.write(cols)
# df1 = df1[cols]
# cols = ['Distance KM'] + df2.columns[0:-1]
# df2 = df2[cols]


radiusKM = radius / 1000
st.write("Couche-Tard locations within radius:")
st.write(df2[df2['Distance KM']<=radiusKM])
st.write("Shell locations within radius:")
st.write(df1[df1['Distance KM']<=radiusKM])

m = drawMap(df1, df2, lat, lon, radius)


# call to render Folium map in Streamlit
st_data = st_folium(m, width = 800)

st.header("All Shell Locations")
st.dataframe(df1)

st.header("All Couche-Tard Locations")
st.dataframe(df2)
