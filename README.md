# The X-Vault
## A UFO Sightings Dashboard

This repository contains the source code for an interactive web application to explore and visualise UFO sightings data. The data is sourced from the National UFO Reporting Center (NUFORC), an organization dedicated to the collection and documentation of UFO sighting reports.

The dashboard provides a variety of visualisations, including a map of sightings, bar charts displaying the most common sighting locations and UFO shapes, and a line chart showing the total number of sightings over time. Users can interact with the dashboard using a slider to filter the data by year and a dropdown to change the bar chart visualisation.

## Features

- Interactive heatmap of UFO sightings
- Bar charts displaying the top 5 sighting locations, most observed UFO shapes, and highest average encounter durations by location
- Line chart showing the total number of sightings over time
- Slider to filter the data by year
- Dropdown menu to change the bar chart visualisation
- K-means clustering analysis for geospatial visualisation

## Installation

1. Clone the repository: git clone https://github.com/j-a-collins/ufo-sightings-dashboard.git
2. Change to the project directory:
    cd ufo-sightings-dashboard
3. Create a virtual environment and activate it: python -m venv venv
use venv\Scripts\activate
4. Install the required packages: pip install -r requirements.txt


## Usage

1. Run the app: python app.py
2. Open a web browser and navigate to [http://127.0.0.1:8050/](http://127.0.0.1:8050/)

## Tech

- Python 3.9
- Dash and Plotly
- Pandas
- Scikit-learn
