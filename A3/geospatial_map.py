import pandas as pd
import plotly.graph_objs as go

# Define regions' coordinates for PM2.5 map visualization
region_coordinates = {
    'East': {'lat': 1.35735, 'lon': 103.94},
    'West': {'lat': 1.352083, 'lon': 103.7},
    'North': {'lat': 1.41803, 'lon': 103.82025},
    'South': {'lat': 1.27431, 'lon': 103.851959},
    'Central': {'lat': 1.3521, 'lon': 103.8198}
}

def create_geospatial_map(df, rainfall_df, selected_date):
    # Filter the dataset for the specific date
    filtered_df = df[df['date'] == selected_date]
    filtered_rainfall_df = rainfall_df[rainfall_df['date'] == selected_date]
    
    # Return an empty figure if there's no data for the selected day
    if filtered_df.empty or filtered_rainfall_df.empty:
        return go.Figure()

    pm25_values = [
        filtered_df['pm25_east'].mean(),
        filtered_df['pm25_west'].mean(),
        filtered_df['pm25_north'].mean(),
        filtered_df['pm25_south'].mean(),
        filtered_df['pm25_central'].mean()
    ]
    
    # Define the PM2.5 and rainfall traces as before
    pm25_trace = go.Scattermapbox(
        lat=[coords['lat'] for coords in region_coordinates.values()],
        lon=[coords['lon'] for coords in region_coordinates.values()],
        mode='markers',
        marker=dict(
            size=[value for value in pm25_values],  
            color='red',
            opacity=1.0
        ),
        text=[f'Region: {region}<br>PM2.5: {pm25_values[idx]:.2f}' 
              for idx, region in enumerate(region_coordinates.keys())],
        hoverinfo='text',
        name='PM2.5'
    )
    
    link_traces = []
    for _, station in filtered_rainfall_df.iterrows():
        if station['rainfall_value'] > 0:
            for region_name, region_coord in region_coordinates.items():
                link_trace = go.Scattermapbox(
                    lat=[station['latitude'], region_coord['lat'], None],
                    lon=[station['longitude'], region_coord['lon'], None],
                    mode='lines',
                    line=dict(width=station['rainfall_value'], color='green'),
                    opacity=0.2,
                    showlegend=False
                )
                link_traces.append(link_trace)

    rainfall_trace = go.Scattermapbox(
        lat=filtered_rainfall_df['latitude'],
        lon=filtered_rainfall_df['longitude'],
        mode='markers',
        marker=dict(
            size=10,
            color=filtered_rainfall_df['rainfall_value'],
            colorscale='Viridis_r',
            cmin=0,
            cmax=filtered_rainfall_df['rainfall_value'].max(),
            showscale=True,
            colorbar=dict(title="Rainfall", x=0.9)
        ),
        text=[f'Station: {row["station_name"]}<br>Rainfall: {row["rainfall_value"]:.2f} mm'
              for _, row in filtered_rainfall_df.iterrows()],
        hoverinfo='text',
        name='Rainfall'
    )

    # Configure layout with legend at the top
    layout = go.Layout(
        title=dict(
        text=f'PM2.5 and Rainfall Levels for {selected_date.date()}',
        y=0.1  ,  
        font=dict(size=14)
    ),
        mapbox=dict(
            style="carto-positron",
            center=dict(lat=1.3521, lon=103.8198),
            zoom=10.5,
        ),
        margin=dict(t=30, b=30, l=0, r=0),
        legend=dict(orientation="h", yanchor="bottom", y=0.9, xanchor="center", x=0.1)
    )

    # Combine traces into a single figure
    fig = go.Figure(data=link_traces + [pm25_trace, rainfall_trace], layout=layout)
    return fig
