import pandas as pd
import geopandas as gpd
import streamlit as st
from src import csv_cleaner, graph, trip

# Streamlit title and description
st.title("European Temperature Analysis")

# We create the sidebar menu using streamlit
st.sidebar.title("Section")
section = st.sidebar.radio("Choose a Section", ("Global Temperature Trends", "Europe Temperature Map", "Trip Calculator"))

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

europe['SOVEREIGNT'] = europe['SOVEREIGNT'].replace({
    "Czechia": "Czech Republic",
    "Republic of Serbia": "Serbia"
})

europe_csv = pd.read_csv('data/europe_city.csv')

# we must clean the cordinates, because it contains some char value like N for North
europe_csv = csv_cleaner.clean_coordinates(europe_csv, lat_col = 'Latitude', lon_col = 'Longitude')

if section == "Global Temperature Trends":
    st.header("Global Temperature Trends", divider = "gray")

    st.markdown("""
        <div style='text-align: justify;'>
            <b> In this section of the app, we use a dataframe containing global temperature data for each month from 1740 to 2015, which we visualize in an interactive graph. </b>
        </div> <br>
        """,
        unsafe_allow_html = True
    )

    # Display Cleaned Data
    st.write('These are the global temperature data that we use to create the graph below.')
    st.dataframe(data_cleaned.head(100), use_container_width = True)

    st.divider()
    st.write("We first clena the data, and after we call a function for create the plot: ")

    complete_temperature_chart = graph.plot_line_trend(data_cleaned)

    st.altair_chart(complete_temperature_chart, use_container_width=True)

    # we use HTML and CSS to justify and display using bullet poin the data
    st.markdown("""
        <div style='text-align: justify;'>
            <ul>
                <li> In the first part, we notice that the years before 1840 contain some inconsistent data and noise. Therefore, using the slider, you can remove these dates and display only the data from 1840 to 2010. </li>
                <li> Starting from the year 1975, we observe a significant change in temperature, where the effects of global warming become evident. </li>
            </ul>
        </div>
        """,
        unsafe_allow_html = True
    )

elif section == "Europe Temperature Map":
    st.header("Europe Temperature Map", divider = "gray")
    st.markdown("""
        <div style='text-align: justify;'>
            <b> In this section of the app, we use a GeoPandas world map and merge it with a dataframe containing extensive temperature data for cities and countries. We then display two interactive maps of Europe: the first shows the average temperature for each country, and the second highlights the 10 cities with the highest and lowest thermal excursions. </b>
        </div> <br>
        """,
        unsafe_allow_html = True
    )

    # plot the europe, coloring the country accordingly to average temperature
    state_branches = europe_csv.groupby('Country')['AverageTemperature'].mean().reset_index()
    countries_in_europe = europe.groupby('SOVEREIGNT')

    st.write("Using the data in our dataframe, we will analyze all temperature records and calculate an average for each country. These are the results:")
    st.dataframe(state_branches, use_container_width=True)
    st.write("Now, we display the data on an interactive map:")

    europe = europe.merge(state_branches, left_on="SOVEREIGNT", right_on="Country", how="left")
    europe = europe.to_crs(epsg=4326)
    geojson_data = europe.__geo_interface__

    fig_interactive_map_temperature = graph.europe_temperature_map(europe, geojson_data)

    st.plotly_chart(fig_interactive_map_temperature)

    # Now we want to find the 10 cities with the highest/lower thermal excursion
    city_te = europe_csv.groupby(['City', 'Country', 'Latitude', 'Longitude'])['AverageTemperature'].agg(['max', 'min']).reset_index()
    city_te['thermal_excursion'] = city_te['max'] - city_te['min']
    city_te.columns = ['city', 'country', 'latitude', 'longitude', 'max_temp', 'min_temp', 'thermal_excursion']

    top_10_highest_excursion = city_te.nlargest(10, 'thermal_excursion')
    top_10_lowest_excursion = city_te.nsmallest(10, 'thermal_excursion')

    st.markdown('''
        <div style='text-align: justify;'>
            In this phase, we calculate the minimum and maximum temperatures for each city, then determine the thermal excursion. Here are the results for the 10 cities with the highest thermal excursion:
        <div> <br>''',
        unsafe_allow_html = True
    )
    st.dataframe(top_10_highest_excursion, use_container_width=True)
    
    st.write("And the 10 cities with the lowest thermal excursion:")
    st.dataframe(top_10_lowest_excursion, use_container_width=True)

    st.write("Now, we display the data on an interactive map:")
    fig_interactive_map_thermal_excursion = graph.europe_thermal_excursion_map(europe, geojson_data, top_10_highest_excursion, top_10_lowest_excursion)
    st.plotly_chart(fig_interactive_map_thermal_excursion)
    
elif section == "Trip Calculator":
    st.header("Trip Calculator Based on Temperature", divider = 'gray')

    st.markdown("""
        <div style='text-align: justify;'>
            <b> In this section of the app, we analyze temperature data to calculate a customized travel route across Europe based on user-selected cities.
            Users can select a start city and a final city, and the app calculates a route that prioritizes the warmest nearby cities while avoiding revisits. 
            This is achieved through distance calculations and temperature comparisons across selected cities. 
            Additionally, an interactive map is generated to visually display the calculated route, with markers showing each visited city along the way.</b>
        </div> <br>
        """,
        unsafe_allow_html = True
    )

    unique_cities_for_trip = europe_csv['City'].unique()
    reversed_cities_for_trip = unique_cities_for_trip[::-1]

    start_city = st.selectbox(
        "Select the start city: ",
        unique_cities_for_trip,
        key = "start_city_selectbox", # we need to put a key because streamlit give us an error if we don't put it
        placeholder = "No city selected"
    )

    final_city = st.selectbox(
        "Select the start city: ",
        reversed_cities_for_trip,
        key = "final_city_selectbox",
        placeholder = "No city selected"
    )

    if start_city and final_city:
        cities_trip = trip.trip_calculator(europe_csv, start_city, final_city)
        st.write("Cities visited", cities_trip)

        fig = graph.plot_trip_map(europe_csv, cities_trip)
        # Display the interactive map in Streamlit
        st.plotly_chart(fig)
        
    else:
        st.info("Please enter both a start city and a final city to calculate the trip.")