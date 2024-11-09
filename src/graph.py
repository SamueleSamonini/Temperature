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
        
    # Plot lowest excursion cities in blue with bold labels
    if lowest_cities is not None:
        ax.scatter(lowest_cities['longitude'], lowest_cities['latitude'], color='blue', s=50, label='Top 10 Lowest Excursion')
        
    ax.legend()

    # Set labels and aspect
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_aspect('auto')
    plt.show()

def plot_path(europe, europe_city, path):
    fig, ax = plt.subplots(figsize=(15, 10))
    europe.plot(ax=ax, color='lightgrey')

    path_coords = europe_city[europe_city['City'].isin(path)]
    ax.plot(path_coords['Longitude'], path_coords['Latitude'], color='red', linewidth=2)
    ax.scatter(path_coords['Longitude'], path_coords['Latitude'], color='blue', s=50)

    for idx, row in path_coords.iterrows():
        ax.annotate(row['City'], xy=(row['Longitude'], row['Latitude']), xytext=(3, 3), textcoords="offset points")
    
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Path of Cities Visited from Lisbon to Kiev")
    plt.show()

def plot_trip(europe, cities_trip, europe_csv):
    visited_cities = pd.DataFrame({
        'City': cities_trip,
        'Latitude': [europe_csv[europe_csv['City'] == city]['Latitude'].values[0] for city in cities_trip],
        'Longitude': [europe_csv[europe_csv['City'] == city]['Longitude'].values[0] for city in cities_trip]
    })
    
    gdf_visited = gpd.GeoDataFrame(
        visited_cities,
        geometry = gpd.points_from_xy(visited_cities['Longitude'], visited_cities['Latitude']),
        crs="EPSG:4326"
    )

    fig, ax = plt.subplots(figsize=(12, 7))
    europe.plot(ax=ax, color='lightgrey', edgecolor='black')

    gdf_visited.plot(ax=ax, color='blue', marker='o', markersize=50, label='Visited Cities')
    plt.plot(gdf_visited['Longitude'], gdf_visited['Latitude'], color='red', linewidth=2, linestyle='-', label='Route')

    plt.legend()
    plt.title("Percorso")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    plt.show()