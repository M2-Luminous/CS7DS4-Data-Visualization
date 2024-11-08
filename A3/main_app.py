# main_app.py
import pandas as pd
from dash import Dash, dcc, html, Input, Output
from temp_chart import create_temp_trend_charts
from wind_rose_chart import create_wind_rose_chart
from scatter_matrix import create_scatter_matrix
from geospatial_map import create_geospatial_map
from stream_graph import create_streamgraph
from bubble_timeline import create_bubble_timeline

# Load the weather dataset
df = pd.read_csv('C:/Users/M2-Winterfell/Downloads/CS7DS4-Data-Visualization/A3/weather_forecast_data_realtime.csv')
df['date'] = pd.to_datetime(df['date'])

# Load the rainfall dataset
rainfall_df = pd.read_csv('C:/Users/M2-Winterfell/Downloads/CS7DS4-Data-Visualization/A3/max_rainfall.csv')
rainfall_df['date'] = pd.to_datetime(rainfall_df['date'])

# Initialize the app
app = Dash(__name__)

# Define layout of the app
app.layout = html.Div([
    html.H1("Singapore Weather Dashboard"),

    # Dropdown to select different chart views
    dcc.Dropdown(
        id='view_selector',
        options=[
            {'label': 'Temperature, Humidity, and Wind Speed Trends', 'value': 'trends'},
            {'label': 'Wind Rose Chart', 'value': 'wind_rose'},
            {'label': 'Scatter Matrix', 'value': 'scatter_matrix'},
            {'label': 'Geospatial Map', 'value': 'geospatial_map'},
            {'label': 'Stream Graph', 'value': 'stream_graph'},
            {'label': 'Bubble Timeline', 'value': 'bubble_timeline'}
        ],
        value='trends',
        style={'width': '70%', 'margin-bottom': '20px'}
    ),

    # Dropdown for selecting time range, shown only for views that need it
    dcc.Dropdown(id='time_range', style={'width': '50%', 'margin-bottom': '20px'}),

    html.Div(
        dcc.Slider(
            id='day_slider',
            min=0,
            max=29,
            value=0,  # Default to the most recent day
            marks={i: f'{i}d ago' if i > 0 else 'Today' for i in range(30)},
            step=1,
            included=False,
            updatemode='drag'
        ),
        style={'width': '90%'}  # Apply width to the div container
    ),

    # Placeholder for dynamic content
    html.Div(id='dynamic_chart_container'),
])

# Callback to update time range dropdown options based on selected view
@app.callback(
    Output('time_range', 'options'),
    Output('time_range', 'value'),
    Output('time_range', 'style'),
    Output('day_slider', 'style'),
    Input('view_selector', 'value')
)
def update_time_range_selector(view_selector):
    # Define time range options for each type of chart
    if view_selector in ['trends', 'scatter_matrix', 'bubble_timeline']:
        options = [
            {'label': 'Most Recent Week', 'value': 'week'},
            {'label': 'Most Recent Month', 'value': 'month'},
            {'label': 'Most Recent Year', 'value': 'year'},
            {'label': 'Full Dataset', 'value': 'full'}
        ]
        time_range_style = {'width': '50%', 'margin-bottom': '20px'}
        day_slider_style = {'display': 'none'}
    elif view_selector == 'wind_rose':
        options = [
            {'label': 'Most Recent Week 1', 'value': 'week1'},
            {'label': 'Most Recent Week 2', 'value': 'week2'},
            {'label': 'Most Recent Week 3', 'value': 'week3'},
            {'label': 'Full Dataset', 'value': 'full'}
        ]
        time_range_style = {'width': '50%', 'margin-bottom': '20px'}
        day_slider_style = {'display': 'none'}
    elif view_selector == 'stream_graph':
        options = [
            {'label': 'Most Recent Month', 'value': 'month'},
            {'label': 'Most Recent Year', 'value': 'year'},
            {'label': 'Full Dataset', 'value': 'full'}
        ]
        time_range_style = {'width': '50%', 'margin-bottom': '20px'}
        day_slider_style = {'display': 'none'}
    elif view_selector == 'geospatial_map':
        options = [
            {'label': 'Today', 'value': 'today'},
            {'label': 'Yesterday', 'value': 'yesterday'},
            {'label': 'The Day Before Yesterday', 'value': 'day_before_yesterday'}
        ]
        time_range_style = {'display': 'none'}
        day_slider_style = {'width': '70%', 'margin-bottom': '20px'}

    return options, options[0]['value'], time_range_style, day_slider_style

# Callback to update chart based on selected view, time range, and day slider
@app.callback(
    Output('dynamic_chart_container', 'children'),
    Input('view_selector', 'value'),
    Input('time_range', 'value'),
    Input('day_slider', 'value')
)
def update_graph(view_selector, time_range, day_slider_value):
    # Check which view is selected
    if view_selector == 'geospatial_map':
        # Calculate date for the selected day in the last 30 days
        selected_date = df['date'].max().normalize() - pd.Timedelta(days=day_slider_value)
        geospatial_map_fig = create_geospatial_map(df, rainfall_df, selected_date)
        return dcc.Graph(id='geospatial_map_chart', figure=geospatial_map_fig)
    
    elif view_selector == 'trends':
        temp_fig, humidity_fig, wind_fig = create_temp_trend_charts(df, time_range)
        return html.Div([
            dcc.Graph(id='temp_trend_chart', figure=temp_fig),
            dcc.Graph(id='humidity_trend_chart', figure=humidity_fig),
            dcc.Graph(id='wind_trend_chart', figure=wind_fig)
        ])
    
    elif view_selector == 'wind_rose':
        wind_rose_fig = create_wind_rose_chart(df, time_range)
        return dcc.Graph(id='wind_rose_chart', figure=wind_rose_fig)
    
    elif view_selector == 'scatter_matrix':
        scatter_matrix_fig = create_scatter_matrix(df, time_range)
        return dcc.Graph(id='scatter_matrix_chart', figure=scatter_matrix_fig)
    
    elif view_selector == 'stream_graph':
        stream_graph_fig = create_streamgraph(df, time_range)
        return dcc.Graph(id='stream_graph_chart', figure=stream_graph_fig)
    
    elif view_selector == 'bubble_timeline':
        bubble_timeline_fig = create_bubble_timeline(df, time_range)
        return dcc.Graph(id='bubble_timeline_chart', figure=bubble_timeline_fig)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
