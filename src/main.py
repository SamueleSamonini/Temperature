import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt
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

# load into the project the map of the world
world = gpd.read_file("map/ne_10m_admin_0_countries.shp") 
world = world.explode(index_parts=False)

# We filter the file for print only the europe, and we delete russia and other far land for a better visualization of the map
europe = world[(world['CONTINENT'] == 'Europe') & (world['SOVEREIGNT'] != 'Russia')]
europe = europe[(europe.geometry.centroid.y > 35) & (europe.geometry.centroid.y < 72) &
                (europe.geometry.centroid.x > -30) & (europe.geometry.centroid.x < 50)]

europe_csv = pd.read_csv('data/europe_city.csv')

# we must clean the cordinates, because it contains some char value like N for North
europe_csv = csv_cleaner.clean_coordinates(europe_csv, lat_col = 'Latitude', lon_col = 'Longitude')

if section == "Global Temperature Trends":
    st.header("Global Temperature Trends", divider = "gray")

    # Display Cleaned Data
    st.write("Global temperature data, these are the data that we use to create the two graphs")
    st.dataframe(data_cleaned.head(100), use_container_width = True)

    # we want a graph to visualize better the change of temperatures
    data_cleaned['smoothedtemperature'] = data_cleaned['landaveragetemperature'].rolling(window = 12, center = True).mean()
    data_cleaned.set_index(data_cleaned['dt'], inplace=True)
    
    # graph1 = graph.temperature_graph(data_cleaned, 'green', 'Average world temperature 1750/2015')

    st.divider()
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

    chart_data = pd.DataFrame(
    {
        "Year": data_cleaned['dt'],
        "Temperature (°C)": data_cleaned['smoothedtemperature'],
    }
    )

    start_year_chart = st.slider("Select Start Year", min_value=1750, max_value=chart_data['Year'].dt.year.max(), value=1750)
    st.write(" ")

    filtered_data = chart_data[chart_data['Year'].dt.year >= start_year_chart]

    alt_chart_graph = alt.Chart(filtered_data).mark_line(color="#CD9077").encode(
        x = alt.X('Year:T', title='Year'),
        y = alt.Y('Temperature (°C):Q', title = 'Temperature (°C)', scale = alt.Scale(domain=[6, 10]))
        ).properties(
        width=700,
        height=400
    )
    
    st.altair_chart(alt_chart_graph, use_container_width=True)
    st.code(code1, language = 'python')
    # st.pyplot(graph1)

    # we saw that the first data of the graph are not correct, probably. So we print only the data starting from 1840
    # data_filtered = data_cleaned[(data_cleaned['dt'] >= '1840-01-01') & (data_cleaned['dt'] <= '2015-12-31')]
    # data_filtered['smoothedtemperature'] = data_filtered['landaveragetemperature'].rolling(window = 12, center = True).mean()
    # graph2 = graph.temperature_graph(data_filtered, 'red', 'Average world temperature 1840/2015')

    code2 = '''
    # main.py
    data_filtered = data_cleaned[(data_cleaned['dt'] >= '1840-01-01') & (data_cleaned['dt'] <= '2015-12-31')]
    data_filtered['smoothedtemperature'] = data_filtered['landaveragetemperature'].rolling(window = 12, center = True).mean()
    graph2 = graph.temperature_graph(data_filtered, 'red', 'Average world temperature 1840/2015')
    st.pyplot(graph2)
    '''

    st.write("In the first graph, we notice that the years before 1840 contain some inconsistent data and noise. Therefore, we remove these dates and display only the data from 1840 to 2010")
    st.code(code2, language = 'python')
    #st.pyplot(graph2)
elif section == "Europe Map & Temperature":
    st.header("Europe Map & Temperature")
    # plot the europe
    # graph.plot_europe(europe, plot_type = 'outline', city_te = city_te)

    # plot the europe, coloring the country accordingly to average temperature
    state_branches = europe_csv.groupby('Country')['AverageTemperature'].mean().reset_index()
    graph3 = graph.plot_europe(europe, plot_type = 'temperature', state_branches = state_branches)

    code3 = '''
    # main.py
    state_branches = europe_csv.groupby('Country')['AverageTemperature'].mean().reset_index()
    graph3 = graph.plot_europe(europe, plot_type = 'temperature', state_branches = state_branches)

    # graph.py
    def plot_europe(europe, plot_type = 'outline', state_branches = None, highest_cities = None, lowest_cities = None):
        fig, ax = plt.subplots(figsize=(12, 7))

        if plot_type == 'outline':
            # Plot just the outline of Europe
            europe.plot(ax=ax, color = 'white', edgecolor = 'black')
            ax.set_title('Europe')
        elif plot_type == 'temperature' and state_branches is not None:
            # Merge temperature data with Europe GeoDataFrame
            europe = europe.merge(state_branches, left_on="SOVEREIGNT", right_on="Country", how="left")
            
            # Plot average temperature by country
            europe.plot(column='AverageTemperature', cmap='coolwarm', legend=True, edgecolor='black', ax=ax)
            ax.set_title('Europe - Average Temperature by Country from 1740 to 2015')

        # Plot highest excursion cities in red with bold labels
        if highest_cities is not None:
            ax.scatter(highest_cities['longitude'], highest_cities['latitude'], color='red', s=50, label='Top 10 Highest Excursion')
            
        # Plot lowest excursion cities in blue with bold labels
        if lowest_cities is not None:
            ax.scatter(lowest_cities['longitude'], lowest_cities['latitude'], color='blue', s=50, label='Top 10 Lowest Excursion')
            
        ax.legend()

        # Set labels and aspect
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_aspect('auto')

        return fig
    '''

    st.write("europe_csv.csv")
    st.dataframe(europe_csv.head(100), use_container_width=True)
    st.write("state_branches")
    st.dataframe(state_branches, use_container_width=True)
    st.write("Now, using the data contained in europe_city.csv, we will analyze all temperature data, calculate an average for each country, and visualize the results on a map.")
    st.code(code3, language = 'python')
    st.write("Europe Temperature Map")
    st.pyplot(graph3)

    # Now we want to find the 10 cities with the highest/lower thermal excursion
    city_te = europe_csv.groupby(['City', 'Country', 'Latitude', 'Longitude'])['AverageTemperature'].agg(['max', 'min']).reset_index()
    city_te['thermal_excursion'] = city_te['max'] - city_te['min']
    city_te.columns = ['city', 'country', 'latitude', 'longitude', 'max_temp', 'min_temp', 'thermal_excursion']

    top_10_highest_excursion = city_te.nlargest(10, 'thermal_excursion')
    top_10_lowest_excursion = city_te.nsmallest(10, 'thermal_excursion')

    # plot the europe
    graph4 = graph.plot_europe(europe, plot_type = 'outline', highest_cities = top_10_highest_excursion, lowest_cities = top_10_lowest_excursion)
    
    code4 = '''
    city_te = europe_csv.groupby(['City', 'Country', 'Latitude', 'Longitude'])['AverageTemperature'].agg(['max', 'min']).reset_index()
    city_te['thermal_excursion'] = city_te['max'] - city_te['min']
    city_te.columns = ['city', 'country', 'latitude', 'longitude', 'max_temp', 'min_temp', 'thermal_excursion']

    top_10_highest_excursion = city_te.nlargest(10, 'thermal_excursion')
    top_10_lowest_excursion = city_te.nsmallest(10, 'thermal_excursion')

    graph4 = graph.plot_europe(europe, plot_type = 'outline', highest_cities = top_10_highest_excursion, lowest_cities = top_10_lowest_excursion)
    '''

    st.code(code4, language = 'python')

    st.write("Top 10 Cities with Highest Thermal Excursion")
    st.dataframe(top_10_highest_excursion, use_container_width=True)
    
    st.write("Top 10 Cities with lowest Thermal Excursion")
    st.dataframe(top_10_lowest_excursion, use_container_width=True)

    st.pyplot(graph4)
elif section == "Trip Calculator":
    st.header("Trip Calculator Based on Temperature")

    start_city = st.text_input("Insert Start City:", "")
    final_city = st.text_input("Insert Final City:", "")

    if start_city and final_city:
        if start_city in europe_csv['City'].values and final_city in europe_csv['City'].values:
            cities_trip = trip.trip_calculator(europe_csv, start_city, final_city)
            st.write(cities_trip)
        else:
            st.write("One or both cities are not present in the dataset. Please enter valid city names.")
    else:
        st.info("Please enter both a start city and a final city to calculate the trip.")

    graph5 = graph.plot_trip(europe, cities_trip, europe_csv)
    st.pyplot(graph5)