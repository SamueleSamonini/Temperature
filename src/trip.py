import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import KDTree

def trip_calculator(europe_csv):
    recent_temperature_df = europe_csv[europe_csv['dt'] >= '2005-01-01']
    europe_city = recent_temperature_df.groupby(['City', 'Latitude', 'Longitude'])['AverageTemperature'].mean().reset_index()

    print("Initial DataFrame:", europe_city.head())

    cities_already_visited = []
    city_deleted = set()

    city_coords = europe_city[['Latitude', 'Longitude']].values
    city_tree = KDTree(city_coords)

    city_coords_map = {city: (lat, lon) for city, lat, lon in zip(europe_city['City'], europe_city['Latitude'], europe_city['Longitude'])}

    def distance_calculation(current_coordinates, cities_not_visited):
        # Get the indices of the closest cities from the KDTree, then map back to the original DataFrame
        _, indices = city_tree.query([current_coordinates], k=len(europe_city))
        
        # Filter the indices to include only those cities in `cities_not_visited`
        valid_cities = []
        for index in indices[0]:
            city_name = europe_city.iloc[index]['City']
            if city_name in cities_not_visited['City'].values:
                valid_cities.append(city_name)
            if len(valid_cities) == 3:  # Only keep the closest 3 valid cities
                break
        return valid_cities

    def trip_3_cities(europe_city, cities_already_visited):
        current_city = cities_already_visited[-1]
        current_city_data = europe_city.query("City == @current_city")
        current_coordinates = np.array([current_city_data['Latitude'].values[0], current_city_data['Longitude'].values[0]])

        # Filter out cities that are already visited or deleted
        cities_not_visited = europe_city[~europe_city['City'].isin(cities_already_visited + list(city_deleted))]

        # Find the names of the 3 closest cities
        closest_3_cities_names = distance_calculation(current_coordinates, cities_not_visited)
        closest_3_cities = cities_not_visited[cities_not_visited['City'].isin(closest_3_cities_names)]

        # Select the city with the highest temperature among the closest 3 cities
        highest_temp_city = closest_3_cities.loc[closest_3_cities['AverageTemperature'].idxmax(), 'City']
        cities_already_visited.append(highest_temp_city)

        # Mark the other two cities as deleted so they are not reconsidered
        for city in closest_3_cities['City']:
            if city != highest_temp_city:
                city_deleted.add(city)

    start_city = 'Lisbon'
    final_city = 'Kiev'
    cities_already_visited.append(start_city)

    # Limit the number of iterations
    max_iterations = 500
    iteration = 0

    while final_city not in cities_already_visited and iteration < max_iterations:
        print(f"Iteration {iteration}: Currently at {cities_already_visited[-1]}")
        trip_3_cities(europe_city, cities_already_visited)
        iteration += 1

    if final_city in cities_already_visited:
        print("Reached Kiev!")
    else:
        print("Reached the iteration limit without reaching Kiev.")

    print("Trip:", cities_already_visited)
    print("Number of cities visited:", len(cities_already_visited))
    print("Deleted cities:", city_deleted)
    print("Number of cities deleted:", len(city_deleted))

    return cities_already_visited
