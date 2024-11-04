# weather.py
import pandas as pd
import plotly.graph_objs as go

# Define regions' coordinates for map visualization
region_coordinates = {
    'East': {'lat': 1.35735, 'lon': 103.94},
    'West': {'lat': 1.352083, 'lon': 103.7},
    'North': {'lat': 1.41803, 'lon': 103.82025},
    'South': {'lat': 1.27431, 'lon': 103.851959},
    'Central': {'lat': 1.3521, 'lon': 103.8198}
}

def create_geospatial_map(df, time_range):
    # Get the current date to filter data
    today = df['date'].max().normalize()
    
    # Filter the dataset based on the selected time range
    if time_range == 'today':
        filtered_df = df[df['date'] == today]
    elif time_range == 'yesterday':
        filtered_df = df[df['date'] == today - pd.Timedelta(days=1)]
    elif time_range == 'day_before_yesterday':
        filtered_df = df[df['date'] == today - pd.Timedelta(days=2)]
    else:
        filtered_df = df  # Default fallback if time range is invalid or unspecified
    
    # Return an empty figure if there's no data for the selected time range
    if filtered_df.empty:
        return go.Figure()

    # Calculate PM2.5 average values for each region
    pm25_values = [
        filtered_df['pm25_east'].mean(),
        filtered_df['pm25_west'].mean(),
        filtered_df['pm25_north'].mean(),
        filtered_df['pm25_south'].mean(),
        filtered_df['pm25_central'].mean()
    ]
    
    # Gather additional data for hover information
    wind_speed = filtered_df['wind_speed_high'].mean()  # Average wind speed
    wind_direction = filtered_df['wind_direction'].mode()[0]  # Most common wind direction
    forecast = filtered_df['forecast'].mode()[0]  # Most common forecast
    
    # Define Scattermapbox trace for PM2.5 levels, color-coded by intensity
    pm25_trace = go.Scattermapbox(
        lat=[coords['lat'] for coords in region_coordinates.values()],
        lon=[coords['lon'] for coords in region_coordinates.values()],
        mode='markers',
        marker=dict(
            size=20,
            color=pm25_values,
            colorscale='Picnic',  # Color scale for PM2.5 intensity
            cmin=min(pm25_values),
            cmax=max(pm25_values),
            showscale=True,
            colorbar=dict(title="PM2.5 Levels", x=1.05)
        ),
        text=[
            f'Region: {region}<br>'
            f'PM2.5: {pm25_values[idx]:.2f}<br>'
            f'Wind Speed: {wind_speed:.2f} km/h<br>'
            f'Wind Direction: {wind_direction}<br>'
            f'Forecast: {forecast}'
            for idx, region in enumerate(region_coordinates.keys())
        ],  # Additional data for hover information
        hoverinfo='text'
    )
    
    # Configure layout for the map
    layout = go.Layout(
        title='PM2.5 Levels with Wind and Forecast Info (Hover to View)',
        mapbox=dict(
            style="carto-positron",  # Map style
            center=dict(lat=1.3521, lon=103.8198),  # Center on Singapore
            zoom=10,  # Set zoom level
        ),
        margin=dict(t=30, b=30, l=0, r=0),  # Adjust margins
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)  # Legend position
    )
    
    # Return the complete figure
    return go.Figure(data=[pm25_trace], layout=layout)
