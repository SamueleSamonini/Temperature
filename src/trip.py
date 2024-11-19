import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

def trip_calculator(europe_csv, start_city, final_city):
    recent_temperature_df = europe_csv[europe_csv['dt'] >= '2005-01-01']
    europe_city = recent_temperature_df.groupby(['City', 'Latitude', 'Longitude'])['AverageTemperature'].mean().reset_index()

    print("Initial DataFrame:", europe_city.head())

    cities_already_visited = []
    city_deleted = set()

    city_coords = europe_city[['Latitude', 'Longitude']].values

    def distance_calculation(current_coordinates, cities_not_visited):
        # Calculate distances from the current city to all other cities in cities_not_visited
        distances = np.sqrt(
            (cities_not_visited['Latitude'].values - current_coordinates[0]) ** 2 +
            (cities_not_visited['Longitude'].values - current_coordinates[1]) ** 2
        )
        
        # Get indices of the closest 3 cities
        closest_indices = np.argsort(distances)[:3]
        return cities_not_visited.iloc[closest_indices]['City'].tolist()


    def trip_3_cities(europe_city, cities_already_visited, final_city):
        current_city = cities_already_visited[-1]
        current_city_data = europe_city.query("City == @current_city")
        current_coordinates = np.array([current_city_data['Latitude'].values[0], current_city_data['Longitude'].values[0]])

        # Filter out cities that are already visited or deleted
        cities_not_visited = europe_city[~europe_city['City'].isin(cities_already_visited + list(city_deleted))]

        # Find the names of the 3 closest cities
        closest_3_cities_names = distance_calculation(current_coordinates, cities_not_visited)
        closest_3_cities = cities_not_visited[cities_not_visited['City'].isin(closest_3_cities_names)]

        # Check if final_city is among the closest cities
        if final_city in closest_3_cities['City'].values:
            # If final_city is in the closest 3 cities, prioritize and choose it
            print(f"Final city {final_city} found in closest cities. Prioritizing it.")
            cities_already_visited.append(final_city)
        else:
            # Otherwise, select the city with the highest temperature
            highest_temp_city = closest_3_cities.loc[closest_3_cities['AverageTemperature'].idxmax(), 'City']
            cities_already_visited.append(highest_temp_city)

            # Mark the other two cities as deleted so they are not reconsidered
            for city in closest_3_cities['City']:
                if city != highest_temp_city:
                    city_deleted.add(city)

    # start_city = input('Insert start city: ')
    # while start_city not in europe_city['City'].values:
    #     print("Error, the city is not present in the df!!")
    #     start_city = input('Insert start city: ')
    
    # final_city = input('Insert final city: ')
    # while final_city not in europe_city['City'].values:
    #     print("Error, the city is not present in the df!!")
    #     final_city = input('Insert start city: ')
        
    cities_already_visited.append(start_city)

    # Limit the number of iterations
    max_iterations = 500
    iteration = 0

    while final_city not in cities_already_visited and iteration < max_iterations:
        print(f"Iteration {iteration}: Currently at {cities_already_visited[-1]}")
        trip_3_cities(europe_city, cities_already_visited, final_city)
        iteration += 1

    if final_city in cities_already_visited:
        print(f"Reached {final_city}!")
    else:
        print(f"Reached the iteration limit without reaching {final_city}.")

    print("Trip:", cities_already_visited)
    print("Number of cities visited:", len(cities_already_visited))
    print("Deleted cities:", city_deleted)
    print("Number of cities deleted:", len(city_deleted))

    return cities_already_visited
