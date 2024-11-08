import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import csv_cleaner
import graph
import trip
import sys
import csv

# first of all we load the CSV file called GlobalTemperatures
csv_path = 'data/GlobalTemperatures.csv'
data_cleaned = csv_cleaner.data_clean_global_temperatures(csv_path)

print(data_cleaned)

# we want a graph to visualize better the change of temperatures
data_cleaned['smoothedtemperature'] = data_cleaned['landaveragetemperature'].rolling(window = 12, center = True).mean()
#graph.temperature_graph(data_cleaned, 'green', 'Average world temperature 1750/2015')

# we saw that the first data of the graph are not correct, probably. So we print only the data starting from 1840
data_filtered = data_cleaned[(data_cleaned['dt'] >= '1840-01-01') & (data_cleaned['dt'] <= '2015-12-31')]
data_filtered['smoothedtemperature'] = data_filtered['landaveragetemperature'].rolling(window = 12, center = True).mean()
#graph.temperature_graph(data_filtered, 'red', 'Average world temperature 1840/2015')

# load into the project the map of the world
world = gpd.read_file("map/ne_10m_admin_0_countries.shp") 
world = world.explode(index_parts=False)

# We filter the file for print only the europe, and we delete russia and other far land for a better visualization of the map
europe = world[(world['CONTINENT'] == 'Europe') & (world['SOVEREIGNT'] != 'Russia')]
europe = europe[(europe.geometry.centroid.y > 35) & (europe.geometry.centroid.y < 72) &
                (europe.geometry.centroid.x > -30) & (europe.geometry.centroid.x < 50)]

# # plot the europe
# graph.plot_europe(europe, plot_type = 'outline', city_te = city_te)

# plot the europe, coloring the country accordingly to average temperature
europe_csv = pd.read_csv('data/europe_city.csv')
state_branches = europe_csv.groupby('Country')['AverageTemperature'].mean().reset_index()
#graph.plot_europe(europe, plot_type = 'temperature', state_branches = state_branches)

# we must clean the cordinates, because it contains some char value like N for North
df = csv_cleaner.clean_coordinates(europe_csv, lat_col = 'Latitude', lon_col = 'Longitude')

# Now we want to find the 10 cities with the highest/lower thermal excursion
city_te = europe_csv.groupby(['City', 'Country', 'Latitude', 'Longitude'])['AverageTemperature'].agg(['max', 'min']).reset_index()
city_te['thermal_excursion'] = city_te['max'] - city_te['min']
city_te.columns = ['city', 'country', 'latitude', 'longitude', 'max_temp', 'min_temp', 'thermal_excursion']

top_10_highest_excursion = city_te.nlargest(10, 'thermal_excursion')
top_10_lowest_excursion = city_te.nsmallest(10, 'thermal_excursion')

print(top_10_highest_excursion)
print(top_10_lowest_excursion)

# plot the europe
#graph.plot_europe(europe, plot_type='outline', highest_cities = top_10_highest_excursion, lowest_cities = top_10_lowest_excursion)

cities_trip = trip.trip_calculator(europe_csv)

visited_cities = pd.DataFrame({
    'City': cities_trip,
    'Latitude': [europe_csv[europe_csv['City'] == city]['Latitude'].values[0] for city in cities_trip],
    'Longitude': [europe_csv[europe_csv['City'] == city]['Longitude'].values[0] for city in cities_trip]
})

gdf_visited = gpd.GeoDataFrame(
    visited_cities,
    geometry=gpd.points_from_xy(visited_cities['Longitude'], visited_cities['Latitude']),
    crs="EPSG:4326"
)

fig, ax = plt.subplots(figsize=(12, 7))
europe.plot(ax=ax, color='lightgrey', edgecolor='black')

gdf_visited.plot(ax=ax, color='blue', marker='o', markersize=50, label='Visited Cities')
plt.plot(gdf_visited['Longitude'], gdf_visited['Latitude'], color='red', linewidth=2, linestyle='-', label='Route')

plt.legend()
plt.title("Percorso delle Città Visitate da Lisbon a Kiev")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.show()