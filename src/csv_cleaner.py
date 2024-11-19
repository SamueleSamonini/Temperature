import pandas as pd

def data_clean_global_temperatures(csv_path):
    """
    Cleans and preprocesses a global temperature dataset from a CSV file.

    Parameter: 
        csv_path -> The file path of the CSV file containing the dataset.

    Return:
        data_clean -> A cleaned and preprocessed DataFrame.
    """
    data = pd.read_csv(csv_path)
    
    data['dt'] = pd.to_datetime(data['dt']) # convert from string to datetime format
    data_clean = data.dropna(subset = ['LandAverageTemperature']) # delete some rows in case of missing values
    data_clean.fillna(method = 'ffill', inplace = True) # in case of missing values, this operation complete the missing values with a coerent data
    data_clean.drop_duplicates(inplace = True) # drop duplicates rows
    data_clean.columns = [col.lower() for col in data_clean.columns] # all the words are now lowercase

    return(data_clean)

def clean_coordinates(df, lat_col = 'Latitude', lon_col = 'Longitude'):
    """
    Remove non-numeric characters except for "N", "S", "E", and "W". And also set the dt column to datetime values.

    Parameters: 
        df -> The CSV file that contain all the cities
        lat_col -> the latitude value
        lon_col -> the longitude value

    Return:
        df -> A dataframe with cleaned coordinates
    """
    df['dt'] = pd.to_datetime(df['dt'])
    def clean_lat_lon(value):
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
    
    return df