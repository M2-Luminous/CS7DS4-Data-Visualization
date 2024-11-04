# temp_chart.py
import pandas as pd
import plotly.graph_objs as go

def create_temp_trend_charts(df, time_range):
    # Filter dataset based on time range
    if time_range == 'week':
        filtered_df = df[df['date'] >= df['date'].max() - pd.Timedelta(weeks=1)]
    elif time_range == 'month':
        filtered_df = df[df['date'] >= df['date'].max() - pd.DateOffset(months=1)]
    elif time_range == 'year':
        filtered_df = df[df['date'] >= df['date'].max() - pd.DateOffset(years=1)]
    else:
        filtered_df = df  # Full dataset

    # Temperature chart
    trace_temp_high = go.Scatter(
        x=filtered_df['date'], y=filtered_df['temperature_high'],
        mode='lines+markers', name='High Temp',
        hovertemplate='Date: %{x}<br>High Temp: %{y}°C<extra></extra>',
        line=dict(color='firebrick')
    )
    trace_temp_low = go.Scatter(
        x=filtered_df['date'], y=filtered_df['temperature_low'],
        mode='lines+markers', name='Low Temp',
        hovertemplate='Date: %{x}<br>Low Temp: %{y}°C<extra></extra>',
        line=dict(color='royalblue'),
        yaxis='y2'
    )
    temp_layout = go.Layout(
        title='Temperature Trends',
        xaxis=dict(title='Date'),
        yaxis=dict(title='High Temp (°C)', titlefont=dict(color='firebrick')),
        yaxis2=dict(title='Low Temp (°C)', titlefont=dict(color='royalblue'), overlaying='y', side='right'),
        hovermode='x unified'
    )

    # Humidity chart
    trace_humidity_high = go.Scatter(
        x=filtered_df['date'], y=filtered_df['humidity_high'],
        mode='lines+markers', name='High Humidity',
        hovertemplate='Date: %{x}<br>High Humidity: %{y}%<extra></extra>',
        line=dict(color='green')
    )
    trace_humidity_low = go.Scatter(
        x=filtered_df['date'], y=filtered_df['humidity_low'],
        mode='lines+markers', name='Low Humidity',
        hovertemplate='Date: %{x}<br>Low Humidity: %{y}%<extra></extra>',
        line=dict(color='blue'),
        yaxis='y2'
    )
    humidity_layout = go.Layout(
        title='Humidity Trends',
        xaxis=dict(title='Date'),
        yaxis=dict(title='High Humidity (%)', titlefont=dict(color='green')),
        yaxis2=dict(title='Low Humidity (%)', titlefont=dict(color='blue'), overlaying='y', side='right'),
        hovermode='x unified'
    )

    # Wind Speed chart
    trace_wind_high = go.Scatter(
        x=filtered_df['date'], y=filtered_df['wind_speed_high'],
        mode='lines+markers', name='High Wind Speed',
        hovertemplate='Date: %{x}<br>High Wind Speed: %{y} km/h<extra></extra>',
        line=dict(color='orange')
    )
    trace_wind_low = go.Scatter(
        x=filtered_df['date'], y=filtered_df['wind_speed_low'],
        mode='lines+markers', name='Low Wind Speed',
        hovertemplate='Date: %{x}<br>Low Wind Speed: %{y} km/h<extra></extra>',
        line=dict(color='purple'),
        yaxis='y2'
    )
    wind_layout = go.Layout(
        title='Wind Speed Trends',
        xaxis=dict(title='Date'),
        yaxis=dict(title='High Wind Speed (km/h)', titlefont=dict(color='orange')),
        yaxis2=dict(title='Low Wind Speed (km/h)', titlefont=dict(color='purple'), overlaying='y', side='right'),
        hovermode='x unified'
    )

    # Return the figures for the three charts
    return (
        go.Figure(data=[trace_temp_high, trace_temp_low], layout=temp_layout),
        go.Figure(data=[trace_humidity_high, trace_humidity_low], layout=humidity_layout),
        go.Figure(data=[trace_wind_high, trace_wind_low], layout=wind_layout)
    )
