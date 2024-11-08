import pandas as pd
import matplotlib.pyplot as plt
import sys
import csv

def data_clean_global_temperatures(csv_path):
    data = pd.read_csv(csv_path)
    
    data['dt'] = pd.to_datetime(data['dt']) # convert from string to datetime format
    data_clean = data.dropna(subset = ['LandAverageTemperature']) # delete some rows in case of missing values
    data_clean.fillna(method = 'ffill', inplace = True) # in case of missing values, this operation complete the missing values with a coerent data
    data_clean.drop_duplicates(inplace = True) # drop duplicates rows
    data_clean.columns = [col.lower() for col in data_clean.columns] # all the words are now lowercase

    return(data_clean)

def clean_coordinates(df, lat_col = 'Latitude', lon_col = 'Longitude'):
    df['dt'] = pd.to_datetime(df['dt'])
    def clean_lat_lon(value):
        # Remove non-numeric characters except for "N", "S", "E", and "W"
        if isinstance(value, str):
            if value[-1] == 'N':
                return float(value[:-1])  # North is positive
            elif value[-1] == 'S':
                return -float(value[:-1])  # South is negative

            elif value[-1] == 'E':
                return float(value[:-1])  # East is positive
            elif value[-1] == 'W':
                return -float(value[:-1])  # West is negative
        return float(value)  # If already clean, just convert to float

    # Apply cleaning function to latitude and longitude columns
    df[lat_col] = df[lat_col].apply(clean_lat_lon)
    df[lon_col] = df[lon_col].apply(clean_lat_lon)

    df = df[~(df['City'] == 'Brest')]
    
    return df