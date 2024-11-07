# Weather Data Analysis and Visualization

This project explores global temperature trends using historical data, with a focus on Europe. It uses `Pandas` for data handling, `GeoPandas` for mapping, and `Matplotlib` for visualizations.

The project starts by cleaning global temperature data, fixing any missing values, and formatting coordinates for accurate maps. It then shows smoothed global temperature trends from 1750, focusing on data from 1840 onward for better accuracy. For Europe, it creates a color-coded map that highlights temperature differences by country, leaving out Russia and distant areas for a clearer view.

One interesting feature is the calculation of thermal excursions (the difference between maximum and minimum temperatures) for European cities. This identifies the top 10 cities with the highest and lowest excursions, and these are plotted on the map for easy comparison.

### Future Feature

A new feature will help find the warmest route between two cities based on current temperatures. This tool will suggest a path through nearby cities with the highest average temperatures, helping users find the warmest way from one city to another.
