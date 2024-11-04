# scatter_matrix.py
import pandas as pd
import plotly.express as px

def create_scatter_matrix(df, time_range):
    # Filter the dataset based on the selected time range
    if time_range == 'week':
        filtered_df = df[df['date'] >= df['date'].max() - pd.Timedelta(weeks=1)]
    elif time_range == 'month':
        filtered_df = df[df['date'] >= df['date'].max() - pd.DateOffset(months=1)]
    elif time_range == 'year':
        filtered_df = df[df['date'] >= df['date'].max() - pd.DateOffset(years=1)]
    else:
        filtered_df = df  # Full dataset

    # Create the scatter plot matrix
    fig = px.scatter_matrix(
        filtered_df,
        dimensions=['humidity_low', 'humidity_high', 'temperature_low', 'temperature_high'],
        color='forecast',
        size='wind_speed_high',  # Size of points represents wind speed
        size_max=30,             # Increase max size for visual clarity
        hover_data={'date': True},
        title="Scatter Plot Matrix for Temperature, Humidity, and Wind Speed"
    )

    fig.update_traces(diagonal_visible=False)  # Hide diagonal density plots
    fig.update_layout(height=800, width=1000)

    return fig
