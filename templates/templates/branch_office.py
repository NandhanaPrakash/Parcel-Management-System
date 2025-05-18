import folium
from geopy.geocoders import Nominatim

branch_offices = [
    "Mylapore 600028 Chennai",
    "Tambaram 600046 Chennai",
    "Anna Nagar 600040 Chennai",
    "West Mambalam 600033 Chennai",
    "Nandanam 600035 Chennai"
]

# Get the coordinates of Chennai
geolocator = Nominatim(user_agent='location')
location = geolocator.geocode("Chennai")
chennai_coordinates = (location.latitude, location.longitude)

# Create the map
map = folium.Map(location=chennai_coordinates, zoom_start=11)

# Add markers for each branch office
for office_address in branch_offices:
    office_location = geolocator.geocode(office_address)
    if office_location:
        folium.Marker(
            location=[office_location.latitude, office_location.longitude],
            popup=office_address
        ).add_to(map)

# Save the map as HTML
map.save("Branch_offices_map.html")
