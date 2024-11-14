# main_app.py
# Control + C to terminate app
import pandas as pd
from dash import Dash, dcc, html, Input, Output
from scatter_matrix import create_scatter_matrix
from bubble_timeline import create_bubble_timeline

# Load dataset
df = pd.read_csv('C:/Users/M2-Winterfell/Downloads/CS7DS4-Data-Visualization/A3/weather_forecast_data_realtime.csv')
df['date'] = pd.to_datetime(df['date'])

# Initialize the app
app = Dash(__name__)

# Define layout of the app
app.layout = html.Div([
    html.H1("Singapore Weather Dashboard"),

    # Dropdown to select either Scatter Matrix or Bubble Timeline
    dcc.Dropdown(
        id='view_selector',
        options=[
            {'label': 'Scatter Matrix', 'value': 'scatter_matrix'},
            {'label': 'Bubble Timeline', 'value': 'bubble_timeline'}
        ],
        value='scatter_matrix',  # Default view
        style={'width': '70%', 'margin-bottom': '20px'}
    ),
    
    # Dropdown for selecting time range
    dcc.Dropdown(
        id='time_range',
        options=[
            {'label': 'Most Recent Week', 'value': 'week'},
            {'label': 'Most Recent Month', 'value': 'month'},
            {'label': 'Most Recent Year', 'value': 'year'},
            {'label': 'Full Dataset', 'value': 'full'}
        ],
        value='week',  # Default time range
        style={'width': '50%', 'margin-bottom': '20px'}
    ),

    # Placeholder for dynamic content
    html.Div(id='dynamic_chart_container'),
])

# Callback to update chart based on selected view and time range
@app.callback(
    Output('dynamic_chart_container', 'children'),
    Input('view_selector', 'value'),
    Input('time_range', 'value')
)
def update_graph(view_selector, time_range):
    if view_selector == 'scatter_matrix':
        scatter_matrix_fig = create_scatter_matrix(df, time_range)
        return dcc.Graph(id='scatter_matrix_chart', figure=scatter_matrix_fig)
    elif view_selector == 'bubble_timeline':
        bubble_timeline_fig = create_bubble_timeline(df, time_range)
        return dcc.Graph(id='bubble_timeline_chart', figure=bubble_timeline_fig)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
