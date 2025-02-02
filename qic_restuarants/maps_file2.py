import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial as spatial
import folium 
from folium.plugins import MarkerCluster
from geopy.distance import geodesic

restaurants = pd.read_csv('restaurants.csv')
shelters = pd.read_csv('shelters.csv')

for index, row in shelters.iterrows():
    print(f"Row {index}:")
    print(row)
    print()  

# Ensure latitude and longitude columns are properly named and exist
shelter_lat_col, shelter_lon_col = 'latitude', 'longitude'
restaurant_lat_col, restaurant_lon_col = 'latitude', 'longitude'


print(shelters.columns)




# Function to find the top 3 closest restaurants
def find_top_3_restaurants(shelter):
    shelter_location = (shelter[shelter_lat_col], shelter[shelter_lon_col])
    restaurants['distance'] = restaurants.apply(
        lambda x: geodesic(shelter_location, (x[restaurant_lat_col], x[restaurant_lon_col])).kilometers, axis=1)
    top_3 = restaurants.nsmallest(3, 'distance')
    return top_3[['businessname','latitude', 'longitude', 'distance']].values.tolist()

# Check if the specific column names are in the DataFrame
if 'latitude' in shelters.columns and 'longitude' in shelters.columns:
    shelters['top_3_restaurants'] = shelters.apply(find_top_3_restaurants, axis=1)
else:
    print("One or both of the 'latitude' or 'longitude' columns are missing.")

# # Apply function to each shelter
#shelters['top_3_restaurants'] = shelters.apply(find_top_3_restaurants, axis=1)

# Save results
output_file = '/Users/druhibhargava/Downloads/qic_restuarants/top_3_restaurants.csv'
shelters.to_csv(output_file, index=False)

# print(f"Results saved to {output_file}")


'''
chain_restaurants = restaurants[restaurants['businessname'].str.contains(
    'Dunkin|McDonald|Burger King|Pizza Hut|Wendy|Panda Express|Eataly|Sweetgreen|Cava|Chipotle|California Pizza Kitchen|Shake Shack|Panera Bread|Subway|Five Guys|TGI Fridays|The Cheesecake Factory|Red Lobster|Olive Garden|Buffalo Wild Wings|Starbucks|Auntie Anne\'s|Nando\'s|Domino\'s|IHop|Applebee\'s|Cracker Barrel|Hooters|Arby\'s|KFC|Jack in the Box|Tim Hortons|Wingstop|Jimmy John\'s|Papa John\'s|Sonic|Zaxby\'s|Hardee\'s|Taco Bell|Whataburger|Moe\'s Southwest Grill|Bojangles|Denny\'s|Church\'s Chicken|Captain D\'s|Raising Cane\'s|Jersey Mike\'s|Steak \'n Shake|Cold Stone Creamery|Baskin-Robbins|Papa Murphy\'s|Lenny\'s Sub Shop|Wingstreet|Del Taco|Maggiano\'s Little Italy|Ted\'s Montana Grill|The Melting Pot|El Jefe\'s|Tatte', 
    case=False)]
short_chain_restaurants = chain_restaurants[['businessname', 'latitude', 'longitude']].dropna()
short_chain_restaurants = short_chain_restaurants[short_chain_restaurants['latitude'] > 40]

short_chain_restaurants.to_csv('short_chain_restaurants.csv', index=False)

plt.scatter(short_chain_restaurants['longitude'], short_chain_restaurants['latitude'])
plt.scatter(shelters['Longitude'], shelters['Latitude'], color = 'red')
plt.xlabel('Longitude')
plt.ylabel('Latitude')




# Create a folium map centered around the average latitude and longitude
m = folium.Map(location=[short_chain_restaurants['latitude'].mean(), short_chain_restaurants['longitude'].mean()], zoom_start=12)

# Add short chain restaurants to the map
for idx, row in short_chain_restaurants.iterrows():
    folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=5, color='blue', fill=True).add_to(m)

# Add shelters to the map
for idx, row in shelters.iterrows():
    folium.CircleMarker(location=[row['Latitude'], row['Longitude']], radius=5, color='red', fill=True).add_to(m)

# Save map as HTML file or display it
m.save('map.html')



# Convert restaurant and shelter DataFrames to coordinate arrays
restaurant_coords = short_chain_restaurants[['longitude', 'latitude']].values
shelter_coords = shelters[['Longitude', 'Latitude']].values

# Build a KDTree for shelters
shelter_tree = spatial.cKDTree(shelter_coords)

# Find the closest shelter for each restaurant
distances, indices = shelter_tree.query(restaurant_coords)


# Create a folium map centered around the mean of the restaurants' coordinates
map_center = [short_chain_restaurants['latitude'].mean(), short_chain_restaurants['longitude'].mean()]
folium_map = folium.Map(location=map_center, zoom_start=13)

# Add shelter markers to the map
shelter_cluster = MarkerCluster().add_to(folium_map)
for idx, shelter in shelters.iterrows():
    folium.Marker(
        location=[shelter['Latitude'], shelter['Longitude']],
        popup=f"Shelter {shelter.name}",
        icon=folium.Icon(color='red', icon='cloud')
    ).add_to(shelter_cluster)

# Add restaurant markers to the map
restaurant_cluster = MarkerCluster().add_to(folium_map)
for idx, restaurant in short_chain_restaurants.iterrows():
    folium.Marker(
        location=[restaurant['latitude'], restaurant['longitude']],
        popup=f"Restaurant {restaurant.name}",
        icon=folium.Icon(color='blue', icon='coffee')
    ).add_to(restaurant_cluster)

# Add lines from each restaurant to its closest shelter
for i in range(len(short_chain_restaurants)):  # Loop through restaurants
    # Get the closest shelter index
    closest_shelter_index = indices[i]
    closest_shelter = shelters.iloc[closest_shelter_index]
    
    # Add a line from restaurant to the closest shelter
    folium.PolyLine(
        locations=[
            [short_chain_restaurants.iloc[i]['latitude'], short_chain_restaurants.iloc[i]['longitude']],
            [closest_shelter['Latitude'], closest_shelter['Longitude']]
        ],
        color='blue',
        weight=2,
        opacity=0.6
    ).add_to(folium_map)

# Show the map
folium_map.save("restaurants_and_shelters_map.html")
folium_map
'''


