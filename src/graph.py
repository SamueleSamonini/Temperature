import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import streamlit as st
import altair as alt
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

    st.altair_chart(complete_temperature_chart, use_container_width=True)