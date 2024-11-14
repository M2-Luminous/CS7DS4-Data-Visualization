# temp_chart.py
import pandas as pd
import plotly.graph_objs as go

def create_temp_trend_charts(df):
    # Filter dataset to show only data from the last month
    filtered_df = df[df['date'] >= df['date'].max() - pd.DateOffset(months=1)]

    # Calculate min and max values for each variable to dynamically set y-axis ranges
    temp_high_min, temp_high_max = filtered_df['temperature_high'].min(), filtered_df['temperature_high'].max()
    temp_low_min, temp_low_max = filtered_df['temperature_low'].min(), filtered_df['temperature_low'].max()
    humidity_high_min, humidity_high_max = filtered_df['humidity_high'].min(), filtered_df['humidity_high'].max()
    humidity_low_min, humidity_low_max = filtered_df['humidity_low'].min(), filtered_df['humidity_low'].max()
    wind_high_min, wind_high_max = filtered_df['wind_speed_high'].min(), filtered_df['wind_speed_high'].max()
    wind_low_min, wind_low_max = filtered_df['wind_speed_low'].min(), filtered_df['wind_speed_low'].max()

    # Temperature chart with line and bar traces
    trace_temp_high_line = go.Scatter(
        x=filtered_df['date'], y=filtered_df['temperature_high'],
        mode='lines+markers', name='High Temp (Line)',
        hovertemplate='Date: %{x}<br>High Temp: %{y}°C<extra></extra>',
        line=dict(color='firebrick')
    )
    trace_temp_low_line = go.Scatter(
        x=filtered_df['date'], y=filtered_df['temperature_low'],
        mode='lines+markers', name='Low Temp (Line)',
        hovertemplate='Date: %{x}<br>Low Temp: %{y}°C<extra></extra>',
        line=dict(color='royalblue'),
        yaxis='y2'
    )
    trace_temp_high_bar = go.Bar(
        x=filtered_df['date'], y=filtered_df['temperature_high'],
        name='High Temp (Bar)',
        marker=dict(
            color=filtered_df['temperature_high'],
            colorscale='Reds',
            showscale=False
        ),
        opacity=0.6
    )
    trace_temp_low_bar = go.Bar(
        x=filtered_df['date'], y=filtered_df['temperature_low'],
        name='Low Temp (Bar)',
        marker=dict(
            color=filtered_df['temperature_low'],
            colorscale='Blues',
            showscale=False
        ),
        opacity=0.6,
        yaxis='y2'
    )
    temp_layout = go.Layout(
        title=dict(
            text="Temperature Variation",
            font=dict(size=15)  # Adjust title font size if needed
        ),
        yaxis=dict(
            title='High Temp (°C)',
            titlefont=dict(color='firebrick'),
            range=[temp_high_min - 1, temp_high_max + 1]
        ),
        yaxis2=dict(
            title='Low Temp (°C)',
            titlefont=dict(color='royalblue'),
            overlaying='y', side='right',
            range=[temp_low_min - 1, temp_low_max + 1]
        ),
        legend=dict(x=0.72, y=0.98),
        hovermode='x unified',
        barmode='overlay'
    )

    # Humidity chart with line and bar traces
    trace_humidity_high_line = go.Scatter(
        x=filtered_df['date'], y=filtered_df['humidity_high'],
        mode='lines+markers', name='High Humidity (Line)',
        hovertemplate='Date: %{x}<br>High Humidity: %{y}%<extra></extra>',
        line=dict(color='green')
    )
    trace_humidity_low_line = go.Scatter(
        x=filtered_df['date'], y=filtered_df['humidity_low'],
        mode='lines+markers', name='Low Humidity (Line)',
        hovertemplate='Date: %{x}<br>Low Humidity: %{y}%<extra></extra>',
        line=dict(color='blue'),
        yaxis='y2'
    )
    trace_humidity_high_bar = go.Bar(
        x=filtered_df['date'], y=filtered_df['humidity_high'],
        name='High Humidity (Bar)',
        marker=dict(
            color=filtered_df['humidity_high'],
            colorscale='Greens',
            showscale=False
        ),
        opacity=0.6
    )
    trace_humidity_low_bar = go.Bar(
        x=filtered_df['date'], y=filtered_df['humidity_low'],
        name='Low Humidity (Bar)',
        marker=dict(
            color=filtered_df['humidity_low'],
            colorscale='Blues',
            showscale=False  # Disable color bar legend
        ),
        opacity=0.6,
        yaxis='y2'
    )
    humidity_layout = go.Layout(
        title=dict(
            text="Humidity Variation",
            font=dict(size=15)  # Adjust title font size if needed
        ),
        yaxis=dict(
            title='High Humidity (%)',
            titlefont=dict(color='green'),
            range=[humidity_high_min - 1, humidity_high_max + 1]  # Adjust y-axis range dynamically
        ),
        yaxis2=dict(
            title='Low Humidity (%)',
            titlefont=dict(color='blue'),
            overlaying='y', side='right',
            range=[humidity_low_min - 1, humidity_low_max + 1]  # Adjust y2-axis range dynamically
        ),
        legend=dict(x=0.68, y=0.98),
        hovermode='x unified',
        barmode='overlay'
    )

    # Wind Speed chart with line and bar traces
    trace_wind_high_line = go.Scatter(
        x=filtered_df['date'], y=filtered_df['wind_speed_high'],
        mode='lines+markers', name='High Wind Speed (Line)',
        hovertemplate='Date: %{x}<br>High Wind Speed: %{y} km/h<extra></extra>',
        line=dict(color='orange')
    )
    trace_wind_low_line = go.Scatter(
        x=filtered_df['date'], y=filtered_df['wind_speed_low'],
        mode='lines+markers', name='Low Wind Speed (Line)',
        hovertemplate='Date: %{x}<br>Low Wind Speed: %{y} km/h<extra></extra>',
        line=dict(color='purple'),
        yaxis='y2'
    )
    trace_wind_high_bar = go.Bar(
        x=filtered_df['date'], y=filtered_df['wind_speed_high'],
        name='High Wind Speed (Bar)',
        marker=dict(
            color=filtered_df['wind_speed_high'],
            colorscale='Oranges',
            showscale=False  # Disable color bar legend
        ),
        opacity=0.6
    )
    trace_wind_low_bar = go.Bar(
        x=filtered_df['date'], y=filtered_df['wind_speed_low'],
        name='Low Wind Speed (Bar)',
        marker=dict(
            color=filtered_df['wind_speed_low'],
            colorscale='Purples',
            showscale=False  # Disable color bar legend
        ),
        opacity=0.6,
        yaxis='y2'
    )
    wind_layout = go.Layout(
        title=dict(
            text="Wind Speed Variation",
            font=dict(size=15)  # Adjust title font size if needed
        ),
        yaxis=dict(
            title='High Wind Speed (km/h)',
            titlefont=dict(color='orange'),
            range=[wind_high_min - 1, wind_high_max + 1]
        ),
        yaxis2=dict(
            title='Low Wind Speed (km/h)',
            titlefont=dict(color='purple'),
            overlaying='y', side='right',
            range=[wind_low_min - 1, wind_low_max + 1]  
        ),
        legend=dict(x=0.64, y=0.98),
        hovermode='x unified',
        barmode='overlay'
    )

    # Return the figures for the three charts
    return (
        go.Figure(data=[trace_temp_high_line, trace_temp_low_line, trace_temp_high_bar, trace_temp_low_bar], layout=temp_layout),
        go.Figure(data=[trace_humidity_high_line, trace_humidity_low_line, trace_humidity_high_bar, trace_humidity_low_bar], layout=humidity_layout),
        go.Figure(data=[trace_wind_high_line, trace_wind_low_line, trace_wind_high_bar, trace_wind_low_bar], layout=wind_layout)
    )
