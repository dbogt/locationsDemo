#%% Import Packages
import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from math import pi, acos, sin, cos, sqrt, atan2, radians

#%% Streamlit Controls
st.set_page_config(layout="wide",page_title='Locations Finder',
menu_items={
        "About": f"Locations Finder"
        f"\nApp contact: [Bogdan Tudose](mailto:bogdan.tudose@marqueegroup.ca)",
        "Report a Bug": "https://github.com/dbogt/locationsDemo/issues/",
    })


#%% App Details
appDetails = """
Created by: [Bogdan Tudose](https://www.linkedin.com/in/tudosebogdan/) \n
Date: August 9, 2022 \n
Purpose: Compare gas station locations of two different companies (Couche-Tard and Shell) \n
This app is a demo of how Python could be used to augment a ficticious M&A deal:
- If Couche-Tard and Shell were to merge, the investment banking analyts working on the deal would try to find gas stations of the competing brands that are close to each other
- Gas stations close in proximity are potential targets for closures to create cost synergies 


How to use the app:
- Pick a Couche-Tard and Shell gas station (use the defaults as a starting point)
- The app will first calculate the distance in km between the 2 picked locations
- Pick which of the two stations to analyze and the radius proximity (in metres, default set to 2.5km)
- The app will then plot a radius of the chosen distance and filter out all the gas stations within that radius

At the bottom of the app you can also find all the locations, sorted by distance to the picked gas station.

Short link: https://bit.ly/locationsDemo
"""
with st.expander("See app info"):
    st.write(appDetails)


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

l1 = grabDF1()
l2 = grabDF2()
df1 = l1.copy()
df2 = l2.copy()

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

cLocs = list(df2['address'].unique()) #list of couche-tard locations
sLocs = list(df1['name'].unique()) #list of shell locations
idx1 = cLocs.index('2742 HIGHWAY 325')
idx2 = sLocs.index('CORP-LAHAVE ST')
station = st.selectbox("Pick a Couche-Tard gas station to analyze", cLocs, index=idx1, help="Try: 2742 HIGHWAY 325")
station2 = st.selectbox("Pick a Shell gas station to analyze", sLocs, index=idx2, help="Try: CORP-LAHAVE ST")

pickedLat = float(df2[df2['address']==station]['latitude'])
pickedLong = float(df2[df2['address']==station]['longitude'])
pickedLat2 = float(df1[df1['name']==station2]['lat'])
pickedLong2 = float(df1[df1['name']==station2]['lng'])

distKM = distCoordKM(pickedLat, pickedLong, pickedLat2, pickedLong2)
st.write("Distance between gas stations in KM: **{:,.2f}**".format(distKM))

st.write("""Couche-Tarde Gas Station: {}  \n Lat: {} Lon: {}""".format(station, pickedLat, pickedLong))
st.write(df2[df2['address']==station])
st.write("""Shell Gas Station: {}  \n Lat: {} Lon: {}""".format(station2, pickedLat2, pickedLong2))
st.write(df1[df1['name']==station2])

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
df1 = df1[cols]
cols2 = ['Distance KM'] + list(df2.columns[0:-1])
df2 = df2[cols2]


radiusKM = radius / 1000
st.write("Couche-Tard locations within radius:")
st.write(df2[df2['Distance KM']<=radiusKM])
st.write("Shell locations within radius:")
st.write(df1[df1['Distance KM']<=radiusKM])

m = drawMap(df1, df2, lat, lon, radius)


st.write("Blue markers are Couche-Tard gas station and red markers are Shell gas stations.")
# call to render Folium map in Streamlit
st_data = st_folium(m, width = 800)

st.header("All Shell Locations")
st.dataframe(df1)

st.header("All Couche-Tard Locations")
st.dataframe(df2)
