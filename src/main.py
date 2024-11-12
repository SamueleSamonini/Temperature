import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt
import plotly.express as px
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

europe['SOVEREIGNT'] = europe['SOVEREIGNT'].replace({
    "Czechia": "Czech Republic",
    "Republic of Serbia": "Serbia"
})

europe_csv = pd.read_csv('data/europe_city.csv')

# we must clean the cordinates, because it contains some char value like N for North
europe_csv = csv_cleaner.clean_coordinates(europe_csv, lat_col = 'Latitude', lon_col = 'Longitude')

if section == "Global Temperature Trends":
    st.header("Global Temperature Trends", divider = "gray")

    # Display Cleaned Data
    st.write("Global temperature data, these are the data that we use to create the two graphs")
    st.dataframe(data_cleaned.head(100), use_container_width = True)

    # old version without streamlit
    # we want a graph to visualize better the change of temperatures
    # data_cleaned['smoothedtemperature'] = data_cleaned['landaveragetemperature'].rolling(window = 12, center = True).mean()
    # data_cleaned.set_index(data_cleaned['dt'], inplace=True)
    # graph1 = graph.temperature_graph(data_cleaned, 'green', 'Average world temperature 1750/2015')

    st.divider()
    st.write("We first filter the data, and after we call a function for create the plot: ")

    chart_data = pd.DataFrame(
    {
        "Year": data_cleaned['dt'],
        "Temperature (°C)": data_cleaned['smoothedtemperature'],
    }
    )

    start_year_chart = st.slider("Select Start Year", min_value=1750, max_value=chart_data['Year'].dt.year.max(), value=1750)
    st.write(" ")

    filtered_data = chart_data[chart_data['Year'].dt.year >= start_year_chart]

    # temperature graph
    alt_chart_graph = alt.Chart(filtered_data).mark_line(color="#CD9077").encode(
        x = alt.X('Year:T', title='Year'),
        y = alt.Y('Temperature (°C):Q', title = 'Temperature (°C)', scale = alt.Scale(domain=[6, 10]))
        ).properties(
        width=700,
        height=400
    )

    # trend line
    trend_line = alt.Chart(filtered_data).transform_regression(
        'Year', 'Temperature (°C)', method='linear'
    ).mark_line(color="blue", opacity=0.7).encode(
        x = alt.X('Year:T'),
        y = alt.Y('Temperature (°C):Q')
    )

    complete_temperature_chart = alt_chart_graph + trend_line
    
    st.altair_chart(complete_temperature_chart, use_container_width=True)

    # old version without streamlit
    # we saw that the first data of the graph are not correct, probably. So we print only the data starting from 1840
    # data_filtered = data_cleaned[(data_cleaned['dt'] >= '1840-01-01') & (data_cleaned['dt'] <= '2015-12-31')]
    # data_filtered['smoothedtemperature'] = data_filtered['landaveragetemperature'].rolling(window = 12, center = True).mean()
    # graph2 = graph.temperature_graph(data_filtered, 'red', 'Average world temperature 1840/2015')

    st.write("""
        - In the first part, we notice that the years before 1840 contain some inconsistent data and noise. Therefore, we remove these dates and display only the data from 1840 to 2010.
        - Starting from the year 1975, we observe a significant change in temperature, where the effects of global warming become evident.
    """)

elif section == "Europe Map & Temperature":
    st.header("Europe Map & Temperature")
    # plot the europe
    # graph.plot_europe(europe, plot_type = 'outline', city_te = city_te)

    # plot the europe, coloring the country accordingly to average temperature
    state_branches = europe_csv.groupby('Country')['AverageTemperature'].mean().reset_index()
    countries_in_europe = europe.groupby('SOVEREIGNT')

    # old version without streamlit
    # graph3 = graph.plot_europe(europe, plot_type = 'temperature', state_branches = state_branches)

    st.write("europe_csv.csv")
    st.dataframe(europe_csv.head(100), use_container_width=True)
    st.write("state_branches")
    st.dataframe(state_branches, use_container_width=True)
    st.write("europe")
    st.dataframe(countries_in_europe)
    st.write("Now, using the data contained in europe_city.csv, we will analyze all temperature data, calculate an average for each country, and visualize the results on a map.")

    europe = europe.merge(state_branches, left_on="SOVEREIGNT", right_on="Country", how="left")
    europe = europe.to_crs(epsg=4326)
    
    geojson_data = europe.__geo_interface__

    # Create the interactive map
    fig_interactive_map = px.choropleth_mapbox(
        europe,
        geojson = geojson_data,
        locations = europe.index,
        color = "AverageTemperature",
        hover_name = "SOVEREIGNT",  # Hover info can include country names
        color_continuous_scale = "temps",
        range_color = (2, 16),  # Adjust based on your data range
        mapbox_style = "carto-positron",
        center = {"lat": 50, "lon": 10},  # Adjust to focus on Europe
        zoom = 2,
        title = "Europe - Average Temperature by Country from 1740 to 2015"
    )

    # Configure the color bar (legend) position
    fig_interactive_map.update_layout(
        coloraxis_colorbar=dict(
            orientation = "h",  # Set horizontal orientation for the legend
            y = -0.2,           # Position the legend below the map (adjust value to move lower or higher)
            x = 0.5,            # Center the color bar horizontally
            xanchor = "center", # Anchor the bar at its center
            title = "Avg Temperature (°C)"  # Label for the color bar
        )
    )

    st.plotly_chart(fig_interactive_map)

    # Now we want to find the 10 cities with the highest/lower thermal excursion
    city_te = europe_csv.groupby(['City', 'Country', 'Latitude', 'Longitude'])['AverageTemperature'].agg(['max', 'min']).reset_index()
    city_te['thermal_excursion'] = city_te['max'] - city_te['min']
    city_te.columns = ['city', 'country', 'latitude', 'longitude', 'max_temp', 'min_temp', 'thermal_excursion']

    top_10_highest_excursion = city_te.nlargest(10, 'thermal_excursion')
    top_10_lowest_excursion = city_te.nsmallest(10, 'thermal_excursion')

    # plot the europe
    graph4 = graph.plot_europe(europe, plot_type = 'outline', highest_cities = top_10_highest_excursion, lowest_cities = top_10_lowest_excursion)

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