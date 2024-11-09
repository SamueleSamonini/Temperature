# Weather Data Analysis and Visualization

This project explores historical global temperature trends, with a particular focus on Europe. Using the `Pandas`, `GeoPandas`, `Matplotlib`, and `NumPy` libraries, the project offers tools for analysis, visualization, and mapping to interpret climate data effectively.

## Project Workflow

### Data Cleaning and Preparation
The first step is preparing historical global temperature data to ensure consistency and accuracy in the analysis. This phase includes:

- **Data Cleaning**: The `data_clean_global_temperatures()` function removes missing values and duplicates, converting dates to a standard format.
- **Coordinate Management**: The `clean_coordinates()` function standardizes geographical data (latitude and longitude), removing any extraneous characters and ensuring that European city data is ready for mapping.

### Visualization of Global Temperature Trends
With the `temperature_graph()` function, the project provides an overview of global average temperatures, smoothed for a clearer visualization. Data from 1750 to 2015 is analyzed, with a primary focus on the period from 1840 onward to avoid potential inaccuracies in older records.

### Mapping European Temperatures
Once cleaned, the data is filtered to focus on Europe, excluding remote areas like Russia for a clearer, more targeted view:

- **Temperature Mapping by Country**: The `plot_europe()` function creates a color-coded map, where each country is represented based on its average temperature, allowing for quick insights into climate differences across regions.
- **Thermal Excursion Analysis**: An interesting feature of the project is the calculation of thermal excursions (the difference between maximum and minimum temperatures) for each European city. Cities with the 10 highest and lowest thermal excursions are highlighted on the map, making it easy to visually compare these variations using the `plot_europe()` function.

### Calculating the Warmest Route
Among the project's innovative features, `trip_calculator()` introduces the ability to find the warmest route between two cities by leveraging the average temperatures of nearby cities to suggest an optimal path. Thanks to the `KDTree` structure in `NumPy`, the calculation of nearby cities is extremely fast, allowing the identification of stops with the highest temperatures. The `plot_path()` function visually represents the selected route on a map of Europe, connecting cities in a clear and intuitive way.
