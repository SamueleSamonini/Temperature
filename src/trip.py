import numpy as np

def trip_calculator(europe_csv, start_city, final_city):
    """
    Create a fuction that, given in input a starting city, try the path for reaching a finla city, sercing for the three nearest cities,
        and choose for next stage until the function reach the target city

    Parameter: 
        europe_csv -> the DataFrame containing city data including names, coordinates, and other attributes.
        start_city -> the city where the trip start
        final_city -> the city where the trip end

    Return:
        cities_already_visited -> return the ordered list of the trip, from the start city, all the stages, and ending with the final city
    """
    recent_temperature_df = europe_csv[europe_csv['dt'] >= '2005-01-01'] # filter only the recent data
    
    # create a df that contains unique cities with his coordinates adn average temeprature
    europe_city = recent_temperature_df.groupby(['City', 'Latitude', 'Longitude'])['AverageTemperature'].mean().reset_index() 

    cities_already_visited = []
    city_deleted = set()

    # a NumPy array that contain the coordinates of the cities
    city_coords = europe_city[['Latitude', 'Longitude']].values

    def distance_calculation(current_coordinates, cities_not_visited):
        """
        This function calculate the distance from the current cities to the other cities in cities_not_visited and return a list
            containing the three nearest cities 

        Parameter: 
            current_coordinates -> the curdinates of the current city
            cities_not_visited -> the cities not visited and not deleted

        Return:
            cities_not_visited.iloc[closest_indices]['City'].tolist() -> return a list with the three nearest cities from the current city
        """
        # Calculate distances from the current city to all other cities in cities_not_visited
        distances = np.sqrt(
            (cities_not_visited['Latitude'].values - current_coordinates[0]) ** 2 +
            (cities_not_visited['Longitude'].values - current_coordinates[1]) ** 2
        )
        
        # Get indices of the closest 3 cities
        closest_indices = np.argsort(distances)[:3]
        return cities_not_visited.iloc[closest_indices]['City'].tolist()


    def trip_3_cities(europe_city, cities_already_visited, final_city):
        """
        This function determines the next city to visit during a trip across Europe by considering the closest cities
        and prioritizing the final destination if it's among them. If not, it selects the city with the highest average temperature.

        Parameters:
            europe_city -> DataFrame containing city data
            cities_already_visited -> List of cities already visited in the trip
            final_city -> The city that is the trip's final destination

        Returns:
            cities_already_visited -> Updates the list of visited cities by appending the next city to visit
        """
        current_city = cities_already_visited[-1] # the new current city is the last city in the list
        current_city_data = europe_city.query("City == @current_city") # take the data of the current city
        # take the coordinates of the city, latitude and longitude
        current_coordinates = np.array([current_city_data['Latitude'].values[0], current_city_data['Longitude'].values[0]]) 

        # Filter out cities that are already visited or deleted
        cities_not_visited = europe_city[~europe_city['City'].isin(cities_already_visited + list(city_deleted))]

        # Find the names of the 3 closest cities using distance calculation
        closest_3_cities_names = distance_calculation(current_coordinates, cities_not_visited)
        # Filter the DataFrame to include only the 3 closest cities
        closest_3_cities = cities_not_visited[cities_not_visited['City'].isin(closest_3_cities_names)]

        # Check if final_city is among the closest cities
        if final_city in closest_3_cities['City'].values:
            # If final_city is in the closest 3 cities, prioritize and choose it
            print(f"Final city {final_city} found in closest cities. Prioritizing it.")
            cities_already_visited.append(final_city)
        else:
            # Otherwise, select the city with the highest temperature
            highest_temp_city = closest_3_cities.loc[closest_3_cities['AverageTemperature'].idxmax(), 'City']
            cities_already_visited.append(highest_temp_city) # and append the city in cities_already_visited

            # Mark the other two cities as deleted so they are not reconsidered
            for city in closest_3_cities['City']:
                if city != highest_temp_city:
                    city_deleted.add(city)
        
    cities_already_visited.append(start_city)

    # Limit the number of iterations
    max_iterations = 500
    iteration = 0

    # continue the trip until the final_city is not in cities_already_visited, in that case we'll conclude the trip
    while final_city not in cities_already_visited and iteration < max_iterations:
        print(f"Iteration {iteration}: Currently at {cities_already_visited[-1]}") # print out the current city
        trip_3_cities(europe_city, cities_already_visited, final_city) # call the function
        iteration += 1

    # check if final_city is present in cities_already_visited, in that case we have a trip
    if final_city in cities_already_visited:
        print(f"Reached {final_city}!")
    else:
        print(f"Reached the iteration limit without reaching {final_city}.")

    print("Trip:", cities_already_visited)
    print("Number of cities visited:", len(cities_already_visited))
    print("Deleted cities:", city_deleted)
    print("Number of cities deleted:", len(city_deleted))

    return cities_already_visited