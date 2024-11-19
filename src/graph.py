import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

def plot_line_trend(data_cleaned):
    """
    Create an interactive trend line graph in streamlit

    Parameter: 
        data_cleaned -> A cleaned dataframe that contains all the temperature values during time.

    Return:
        complete_temperature_chart -> the interactive graph, with the graph showing the world's temperature over time and the line trend
    """
    # Smooth the 'landaveragetemperature' column using a 12-month rolling average, centered around each observation, to reduce noise and highlight trends.
    data_cleaned['smoothedtemperature'] = data_cleaned['landaveragetemperature'].rolling(window = 12, center = True).mean()

    # create a new pandas dataframe used for the chart datas
    chart_data = pd.DataFrame(
    {
        "Year": data_cleaned['dt'],
        "Temperature (°C)": data_cleaned['smoothedtemperature'],
    }
    )

    # the slider that choose the starting year of the graph
    start_year_chart = st.slider("Select Start Year", min_value=1750, max_value = chart_data['Year'].dt.year.max(), value = 1750)

    st.write(" ")

    # filter the data starting from the velue of the slider
    filtered_data = chart_data[chart_data['Year'].dt.year >= start_year_chart]

    # interactive line graph showing the world's temperature over time
    alt_chart_graph = alt.Chart(filtered_data).mark_line(color="#CD9077").encode(
        x = alt.X('Year:T', title='Year'), # create a x values that contain the year as a temporal variable
        y = alt.Y('Temperature (°C):Q', title = 'Temperature (°C)', scale = alt.Scale(domain=[6, 10])) # represent the temperature in celsius over the y, define the domain range
        ).properties(
        width = 700,
        height = 400
    )

    # trend line
    trend_line = alt.Chart(filtered_data).transform_regression(
        'Year', 'Temperature (°C)', method='linear' # did the lienar regression over year and temperature values
    ).mark_line(color="blue", opacity=0.7).encode( # visualize the line
        x = alt.X('Year:T'),
        y = alt.Y('Temperature (°C):Q')
    )

    # combine the graph and the trend line
    complete_temperature_chart = alt_chart_graph + trend_line

    return complete_temperature_chart

def europe_temperature_map(europe, geojson_data):
    """
    Create an interactive map of Europe's average temperature in Streamlit.
    
    Parameters:
        europe -> the GeoDataFrame containing geographic data and average temperatures for European countries.
        geojson_data -> the GeoJSON data corresponding to the GeoDataFrame for geographic visualization.

    Returns:
        complete_temperature_chart -> the interactive chart displaying the average temperature of European countries with a choropleth 
            map and a color scale for temperatures.
    """
    # Create the interactive map
    fig_interactive_map_temperature = px.choropleth_mapbox(
        europe,
        geojson = geojson_data,
        locations = europe.index,
        color = "AverageTemperature",
        hover_name = "SOVEREIGNT",  # Hover info can include country names
        color_continuous_scale = "temps",
        range_color = (2, 16),  # Adjust based on your data range
        mapbox_style = "carto-positron",
        center = {"lat": 50, "lon": 10},  # Adjust to focus on Europe
        zoom = 3,
        title = "Europe - Average Temperature by Country from 1740 to 2015",
        height = 600
    )

    # Configure the color bar (legend) position
    fig_interactive_map_temperature.update_layout(
        margin = dict (t = 30),
        coloraxis_colorbar = dict(
            orientation = "h",  # Set horizontal orientation for the legend
            y = -0.15,           # Position the legend below the map (adjust value to move lower or higher)
            x = 0.5,            # Center the color bar horizontally
            xanchor = "center", # Anchor the bar at its center
            title = "Avg Temperature (°C)"  # Label for the color bar
        )
    )

    return fig_interactive_map_temperature

def europe_thermal_excursion_map(europe, geojson_data, top_10_highest_excursion, top_10_lowest_excursion):
    """
    Create an interactive map of Europe's cities with the highest/lowest thermal excursion in Streamlit.
    
    Parameters:
        europe -> the GeoDataFrame containing geographic data and average temperatures for European countries.
        geojson_data -> the GeoJSON data corresponding to the GeoDataFrame for geographic visualization.
        top_10_highest_excursion -> A df containing the 10 cities with the highest thermal excursion
        top_10_lowest_excursion -> A df containing the 10 cities with the lowest thermal excursion

    Returns:
        fig_interactive_map_thermal_excursion -> the interactive chart displaying, inside the map of europe, the 10 cities with the highest
        thermal excursion in red, and the 10 cities with the lowest thermal excursion in blue
    """
    # show the interactive map of europe
    fig_interactive_map_thermal_excursion = px.choropleth_mapbox(
        europe,
        geojson = geojson_data,
        #locations = europe.index,
        mapbox_style = "carto-positron",
        center = {"lat": 50, "lon": 10},  # Adjust to focus on Europe
        zoom = 3,
        title = "Europe - ten cities with the highest and lowest thermal excursion",
        height = 600
    )

    # Add scatter layer for the 10 cities with the highest thermal excursion with red markers
    fig_interactive_map_thermal_excursion.add_trace(go.Scattermapbox(
        lat = top_10_highest_excursion['latitude'],
        lon = top_10_highest_excursion['longitude'],
        mode = 'markers',
        name = "Highest Thermal Excursions",
        marker = dict(size=10, color='red'),
        text = top_10_highest_excursion.apply(lambda row: f"{row['city']}, {row['country']}<br>Thermal Excursion: {row['thermal_excursion']}°C", axis=1),
        hoverinfo = 'text'
    ))

    # Add scatter layer for the 10 cities with the lowest thermal excursion with blue markers
    fig_interactive_map_thermal_excursion.add_trace(go.Scattermapbox(
        lat = top_10_lowest_excursion['latitude'],
        lon = top_10_lowest_excursion['longitude'],
        mode = 'markers',
        name = "Lowest Thermal Excursions",
        marker = dict(size=10, color='blue'),
        text = top_10_lowest_excursion.apply(lambda row: f"{row['city']}, {row['country']}<br>Thermal Excursion: {row['thermal_excursion']}°C", axis=1),
        hoverinfo = 'text'
    ))

    # Position the legend below the map
    fig_interactive_map_thermal_excursion.update_layout(
        margin = dict (t = 30),
        legend = dict(
            orientation = "h",  # Horizontal orientation
            yanchor = "bottom",
            y = -0.1,  # Position below the map
            xanchor = "center",
            x = 0.5
        )
    )

    return fig_interactive_map_thermal_excursion

def plot_trip_map(europe_csv, cities_trip):
    """
    Create an interactive map to visualize a trip path through selected cities in Europe.

    Parameters:
        europe_csv -> the DataFrame containing city data including names, coordinates, and other attributes.
        cities_trip -> a list of city names in the order of the trip, defining the travel path.

    Returns:
        fig -> an interactive map displaying the trip path with markers for cities and lines connecting them in the order of visit.
    """

    # Ensure cities are in the order of visit for plotting
    # This selects only the rows in europe_csv corresponding to the cities in cities_trip and resets the index to maintain consistency.
    trip_coords = europe_csv.set_index('City').loc[cities_trip].reset_index()

    # Create an empty Plotly map figure for customization
    # go.Figure() initializes an empty interactive figure object to which we can add data and customize.
    fig = go.Figure()

    # Add a scatter mapbox trace for the trip path
    # Scattermapbox is used to plot points (markers) and connect them with lines.
    fig.add_trace(go.Scattermapbox(
        lat = trip_coords['Latitude'], # Latitude coordinates for the cities in the trip
        lon = trip_coords['Longitude'], # Longitude coordinates for the cities in the trip
        mode = 'markers+lines', # Plot both markers and lines connecting the markers
        marker = dict(size=10, color="red"),
        line = dict(width=2, color="blue"),
        text = trip_coords['City'], # Add city names as hover information
        hoverinfo = "text" # Display city names when hovering over points
    ))

    # Set map layout
    fig.update_layout(
        mapbox = dict(
            style = "carto-positron",
            center = dict(lat=50, lon=10),  # Center over Europe
            zoom = 3
        ),
        showlegend = False, # Disable the legend (not needed for this map)
        height = 700,
        title = "Interactive Trip Path"
    )

    return fig