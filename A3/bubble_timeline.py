# bubble_timeline.py
import pandas as pd
import plotly.express as px

def create_bubble_timeline(df, time_range):
    # Get the most recent date in the dataset for filtering
    max_date = df['date'].max()
    
    # Filter the dataset based on the selected time range
    if time_range == 'week':
        filtered_df = df[df['date'] >= (max_date - pd.Timedelta(weeks=1))]
    elif time_range == 'month':
        filtered_df = df[df['date'] >= (max_date - pd.DateOffset(months=1))]
    elif time_range == 'year':
        filtered_df = df[df['date'] >= (max_date - pd.DateOffset(years=1))]
    else:
        filtered_df = df  # Use the full dataset by default

    # Calculate the average PM2.5 across all regions per day
    filtered_df['avg_pm25'] = filtered_df[['pm25_east', 'pm25_west', 'pm25_north', 'pm25_south', 'pm25_central']].mean(axis=1)

    # Create the bubble timeline
    fig = px.scatter(
        filtered_df,
        x='date',
        y='forecast',
        size='avg_pm25',  # Bubble size represents average PM2.5
        color='forecast',  # Color by forecast type
        hover_data={
            'date': True,
            'avg_pm25': ':.2f',  # Show average PM2.5 to 2 decimal places
            'forecast': True
        },
        title="Daily PM2.5 Levels by Region",
        size_max=40
    )

    # Configure layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Region",
        height=800,
        width=1400,
        hovermode="closest"
    )

    # Return the configured figure
    return fig
