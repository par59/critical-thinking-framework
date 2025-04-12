import plotly.express as px
import pandas as pd

# Your city data
data = pd.DataFrame({
    'City': ['Delhi', 'Mumbai', 'Kolkata', 'Chennai'],
    'Population': [31800000, 20400000, 15000000, 11300000],
    'Latitude': [28.6139, 19.0760, 22.5726, 13.0827],
    'Longitude': [77.2090, 72.8777, 88.3639, 80.2707],
    'Area (sq km)': [1484, 603, 205, 426],
    'GDP (Billion USD)': [293.6, 368, 150.1, 78.6]
})

# Use new scatter_map instead of scatter_mapbox
fig = px.scatter_map(
    data,
    lat='Latitude',
    lon='Longitude',
    size='Population',
    color='GDP (Billion USD)',
    hover_name='City',
    hover_data={
        'Population': True,
        'Area (sq km)': True,
        'GDP (Billion USD)': True
    },
    size_max=50,
    zoom=4,
    title='Interactive Map of Indian Metro Cities'
)

# Save or show
fig.write_html("interactive_map.html")
fig.show()
