# streamgraph.py
import pandas as pd
import plotly.graph_objects as go

def create_streamgraph(df):
    # Filter dataset to only the last 30 days
    max_date = df['date'].max()
    filtered_df = df[df['date'] >= (max_date - pd.DateOffset(days=60))]

    # Calculate average values grouped by forecast type
    avg_df = filtered_df.groupby('forecast').agg({
        'humidity_high': 'mean',
        'humidity_low': 'mean',
        'wind_speed_high': 'mean',
        'wind_speed_low': 'mean'
    }).reset_index()

    # Ensure there are enough data points for plotting
    if avg_df.shape[0] == 1:
        avg_df = pd.concat([avg_df, avg_df])  # Duplicate row if only one forecast type

    # Create figure with dual y-axes
    fig = go.Figure()

    # Add traces for humidity (left y-axis)
    fig.add_trace(go.Scatter(
        x=avg_df['forecast'],
        y=avg_df['humidity_high'],
        mode='lines+markers',
        name='Humidity High',
        line=dict(shape='spline', width=2),
        yaxis='y1'
    ))

    fig.add_trace(go.Scatter(
        x=avg_df['forecast'],
        y=avg_df['humidity_low'],
        mode='lines+markers',
        name='Humidity Low',
        line=dict(shape='spline', width=2, dash='dash'),
        yaxis='y1'
    ))

    # Add traces for wind speed (right y-axis)
    fig.add_trace(go.Scatter(
        x=avg_df['forecast'],
        y=avg_df['wind_speed_high'],
        mode='lines+markers',
        name='Wind Speed High',
        line=dict(shape='spline', width=2),
        yaxis='y2'
    ))

    fig.add_trace(go.Scatter(
        x=avg_df['forecast'],
        y=avg_df['wind_speed_low'],
        mode='lines+markers',
        name='Wind Speed Low',
        line=dict(shape='spline', width=2, dash='dash'),
        yaxis='y2'
    ))

    # Configure layout with dual y-axes and smaller height
    fig.update_layout(
        title="Average Humidity and Wind Speed by Forecast Type for Past 60 Days",
        xaxis_title="Forecast Type",
        yaxis=dict(
            title="Average Humidity",
            color="black"
        ),
        yaxis2=dict(
            title="Average Wind Speed",
            color="black",
            overlaying='y',
            side='right'
        ),
        height=300,  # Reduced height
        legend_title_text='Metrics',
        legend=dict(x=1.1,y=1),
        font=dict(size=10),
        hovermode="x unified"
    )

    # Return the figure
    return fig
