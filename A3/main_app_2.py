import pandas as pd
import os
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from scatter_matrix import create_scatter_matrix
from bubble_timeline import create_bubble_timeline

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Load dataset
df = pd.read_csv('../A3/weather_forecast_data_realtime.csv')
df['date'] = pd.to_datetime(df['date'])

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define layout of the app
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),  # Tracks the URL for navigation
    html.H1("Singapore Weather Dashboard"),

    # Dropdown to select either Scatter Matrix or Bubble Timeline and navigation button
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='view_selector',
                options=[
                    {'label': 'Scatter Matrix', 'value': 'scatter_matrix'},
                    {'label': 'Bubble Timeline', 'value': 'bubble_timeline'}
                ],
                value='scatter_matrix',  # Default view
                style={'width': '50%'}  # Full width of the column
            )
        ], width=6),
        dbc.Col([
            dbc.Button(
                "Go to Main Dashboard",
                id="navigate-button",
                n_clicks=0,
                style={'width': '50%'}  # Match the dropdown width
            )
        ], width=6)
    ], style={'margin-top': '10px'}),

    # Dropdown for selecting time range
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='time_range',
                options=[
                    {'label': 'Most Recent Week', 'value': 'week'},
                    {'label': 'Most Recent Month', 'value': 'month'},
                    {'label': 'Most Recent Year', 'value': 'year'},
                    {'label': 'Full Dataset', 'value': 'full'}
                ],
                value='week',  # Default time range
                style={'width': '50%'}  # Full width of the column
            )
        ], width=12)
    ], style={'margin-top': '20px'}),

    # Placeholder for dynamic content
    html.Div(id='dynamic_chart_container'),
], fluid=True)

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

# Callback to navigate to main_app_1
@app.callback(
    Output('url', 'pathname'),
    Input('navigate-button', 'n_clicks')
)
def navigate_to_app1(n_clicks):
    if n_clicks > 0:
        return '/app1'
    return '/'

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
