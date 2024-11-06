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