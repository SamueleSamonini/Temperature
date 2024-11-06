import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import csv_cleaner
import graph
import sys
import csv

# first of all we load the CSV file called GlobalTemperatures
csv_path = 'data/GlobalTemperatures.csv'
data_cleaned = csv_cleaner.data_clean_global_temperatures(csv_path)

print(data_cleaned)

# we want a graph to visualize better the change of temperatures
data_cleaned['smoothedtemperature'] = data_cleaned['landaveragetemperature'].rolling(window = 12, center = True).mean()
graph.temperature_graph(data_cleaned, 'green', 'Average world temperature 1750/2015')

# we saw that the first data of the graph are not correct, probably. So we print only the data starting from 1840
data_filtered = data_cleaned[(data_cleaned['dt'] >= '1840-01-01') & (data_cleaned['dt'] <= '2015-12-31')]
data_filtered['smoothedtemperature'] = data_filtered['landaveragetemperature'].rolling(window = 12, center = True).mean()
graph.temperature_graph(data_filtered, 'red', 'Average world temperature 1840/2015')

# load into the project the map of the world
world = gpd.read_file("map/ne_10m_admin_0_countries.shp") 
world = world.explode(index_parts=False)

# We filter the file for print only the europe, and we delete russia and other far land for a better visualization of the map
europe = world[(world['CONTINENT'] == 'Europe') & (world['SOVEREIGNT'] != 'Russia')] 
europe = europe[(europe.geometry.centroid.y > 35) & (europe.geometry.centroid.y < 72) &
                (europe.geometry.centroid.x > -30) & (europe.geometry.centroid.x < 50)]

# plot the europe
graph.plot_europe(europe, plot_type = 'outline')

# plot the europe, coloring the country accordingly to average temperature
data_state_temperature = pd.read_csv('data/europe_city.csv')
state_branches = data_state_temperature.groupby('Country')['AverageTemperature'].mean().reset_index()
graph.plot_europe(europe, plot_type = 'temperature', state_branches = state_branches)

