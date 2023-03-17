"""
App module for X-vault: a UFO sighting dashboard
Built with plotly Dash.

Author: J-A-Collins
"""

# Imports
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Read the UFO sightings data into a DataFrame
ufo_data = pd.read_csv('ufo_sighting_data.csv', low_memory=False)

ufo_data['datetime'] = pd.to_datetime(ufo_data['datetime'], errors='coerce', format='%m/%d/%Y %H:%M')
ufo_data['year'] = ufo_data['datetime'].dt.year

# Count sightings per year
sightings_per_year = ufo_data['year'].value_counts().sort_index().reset_index()
sightings_per_year.columns = ['year', 'count']


# Layout and interactivity
app = dash.Dash(__name__)

# Set the title of the Dash app
app.title = "The X-Vault"

app.layout = html.Div(className='container', children=[
    html.Div(style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between'}, children=[
        html.Div(style={'display': 'flex', 'align-items': 'baseline'}, children=[
            html.H1("The X-Vault:", style={'textAlign': 'left', 'color': '#ffffff', 'margin-right': '10px'}),
            html.H3("UFO sightings exploration and visualisations", style={'textAlign': 'left', 'color': '#ffffff'}),
        ]),
        html.Img(src='/assets/alien.png', width='100px', height='100px'),

    ]),
    html.Hr(style={'borderTop': '1px solid rgb(0, 255, 0)'}),
    html.P(
        id="description",
        children="† Data is taken from the National UFO Reporting Center (NUFORC). The center aims to "
                 "record, corroborate and document reports from individuals who have been witness to "
                 "unusual, possibly UFO-related events. NUFORC has processed over 150,000 reports, "
                 "and has distributed its information to thousands of individuals. ",
        style={'color': '#ffffff'}
    ),
    html.Div(className='slider-container', children=[
        html.Div(className='slider', children=[
            html.Br(),
            html.P("Drag the slider to change the year:", style={'color': '#ffffff'}),
            dcc.Slider(
                id='year-slider',
                min=ufo_data['year'].min(),
                max=ufo_data['year'].max(),
                value=ufo_data['year'].max(),
                marks={str(year): str(year) for year in ufo_data['year'].unique()},
                step=None,
                className='custom-slider'  # Add a className for custom CSS styling
            )
        ], style={'backgroundColor': '#3a3a3a', 'padding': '20px'})
    ]),
    html.Div(className='graphs-container', children=[
        html.Div(className='graphs', children=[
            html.Div(className='graph', children=[
                dcc.Graph(id='ufo-map')
            ], style={'width': '50%', 'display': 'inline-block'}),  # Adjust the width and display style
            html.Div(className='graph', children=[
                html.Div(className='dropdown-container', children=[
                    dcc.Dropdown(
                        id='bar-option',
                        options=[
                            {'label': 'Top 5 Locations', 'value': 'top_locations'},
                            {'label': 'Most Observed UFO Types', 'value': 'ufo_shapes'},
                            {'label': 'Highest Average Encounter Duration by Location', 'value': 'avg_duration'}
                        ],
                        value='top_locations',
                        clearable=False,
                        style={'color': '#000000'}
                    )
                ], style={'width': '63%', 'margin': '10px auto'}),
                dcc.Graph(id='ufo-bar-chart')
            ], style={'width': '50%', 'display': 'inline-block'})  # Adjust the width and display style
        ])
    ]),
    html.Hr(style={'borderTop': '1px solid rgb(0, 255, 0)'}),
    html.Div(className='line-chart-container', children=[
        html.Div(className='graph', children=[
            dcc.Graph(id='ufo-line-chart')
        ], style={'width': '100%', 'display': 'inline-block'})  # Adjust the width and display style
    ]),
    html.Hr(style={'borderTop': '1px solid rgb(0, 255, 0)'}),
    html.Div(className='kmeans-container', children=[
        html.H2("K-means Analysis", style={'textAlign': 'left', 'color': '#ffffff'}),

        html.Div(className='graph', children=[
            dcc.Graph(id='kmeans-map')
        ], style={'width': '100%', 'display': 'inline-block'})
    ])
])


@app.callback(
    [
        Output('ufo-map', 'figure'),
        Output('ufo-bar-chart', 'figure'),
        Output('ufo-line-chart', 'figure'),
    ],
    [
        Input('year-slider', 'value'),
        Input('bar-option', 'value')
    ])
def update_plots(selected_year, bar_option):
    filtered_data = ufo_data[ufo_data['year'] == selected_year]

    # Update the map
    map_fig = px.scatter_mapbox(filtered_data,
                                lat='latitude',
                                lon='longitude',
                                hover_name='city',
                                zoom=-1,
                                center=dict(lat=0, lon=0),
                                mapbox_style="carto-darkmatter")

    # Set the marker colour to bright green
    map_fig.update_traces(marker=dict(color='rgb(0,255,0)', size=10, opacity=0.8))

    total_sightings = len(filtered_data)
    map_fig.update_layout(
        title=f"UFO Sightings in {selected_year}: {total_sightings}",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='#3a3a3a',
        font=dict(color='#ffffff')
    )

    # Update the bar chart based on the selected option
    if bar_option == 'top_locations':
        top_locations = filtered_data['city'].value_counts().head(5)
        bar_fig = px.bar(
            x=top_locations.index, y=top_locations.values,
            labels={'x': 'City', 'y': 'Sightings'},
            template='plotly_dark'
        )

    elif bar_option == 'ufo_shapes':
        ufo_shapes = filtered_data['ufo_shape'].value_counts().head(5)
        bar_fig = px.bar(
            x=ufo_shapes.index, y=ufo_shapes.values,
            labels={'x': 'UFO Shape', 'y': 'Count'},
            template='plotly_dark'
        )

    elif bar_option == 'avg_duration':
        avg_duration = filtered_data.groupby('city')['encounter_duration'].mean().sort_values(ascending=False).head(5)
        bar_fig = px.bar(
            x=avg_duration.index, y=avg_duration.values,
            labels={'x': 'City', 'y': 'Average Encounter Duration (seconds)'},
            template='plotly_dark'
        )

    else:
        raise ValueError("Invalid bar chart option")

    # Set the bar color to bright green
    bar_fig.update_traces(marker=dict(color='rgb(0,255,0)'))

    bar_fig.update_layout(
        title=f"{bar_option.replace('_', ' ').title()} in {selected_year}",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='#3a3a3a',
        font=dict(color='#ffffff')
    )

    # Update the line chart
    filtered_df = sightings_per_year[sightings_per_year['year'] <= selected_year]

    line_fig = px.line(filtered_df, x='year', y='count', title="Total UFO Sightings Over Time",
                       labels={'year': 'Year', 'count': 'Sightings'},
                       line_shape='spline')

    line_fig.update_traces(line=dict(color='rgb(0, 255, 0)'))

    line_fig.update_layout(
        title_font=dict(size=24),
        xaxis_title_font=dict(size=18),
        yaxis_title_font=dict(size=18),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='#ffffff')
    )

    return map_fig, bar_fig, line_fig


@app.callback(
    Output('kmeans-map', 'figure'),
    Input('year-slider', 'value'))
def update_kmeans_map(selected_year):
    filtered_data = ufo_data[ufo_data['year'] == selected_year]

    # Read the K-means cluster results from a file (e.g., a CSV file)
    # Make sure to filter the cluster results based on the selected year
    kmeans_results = pd.read_csv("ufo_sighting_data_with_clusters.csv")
    kmeans_results['datetime'] = pd.to_datetime(kmeans_results['datetime'], errors='coerce', format='%m/%d/%Y %H:%M')
    kmeans_results['year'] = kmeans_results['datetime'].dt.year
    kmeans_filtered_data = kmeans_results[kmeans_results['year'] == selected_year]

    # Create a scatter mapbox plot with the K-means cluster results
    kmeans_map_fig = px.scatter_mapbox(kmeans_filtered_data,
                                       lat='latitude',
                                       lon='longitude',
                                       hover_name='city',
                                       color='cluster',
                                       zoom=0.2,
                                       center=dict(lat=0, lon=0),
                                       height=500,
                                       mapbox_style="carto-darkmatter")

    kmeans_map_fig.update_layout(
        title=f"K-means Clustering of UFO Sightings in {selected_year}",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='#3a3a3a',
        font=dict(color='#ffffff')
    )

    return kmeans_map_fig


if __name__ == '__main__':
    app.run_server(debug=True)
