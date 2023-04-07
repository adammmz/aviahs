import folium

# Define the starting and ending airport codes
start = "LAX"
end = "JFK"

# Get the latitude and longitude of the airports
# You can use a library like geopy to do this
start_lat = 33.9416
start_lon = -118.4085
end_lat = 40.6413
end_lon = -73.7781

# Create a map centered on the United States
flight_map = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Draw the starting and ending airports as red circles
folium.CircleMarker(location=(start_lat, start_lon), radius=5, color='red', fill=True, fill_color='red', fill_opacity=0.6, popup=start).add_to(flight_map)
folium.CircleMarker(location=(end_lat, end_lon), radius=5, color='red', fill=True, fill_color='red', fill_opacity=0.6, popup=end).add_to(flight_map)


# Draw the flight path as a blue line
folium.PolyLine(locations=[[start_lat, start_lon], [end_lat, end_lon]], color='blue', weight=2, opacity=1).add_to(flight_map)

# Display the map
flight_map.save('output.html')
