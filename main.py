import pandas as pd
import matplotlib.pyplot as plt
import sys
import csv

# first of all we load the CSV file
def data_clean_global_temperatures(csv_path):
    data = pd.read_csv(csv_path)
    
    data['dt'] = pd.to_datetime(data['dt']) # convert from string to datetime format
    data_clean = data.dropna(subset = ['LandAverageTemperature']) # delete some rows in case of missing values
    data_clean.fillna(method = 'ffill', inplace = True) # in case of missing values, this operation complete the missing values with a coerent data
    data_clean.drop_duplicates(inplace = True) # drop duplicates rows
    data_clean.columns = [col.lower() for col in data_clean.columns] # all the words are now lowercase

    return(data_clean)

csv_path = 'data/GlobalTemperatures.csv'
data_cleaned = data_clean_global_temperatures(csv_path)

print(data_cleaned)

# we want a graph to visualize better the vhange of temperatures
data_cleaned['smoothedtemperature'] = data_cleaned['landaveragetemperature'].rolling(window = 12, center = True).mean()

plt.figure(figsize = (12, 6))
plt.plot(data_cleaned['dt'], data_cleaned['smoothedtemperature'], label = 'Average temperature', color = 'green')
plt.title('Average world temperature 1750/2015')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.show()

data_filtered = data_cleaned[(data_cleaned['dt'] >= '1840-01-01') & (data_cleaned['dt'] <= '2015-12-31')]
data_filtered['smoothedtemperature'] = data_filtered['landaveragetemperature'].rolling(window = 12, center = True).mean()

plt.figure(figsize = (12, 6))
plt.plot(data_filtered['dt'], data_filtered['smoothedtemperature'], label = 'Average temperature', color = 'red')
plt.title('Average world temperature 1840/2015')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.show()