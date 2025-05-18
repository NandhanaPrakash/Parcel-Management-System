import folium
from geopy.geocoders import Nominatim

address = ' Kolathur Chennai TamilNadu 600082'
geolocator = Nominatim(user_agent='location')
location = geolocator.geocode(address)
coor = (location.latitude,location.longitude)

map = folium.Map(location=coor, zoom_start=11)

