# Weather Data Analysis and Visualization

This university project explores historical global temperature trends, focusing on Europe. Using `Pandas`, `GeoPandas`, `Matplotlib`, `NumPy`, and `Streamlit`, the project offers tools for analysis, visualization, and mapping to interpret climate data effectively. The interactive application is built with `Streamlit`, providing an intuitive user interface.

## Notes

- You can access the project at [this link](https://temperaturepythonuniversityproject.streamlit.app/ "Temperature App").
- This project is part of a university assignment for the **Data Science for Economics (DSE)** course at the **University of Milan (Unimi)**. Its goal is to explore and visualize historical temperature data.
- The project also includes a Jupyter Notebook called `version_without_streamlit.ipynb`. This is an older version of the code without Streamlit integration, included in the project for educational purposes only.

## Project Workflow

### Data Cleaning and Preparation
The first step is preparing historical global temperature data to ensure consistency and accuracy in the analysis. This phase includes:

- **Data Cleaning**: The `data_clean_global_temperatures()` function removes missing values and duplicates, converting dates to a standard format.
- **Coordinate Management**: The `clean_coordinates()` function standardizes geographical data (latitude and longitude), ensuring that European city data is ready for mapping.

### Visualization of Global Temperature Trends
With the `plot_line_trend()` function, the project provides an overview of global average temperatures, smoothed for a clearer visualization. Data from 1750 to 2015 is analyzed, with a primary focus on the period from 1840 onward to avoid potential inaccuracies in older records.

### Mapping European Temperatures
Once cleaned, the data is filtered to focus on Europe, excluding remote areas like Russia for a clearer, more targeted view:

- **Temperature Mapping by Country**: The `plot_europe()` function creates a color-coded map, where each country is represented based on its average temperature, allowing for quick insights into climate differences across regions.
- **Thermal Excursion Analysis**: A feature of the project is the calculation of thermal excursions (the difference between maximum and minimum temperatures) for each European city. Cities with the 10 highest and lowest thermal excursions are highlighted on the map, making it easy to visually compare these variations using the `plot_europe()` function.

### Calculating the Warmest Route
Among the project's features, `trip_calculator()` introduces the ability to find the warmest route between two cities by leveraging the average temperatures of nearby cities to suggest an optimal path. The function use the `NumPy` libraary for distance calculations, ensuring simplicity and speed. The function:

- Processes the recent temperature data to calculate averages for cities.
- Filters out already-visited or invalid cities.
- Calculates distances using `NumPy` to suggest the next city in the route.
    - The function chooses the warmest city among the three nearest cities

The `plot_path()` function visually represents the selected route on a map of Europe, connecting cities in a clear and intuitive way.

## Interactive Features
The project is built with `Streamlit`, enabling an interactive experience. Users can:

- Explore global temperature trends through dynamic graphs.
- Interact with temperature maps of Europe to visualize average temperatures and thermal excursions.
- Calculate and visualize the warmest route between cities in Europe.