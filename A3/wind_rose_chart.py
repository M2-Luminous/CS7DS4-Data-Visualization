# wind_rose_chart.py
import pandas as pd
import plotly.graph_objs as go

def create_wind_rose_chart(df, time_range, title):
    # Filter the dataset based on time range
    if time_range == 'month1':
        filtered_df = df[df['date'] >= df['date'].max() - pd.Timedelta(days=30)]
    elif time_range == 'month2':
        filtered_df = df[(df['date'] >= df['date'].max() - pd.Timedelta(days=60)) & 
                         (df['date'] < df['date'].max() - pd.Timedelta(days=30))]
    else:
        filtered_df = df  # Full dataset

    # Wind direction categories
    wind_directions = df['wind_direction'].unique().tolist()  # Use actual dataset values

    # Group by wind direction and calculate the mean wind speed for high and low
    wind_speed_low = filtered_df.groupby('wind_direction')['wind_speed_low'].mean().reindex(wind_directions, fill_value=0)
    wind_speed_high = filtered_df.groupby('wind_direction')['wind_speed_high'].mean().reindex(wind_directions, fill_value=0)

    # Wind Rose chart
    trace_low_speed = go.Barpolar(
        r=wind_speed_low[wind_directions],  # Low wind speeds
        theta=wind_directions,
        name='Low Wind Speed',
        marker=dict(color='royalblue'),
        hovertemplate='Wind Direction: %{theta}<br>Low Wind Speed: %{r} km/h<extra></extra>'
    )
    
    trace_high_speed = go.Barpolar(
        r=wind_speed_high[wind_directions],  # High wind speeds
        theta=wind_directions,
        name='High Wind Speed',
        marker=dict(color='firebrick'),
        hovertemplate='Wind Direction: %{theta}<br>High Wind Speed: %{r} km/h<extra></extra>'
    )
    
    # Layout with dynamic title
    wind_rose_layout = go.Layout(
        title=dict(
            text=title,
            font=dict(size=15)  # Adjust title font size if needed
        ),
        polar=dict(
            radialaxis=dict(
                range=[0, max(wind_speed_high.max(), wind_speed_low.max())],
                visible=True,
                title=dict(
                    text='Wind Speed (km/h)',
                    font=dict(size=10)
                ),
                tickfont=dict(size=8)
            ),
            angularaxis=dict(
                tickfont=dict(size=8)
            )
        ),
        legend=dict(
            font=dict(size=10)
        ),
        showlegend=True
    )

    # Return the figure
    return go.Figure(data=[trace_low_speed, trace_high_speed], layout=wind_rose_layout)
