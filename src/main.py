import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st
import inspect
import csv_cleaner
import graph
import trip
import sys
import csv

# Streamlit title and description
st.title("European Temperature Analysis Mapping")
st.write("This application analyzes temperature data across Europe and provides insights into average temperatures and thermal excursions. The program also includes a function that allows users to input a starting city A and a final city B, creating an itinerary by selecting the warmest city from a pool of three options until reaching the target city B.")

# We create the sidebar menu using streamlit
st.sidebar.title("Section")
section = st.sidebar.radio("Choose a Section", ("Global Temperature Trends", "Europe Map & Temperature", "Trip Calculator"))

# we load the CSV file called GlobalTemperatures, and we clean it
csv_path = 'data/GlobalTemperatures.csv'
data_cleaned = csv_cleaner.data_clean_global_temperatures(csv_path)

if section == "Global Temperature Trends":
    st.header("Global Temperature Trends")

    # Display Cleaned Data
    st.write("Global temperature data, these are the data that we use to create the two graphs")
    st.write(data_cleaned.head(100))

    # we want a graph to visualize better the change of temperatures
    data_cleaned['smoothedtemperature'] = data_cleaned['landaveragetemperature'].rolling(window = 12, center = True).mean()
    graph1 = graph.temperature_graph(data_cleaned, 'green', 'Average world temperature 1750/2015')

    st.write("We first filter the data, and after we call a function for create the plot: ")
    
    code1 = '''
    # main.py
    data_cleaned['smoothedtemperature'] = data_cleaned['landaveragetemperature'].rolling(window = 12, center = True).mean()
    graph1 = graph.temperature_graph(data_cleaned, 'green', 'Average world temperature 1750/2015')
    st.pyplot(graph1)

    # graph.py
    def temperature_graph(data_temperature_graph, color_graph, title_temperature):
        fig, ax = plt.subplots(figsize=(12, 7))
        ax.plot(data_temperature_graph['dt'], data_temperature_graph['smoothedtemperature'], label='Average temperature', color=color_graph)
        ax.set_title(title_temperature)
        ax.set_xlabel('Year')
        ax.set_ylabel('Temperature (°C)')
        ax.grid(True)

        return fig
        # plt.show()
    '''
    
    st.code(code1, language = 'python')
    st.pyplot(graph1)

    # we saw that the first data of the graph are not correct, probably. So we print only the data starting from 1840
    data_filtered = data_cleaned[(data_cleaned['dt'] >= '1840-01-01') & (data_cleaned['dt'] <= '2015-12-31')]
    data_filtered['smoothedtemperature'] = data_filtered['landaveragetemperature'].rolling(window = 12, center = True).mean()
    graph2 = graph.temperature_graph(data_filtered, 'red', 'Average world temperature 1840/2015')

    code2 = '''
    # main.py
    data_filtered = data_cleaned[(data_cleaned['dt'] >= '1840-01-01') & (data_cleaned['dt'] <= '2015-12-31')]
    data_filtered['smoothedtemperature'] = data_filtered['landaveragetemperature'].rolling(window = 12, center = True).mean()
    graph2 = graph.temperature_graph(data_filtered, 'red', 'Average world temperature 1840/2015')
    st.pyplot(graph2)
    '''
    st.write("In the first graph, we notice that the years before 1840 contain some inconsistent data and noise. Therefore, we remove these dates and display only the data from 1840 to 2010")
    st.code(code2, language = 'python')
    st.pyplot(graph2)

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
graph.plot_europe(europe, plot_type = 'temperature', state_branches = state_branches)

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
graph.plot_europe(europe, plot_type='outline', highest_cities = top_10_highest_excursion, lowest_cities = top_10_lowest_excursion)

cities_trip = trip.trip_calculator(europe_csv)

graph.plot_trip(europe, cities_trip, europe_csv)