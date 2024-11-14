import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from geospatial_map import create_geospatial_map
from temp_chart import create_temp_trend_charts

# Load datasets
df = pd.read_csv('C:/Users/M2-Winterfell/Downloads/CS7DS4-Data-Visualization/A3/weather_forecast_data_realtime.csv')
df['date'] = pd.to_datetime(df['date'])
rainfall_df = pd.read_csv('C:/Users/M2-Winterfell/Downloads/CS7DS4-Data-Visualization/A3/max_rainfall.csv')
rainfall_df['date'] = pd.to_datetime(rainfall_df['date'])

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create the initial figures for the temp, humidity, and wind charts
temp_fig, humidity_fig, wind_fig = create_temp_trend_charts(df)

# Layout of the app
app.layout = dbc.Container([
    # html.H1("Singapore Weather Dashboard", style={'textAlign': 'center'}),
    
    # Dropdown menu for selecting the chart type
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
                style={'width': '50%'}  # Adjust width or position as needed
            )
        ], width=6)
    ], style={'margin-top': '10px'}),  # Reduce margin-top to bring it closer to H1 title
    
    # Placeholder for the selected chart
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='temp_trend_chart', figure=temp_fig)  # Display the initial temperature chart
        ], width=6)
    ], style={'margin-top': '0px', 'height': '60vh'}),  # Reduce margin-top to shift it higher

    # Day slider positioned above the geospatial map
    dbc.Row([
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
            ),
        ], width=6, style={'margin-bottom': '0px'})  # Slightly increase margin-bottom to bring it closer to the map
    ], style={'margin-top': '0px'}),  # Reduce margin-top to bring it closer to temp chart
    
    # Geospatial map positioned at the bottom left
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='geospatial_map_chart'),
        ], width=6)
    ], style={'height': '50vh'})  # Adjust height as needed for the map
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

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
