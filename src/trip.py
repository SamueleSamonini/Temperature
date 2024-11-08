import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import sys
import csv

def trip_calculator(europe_csv):
    recent_temperature_df = europe_csv[europe_csv['dt'] >= '2005-01-01']
    europe_city = recent_temperature_df.groupby(['City', 'Latitude', 'Longitude'])['AverageTemperature'].mean().reset_index()

    print(europe_city)

    #from Lisbon to Kiev
    cities_already_visited = []
    city_deleted = set()
    
    def distance_calculation(current_cordinates, city_cordinates):
        distance = np.sqrt(
            (city_cordinates[:, 0] - current_cordinates[0]) ** 2 + (city_cordinates[:, 1] - current_cordinates[1])
        )

        return distance

    def trip_3_cities(europe_city, city_alredy_visited):
        current_city = cities_already_visited[-1]
        current_city_data = europe_city.query("City == @current_city")
        current_coordinates = np.array([current_city_data['Latitude'].values[0], current_city_data['Longitude'].values[0]])

        cities_not_visited = europe_city[europe_city['City'].isin(cities_already_visited + list(city_deleted)) == False]
        city_names = cities_not_visited['City'].values
        city_coordinates = cities_not_visited[['Latitude', 'Longitude']].values

        distances = distance_calculation(current_coordinates, city_coordinates)

        closest_3_cities = np.argmin(distances)

        closest_3_indices = np.argsort(distances)[:3]
        closest_3_cities = cities_not_visited.iloc[closest_3_indices]

        highest_temp_city = closest_3_cities.loc[closest_3_cities['AverageTemperature'].idxmax(), 'City']
        cities_already_visited.append(highest_temp_city)

        for city in closest_3_cities['City']:
            if city != highest_temp_city:
                city_deleted.add(city)

    start_city = input("Insert start city: ")
    while start_city not in europe_city['City'].values:
        print("The city is not present in the DF!!")
        start_city = input("Insert start city: ")

    cities_already_visited.append(start_city)

    final_city = input("Insert final city: ")
    while final_city not in europe_city['City'].values:
        print("The city is not present in the DF!!")
        start_city = input("Insert final city: ")

    while "Kiev" not in cities_already_visited:
        trip_3_cities(europe_city, cities_already_visited)

    print("Trip: ", cities_already_visited)
    print(len(cities_already_visited))
    print("Deleted: ", city_deleted)
    print(len(city_deleted))

    return cities_already_visited