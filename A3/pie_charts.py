# pie_charts.py
import pandas as pd
import plotly.graph_objs as go
import plotly.colors as pc

def create_pie_charts(df):
    # Filter data for the last 30 days
    filtered_df = df[df['date'] >= df['date'].max() - pd.Timedelta(days=30)]
    
    # Forecast Type Pie Chart: Count occurrences of each forecast type
    forecast_counts = filtered_df['forecast'].value_counts()
    
    # Generate colors dynamically based on the number of forecast types
    forecast_colors = pc.qualitative.Plotly[:len(forecast_counts)] if len(forecast_counts) <= len(pc.qualitative.Plotly) \
                      else pc.sample_colorscale('Viridis', len(forecast_counts))

    # Create Pie Chart for Forecast Types
    forecast_pie = go.Figure(
        data=[go.Pie(
            labels=forecast_counts.index,
            values=forecast_counts.values,
            hoverinfo='label+percent+value',
            textinfo='label+percent',
            marker=dict(
                colors=forecast_colors,
                line=dict(color='#FFFFFF', width=2)
            )
        )]
    )
    forecast_pie.update_layout(
        title="Forecast Types in the Last 30 Days",
        legend=dict(font=dict(size=10))
    )

    # Wind Direction Pie Chart: Count occurrences of each wind direction
    wind_direction_counts = filtered_df['wind_direction'].value_counts()

    # Generate colors dynamically based on the number of wind directions
    wind_direction_colors = pc.qualitative.Plotly[:len(wind_direction_counts)] if len(wind_direction_counts) <= len(pc.qualitative.Plotly) \
                            else pc.sample_colorscale('Viridis', len(wind_direction_counts))

    # Create Pie Chart for Wind Directions
    wind_direction_pie = go.Figure(
        data=[go.Pie(
            labels=wind_direction_counts.index,
            values=wind_direction_counts.values,
            hoverinfo='label+percent+value',
            textinfo='label+percent',
            marker=dict(
                colors=wind_direction_colors,
                line=dict(color='#FFFFFF', width=2)
            )
        )]
    )
    wind_direction_pie.update_layout(
        title="Wind Directions in the Last 30 Days",
        legend=dict(font=dict(size=10))
    )

    # Return the two pie chart figures
    return forecast_pie, wind_direction_pie
