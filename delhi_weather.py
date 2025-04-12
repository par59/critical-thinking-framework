import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_city_weather_data():
    # Current weather data for major Indian cities
    return [
        {
            'city': 'Mumbai',
            'condition': 'Haze',
            'temperature': 29.0,
            'wind_speed': 11.1,
            'wind_direction': 'Southerly',
            'humidity': 80
        },
        {
            'city': 'Bengaluru',
            'condition': 'Mainly Clear Sky',
            'temperature': 25.0,
            'wind_speed': 3.7,
            'wind_direction': 'Northeasterly',
            'humidity': 69
        },
        {
            'city': 'Chennai',
            'condition': 'Partly Cloudy Sky',
            'temperature': 29.2,
            'wind_speed': 7.4,
            'wind_direction': 'Northeasterly',
            'humidity': 74
        },
        {
            'city': 'Hyderabad',
            'condition': 'Haze',
            'temperature': 27.2,
            'wind_speed': 5.6,
            'wind_direction': 'Northwesterly',
            'humidity': 58
        },
        {
            'city': 'Kolkata',
            'condition': 'Haze',
            'temperature': 25.2,
            'wind_speed': 1.9,
            'wind_direction': 'Northeasterly',
            'humidity': 76
        },
        {
            'city': 'Ahmedabad',
            'condition': 'Haze',
            'temperature': 28.4,
            'wind_speed': 3.7,
            'wind_direction': 'Southerly',
            'humidity': 64
        },
        {
            'city': 'Pune',
            'condition': 'Generally Cloudy Sky',
            'temperature': 27.0,
            'wind_speed': 3.7,
            'wind_direction': 'Westerly',
            'humidity': 51
        },
        {
            'city': 'Noida',
            'condition': 'Haze',
            'temperature': 26.8,
            'wind_speed': 5.2,
            'wind_direction': 'East-southeasterly',
            'humidity': 68
        },
        {
            'city': 'Prayagraj',
            'condition': 'Partly Cloudy',
            'temperature': 28.5,
            'wind_speed': 4.2,
            'wind_direction': 'Northwesterly',
            'humidity': 62
        }
    ]

def create_city_weather_dashboard():
    # Get weather data
    data = get_city_weather_data()
    
    # Extract data for plotting
    cities = [d['city'] for d in data]
    temperatures = [d['temperature'] for d in data]
    humidities = [d['humidity'] for d in data]
    wind_speeds = [d['wind_speed'] for d in data]
    conditions = [d['condition'] for d in data]
    wind_directions = [d['wind_direction'] for d in data]

    # Create figure with subplots
    fig = make_subplots(
        rows=2, 
        cols=2,
        subplot_titles=('Temperature (°C)', 'Humidity (%)', 'Wind Speed (km/h)', 'Weather Conditions'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "table"}]],
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )

    # Add temperature trace
    fig.add_trace(
        go.Bar(
            x=cities,
            y=temperatures,
            name='Temperature',
            marker_color='red',
            text=temperatures,
            textposition='auto',
        ),
        row=1, 
        col=1
    )

    # Add humidity trace
    fig.add_trace(
        go.Bar(
            x=cities,
            y=humidities,
            name='Humidity',
            marker_color='skyblue',
            text=humidities,
            textposition='auto',
        ),
        row=1, 
        col=2
    )

    # Add wind speed trace
    fig.add_trace(
        go.Bar(
            x=cities,
            y=wind_speeds,
            name='Wind Speed',
            marker_color='green',
            text=wind_speeds,
            textposition='auto',
        ),
        row=2, 
        col=1
    )

    # Add weather conditions table
    fig.add_trace(
        go.Table(
            header=dict(
                values=['City', 'Condition', 'Wind Direction'],
                fill_color='paleturquoise',
                align='left'
            ),
            cells=dict(
                values=[cities, conditions, wind_directions],
                fill_color='lavender',
                align='left'
            )
        ),
        row=2, 
        col=2
    )

    # Update layout
    fig.update_layout(
        title_text=f'Current Weather Across Major Indian Cities - {datetime.now().strftime("%Y-%m-%d")}',
        title_x=0.5,
        height=1000,
        width=1200,
        showlegend=False,
        template='plotly_white',
        margin=dict(t=100, b=50, l=50, r=50)
    )

    # Update axes
    fig.update_xaxes(tickangle=45)
    
    # Add hover templates
    fig.update_traces(
        hovertemplate="<b>City:</b> %{x}<br>" +
                     "<b>Temperature:</b> %{y:.1f}°C<br>",
        row=1, col=1
    )
    fig.update_traces(
        hovertemplate="<b>City:</b> %{x}<br>" +
                     "<b>Humidity:</b> %{y:.1f}%<br>",
        row=1, col=2
    )
    fig.update_traces(
        hovertemplate="<b>City:</b> %{x}<br>" +
                     "<b>Wind Speed:</b> %{y:.1f} km/h<br>",
        row=2, col=1
    )

    # Save the dashboard as an HTML file
    fig.write_html('indian_cities_weather_dashboard.html')
    print("Interactive weather dashboard for Indian cities has been created successfully! Open indian_cities_weather_dashboard.html in your web browser.")

if __name__ == "__main__":
    create_city_weather_dashboard() 