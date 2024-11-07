import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import csv

def temperature_graph(data_temperature_graph, color_graph, title_temperature):
    """
    Plot graph
    
    Parameters:
    - data_temperature_graph: The data to print.
    - color_graph: The color of the graph.
    - title_temperature: the title of the graph.
    """
    plt.figure(figsize = (12, 6))
    plt.plot(data_temperature_graph['dt'], data_temperature_graph['smoothedtemperature'], label = 'Average temperature', color = color_graph)
    plt.title(title_temperature)
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.show()

def plot_europe(europe, plot_type = 'outline', state_branches = None, highest_cities = None, lowest_cities = None):
    """
    Plot a map of Europe with optional city points for highest and lowest thermal excursions.

    Parameters:
    - europe: The GeoDataFrame for Europe.
    - plot_type: The type of plot ('outline' or 'temperature').
    - state_branches: DataFrame with 'Country' and 'AverageTemperature' for the temperature map.
    - highest_cities: DataFrame of cities with the highest thermal excursions (plotted in red).
    - lowest_cities: DataFrame of cities with the lowest thermal excursions (plotted in blue).
    """
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
        for _, row in highest_cities.iterrows():
            ax.text(row['longitude'], row['latitude'] + 0.3, row['city'], fontsize=10, color='grey', fontweight='bold', ha='center')

    # Plot lowest excursion cities in blue with bold labels
    if lowest_cities is not None:
        ax.scatter(lowest_cities['longitude'], lowest_cities['latitude'], color='blue', s=50, label='Top 10 Lowest Excursion')
        for _, row in lowest_cities.iterrows():
            ax.text(row['longitude'], row['latitude'] + 0.3, row['city'], fontsize=10, color='grey', fontweight='bold', ha='center')
    
    ax.legend()

    # Set labels and aspect
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_aspect('auto')
    plt.show()