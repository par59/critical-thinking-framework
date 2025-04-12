import folium

# Data for the 8 Union Territories of India
union_territories = [
    {"name": "Andaman and Nicobar Islands", "capital": "Port Blair", "latitude": 11.7401, "longitude": 92.6586, "description": "A group of over 500 islands located in the Bay of Bengal."},
    {"name": "Chandigarh", "capital": "Chandigarh", "latitude": 30.7333, "longitude": 76.7794, "description": "A Union Territory and the capital of Haryana and Punjab."},
    {"name": "Dadra and Nagar Haveli and Daman and Diu", "capital": "Daman", "latitude": 20.3974, "longitude": 72.8323, "description": "A coastal Union Territory formed by merging Dadra and Nagar Haveli with Daman and Diu."},
    {"name": "Lakshadweep", "capital": "Kavaratti", "latitude": 10.5625, "longitude": 72.6326, "description": "A group of islands in the Arabian Sea, off the southwestern coast of India."},
    {"name": "Delhi", "capital": "New Delhi", "latitude": 28.6139, "longitude": 77.2090, "description": "The capital city of India and the seat of the Indian government."},
    {"name": "Puducherry", "capital": "Puducherry", "latitude": 11.9416, "longitude": 79.8083, "description": "A coastal Union Territory with a French colonial heritage."},
    {"name": "Ladakh", "capital": "Leh", "latitude": 34.1526, "longitude": 77.5770, "description": "A northernmost region bordered by China and Pakistan, comprising the Leh and Kargil districts."},
    {"name": "Jammu & Kashmir", "capital": "Srinagar (summer), Jammu (winter)", "latitude": 33.7782, "longitude": 76.5762, "description": "A disputed region, now a Union Territory, with Srinagar as the summer capital and Jammu as the winter capital."}
]

# Initialize the map centered around India
india_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

# Add markers for each Union Territory
for ut in union_territories:
    popup_content = f"<b>{ut['name']}</b><br>Capital: {ut['capital']}<br>{ut['description']}"
    folium.Marker(
        location=[ut['latitude'], ut['longitude']],
        popup=popup_content,
        icon=folium.Icon(color='green', icon='info-sign')
    ).add_to(india_map)

# Save map to an HTML file
india_map.save("india_union_territories_map.html")

# Automatically open the map in a web browser
import webbrowser
webbrowser.open("india_union_territories_map.html")
