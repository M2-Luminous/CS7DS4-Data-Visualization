import pandas as pd
import os
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from geospatial_map import create_geospatial_map
from temp_chart import create_temp_trend_charts
from wind_rose_chart import create_wind_rose_chart
from stream_graph import create_streamgraph  
from pie_charts import create_pie_charts     

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Load datasets
df = pd.read_csv('../A3/weather_forecast_data_realtime.csv')
rainfall_df = pd.read_csv('../A3/max_rainfall.csv')
df['date'] = pd.to_datetime(df['date'])
rainfall_df['date'] = pd.to_datetime(rainfall_df['date'])

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create the initial figures for the temp, humidity, and wind charts
temp_fig, humidity_fig, wind_fig = create_temp_trend_charts(df)

# Create the wind rose charts for the first and second month
wind_rose_fig1 = create_wind_rose_chart(df, 'month1', title="Latest Month Wind")
wind_rose_fig2 = create_wind_rose_chart(df, 'month2', title="2nd Latest Month Wind")

# Create the stream graph
stream_fig = create_streamgraph(df)

# Create the pie charts for forecast type and wind direction
forecast_pie_chart, wind_direction_pie_chart = create_pie_charts(df)

# Layout for main_app_1
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),  # Tracks the URL
    html.H1("Singapore Weather Dashboard"),
    
    # Dropdown menu and navigation button in the same row
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="chart_selector",
                options=[
                    {'label': 'Temperature', 'value': 'temperature'},
                    {'label': 'Humidity', 'value': 'humidity'},
                    {'label': 'Wind Speed', 'value': 'wind'}
                ],
                value='temperature',  # Default selection
                clearable=False,
                style={'width': '50%'}  # Full width of the column
            )
        ], width=6),
        dbc.Col([
            dbc.Button(
                "Go to Scatter Matrix and Bubble Timeline",
                id="navigate-button",
                n_clicks=0,
                style={'width': '50%'}  # Match the dropdown width
            )
        ], width=6)
    ], style={'margin-top': '10px'}),
    
    dbc.Row([
        # Left column containing temp chart, day slider, and geospatial map
        dbc.Col([
            dcc.Graph(id='temp_trend_chart', figure=temp_fig),
            dbc.Col([
                dcc.Slider(
                    id='day_slider',
                    min=0,
                    max=29,
                    value=0,
                    step=1,
                    included=False,
                    updatemode='drag',
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], style={'margin-top': '20px', 'margin-bottom': '10px'}),
            dcc.Graph(id='geospatial_map_chart')
        ], width=6, style={'height': '100vh'}),
        
        # Right column containing two wind rose charts, stream graph, and pie charts
        dbc.Col([
            dbc.Row([
                dbc.Col(dcc.Graph(id='wind_rose_chart1', figure=wind_rose_fig1), width=6),
                dbc.Col(dcc.Graph(id='wind_rose_chart2', figure=wind_rose_fig2), width=6)
            ]),
            # Stream graph below wind rose charts
            dbc.Row([
                dbc.Col(dcc.Graph(id='stream_graph', figure=stream_fig), width=12)
            ], style={'margin-top': '0px'}),  # Adjust margin to position stream graph as needed
            
            # New row for pie charts below stream graph
            dbc.Row([
                dbc.Col(dcc.Graph(id='forecast_pie_chart', figure=forecast_pie_chart), width=6),
                dbc.Col(dcc.Graph(id='wind_direction_pie_chart', figure=wind_direction_pie_chart), width=6)
            ], style={'margin-top': '20px'})  # Add margin for spacing
        ], style={'height': '100vh'})
    ])
], fluid=True)

# Callback to update the displayed trend chart based on dropdown selection
@app.callback(
    Output('temp_trend_chart', 'figure'),
    Input('chart_selector', 'value')
)
def update_temp_chart(selected_chart):
    if selected_chart == 'temperature':
        return temp_fig
    elif selected_chart == 'humidity':
        return humidity_fig
    elif selected_chart == 'wind':
        return wind_fig

# Callback to update the geospatial map
@app.callback(
    Output('geospatial_map_chart', 'figure'),
    Input('day_slider', 'value')
)
def update_geospatial_map(day_slider_value):
    # Selected date for the geospatial map
    selected_date = df['date'].max().normalize() - pd.Timedelta(days=day_slider_value)
    
    # Generate the figure for the geospatial map
    geospatial_map_fig = create_geospatial_map(df, rainfall_df, selected_date)
    
    # Return the geospatial map figure
    return geospatial_map_fig

# Callback to navigate to main_app_2
@app.callback(
    Output('url', 'pathname'),
    Input('navigate-button', 'n_clicks')
)
def navigate_to_app2(n_clicks):
    if n_clicks > 0:
        return '/app2'
    return '/'

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
