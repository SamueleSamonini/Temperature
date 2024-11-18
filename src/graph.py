import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import csv

def plot_line_trend(data_cleaned):
    data_cleaned['smoothedtemperature'] = data_cleaned['landaveragetemperature'].rolling(window = 12, center = True).mean()

    chart_data = pd.DataFrame(
    {
        "Year": data_cleaned['dt'],
        "Temperature (°C)": data_cleaned['smoothedtemperature'],
    }
    )

    start_year_chart = st.slider("Select Start Year", min_value=1750, max_value = chart_data['Year'].dt.year.max(), value = 1750)

    st.write(" ")

    filtered_data = chart_data[chart_data['Year'].dt.year >= start_year_chart]

    # interactive line graph showing the world's temperature over time
    alt_chart_graph = alt.Chart(filtered_data).mark_line(color="#CD9077").encode(
        x = alt.X('Year:T', title='Year'),
        y = alt.Y('Temperature (°C):Q', title = 'Temperature (°C)', scale = alt.Scale(domain=[6, 10]))
        ).properties(
        width = 700,
        height = 400
    )

    # trend line
    trend_line = alt.Chart(filtered_data).transform_regression(
        'Year', 'Temperature (°C)', method='linear'
    ).mark_line(color="blue", opacity=0.7).encode(
        x = alt.X('Year:T'),
        y = alt.Y('Temperature (°C):Q')
    )

    complete_temperature_chart = alt_chart_graph + trend_line

    return complete_temperature_chart

def europe_temperature_map(europe, geojson_data):
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

    # Add scatter layer for top 10 cities with red markers
    fig_interactive_map_thermal_excursion.add_trace(go.Scattermapbox(
        lat=top_10_highest_excursion['latitude'],
        lon=top_10_highest_excursion['longitude'],
        mode='markers',
        name = "Highest Thermal Excursions",
        marker=dict(size=10, color='red'),
        text=top_10_highest_excursion.apply(lambda row: f"{row['city']}, {row['country']}<br>Thermal Excursion: {row['thermal_excursion']}°C", axis=1),
        hoverinfo='text'
    ))

    # Add scatter layer for worst 10 cities with blue markers
    fig_interactive_map_thermal_excursion.add_trace(go.Scattermapbox(
        lat=top_10_lowest_excursion['latitude'],
        lon=top_10_lowest_excursion['longitude'],
        mode='markers',
        name = "Lowest Thermal Excursions",
        marker=dict(size=10, color='blue'),
        text=top_10_lowest_excursion.apply(lambda row: f"{row['city']}, {row['country']}<br>Thermal Excursion: {row['thermal_excursion']}°C", axis=1),
        hoverinfo='text'
    ))

    # Position the legend below the map
    fig_interactive_map_thermal_excursion.update_layout(
        margin = dict (t = 30),
        legend=dict(
            orientation="h",  # Horizontal orientation
            yanchor="bottom",
            y=-0.1,  # Position below the map
            xanchor="center",
            x=0.5
        )
    )

    return fig_interactive_map_thermal_excursion