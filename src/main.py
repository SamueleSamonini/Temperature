import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import csv_cleaner as csv_cleaner 
import sys
import csv

# first of all we load the CSV file called LobalTemperature
csv_path = 'data/GlobalTemperatures.csv'
data_cleaned = csv_cleaner.data_clean_global_temperatures(csv_path)

print(data_cleaned)

def temperature_graph(data_temperature_graph, color_graph, title):
    plt.figure(figsize = (12, 6))
    plt.plot(data_temperature_graph['dt'], data_temperature_graph['smoothedtemperature'], label = 'Average temperature', color = color_graph)
    plt.title('Average world temperature')
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.show()

# we want a graph to visualize better the change of temperatures
data_cleaned['smoothedtemperature'] = data_cleaned['landaveragetemperature'].rolling(window = 12, center = True).mean()
temperature_graph(data_cleaned, 'green', 'Average world temperature 1750/2015')

data_filtered = data_cleaned[(data_cleaned['dt'] >= '1840-01-01') & (data_cleaned['dt'] <= '2015-12-31')]
data_filtered['smoothedtemperature'] = data_filtered['landaveragetemperature'].rolling(window = 12, center = True).mean()
temperature_graph(data_filtered, 'red', 'Average world temperature 1840/2015')

world = gpd.read_file("map/ne_110m_admin_0_countries.shp")
world = world.explode(index_parts=False)
europe = world[(world['CONTINENT'] == 'Europe') & (world['SOVEREIGNT'] != 'Russia')]
europe = europe[(europe.geometry.centroid.y > 35) & (europe.geometry.centroid.y < 72) &
                (europe.geometry.centroid.x > -30) & (europe.geometry.centroid.x < 50)]

fig, ax = plt.subplots(figsize=(10, 7))
europe.plot(ax=ax, edgecolor='black')
ax.set_title('Europe')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_aspect('auto') 

plt.show()

# data_state_temperature = pd.read_csv('data/north_america_city.csv')

# state_branches = data_state_temperature.groupby('Country')['AverageTemperature'].mean().reset_index()
# north_america = north_america.merge(state_branches, left_on="SOVEREIGNT", right_on="Country", how="left")

# print(state_branches)

# fig, ax = plt.subplots(figsize=(12, 6))
# north_america.plot(column='AverageTemperature', cmap='coolwarm', legend=True, edgecolor='black', ax=ax)
# ax.set_title('North America - Average Temperature by Country')
# ax.set_xlabel('Longitude')
# ax.set_ylabel('Latitude')

# plt.show()