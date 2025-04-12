import folium
from folium.plugins import MarkerCluster

# Base map
unesco_map = folium.Map(location=[22.9734, 78.6569], zoom_start=5, tiles="CartoDB positron")

# Create a cluster group
marker_cluster = MarkerCluster().add_to(unesco_map)

# UNESCO Sites list: [Name, Latitude, Longitude, Type]
unesco_sites = [
    ["Agra Fort", 27.1795, 78.0211, "Cultural"],
    ["Ajanta Caves", 20.5519, 75.7033, "Cultural"],
    ["Nalanda Mahavihara", 25.1357, 85.4438, "Cultural"],
    ["Buddhist Monuments at Sanchi", 23.4793, 77.7399, "Cultural"],
    ["Kaziranga National Park", 26.5775, 93.1711, "Natural"],
    ["Sundarbans National Park", 21.9497, 89.1833, "Natural"],
    ["Khangchendzonga National Park", 27.6520, 88.3718, "Mixed"],
    ["Humayun's Tomb", 28.5933, 77.2507, "Cultural"],
    ["Qutb Minar", 28.5244, 77.1855, "Cultural"],
    ["Fatehpur Sikri", 27.0937, 77.6600, "Cultural"],
    ["Taj Mahal", 27.1751, 78.0421, "Cultural"],
    ["Mahabodhi Temple", 24.6951, 84.9913, "Cultural"],
    ["Hampi Monuments", 15.3350, 76.4600, "Cultural"],
    ["Ellora Caves", 20.0268, 75.1795, "Cultural"],
    ["Elephanta Caves", 18.9633, 72.9310, "Cultural"],
    ["Chola Temples", 10.7821, 79.1319, "Cultural"],
    ["Jaipur City", 26.9124, 75.7873, "Cultural"],
    ["Western Ghats", 10.3813, 76.1467, "Natural"],
    ["Great Himalayan National Park", 31.7000, 77.3833, "Natural"],
    ["Manas Wildlife Sanctuary", 26.6593, 91.0011, "Natural"],
    ["Keoladeo National Park", 27.1591, 77.5218, "Natural"],
    ["Rani ki Vav", 23.8583, 72.1014, "Cultural"],
    ["Rock Shelters of Bhimbetka", 22.9364, 77.6121, "Cultural"],
    ["Sun Temple, Konark", 19.8876, 86.0948, "Cultural"],
    ["Pattadakal Monuments", 15.9477, 75.8180, "Cultural"],
    ["Victorian Gothic Mumbai", 18.9388, 72.8272, "Cultural"],
    ["Santiniketan", 23.6795, 87.6856, "Cultural"],
    ["Dholavira", 23.8875, 70.2194, "Cultural"],
    ["Ramappa Temple", 18.2341, 79.9429, "Cultural"],
    ["Chhatrapati Shivaji Terminus", 18.9402, 72.8356, "Cultural"],
    ["Churches of Goa", 15.5000, 73.8333, "Cultural"],
    ["Champaner-Pavagadh", 22.4870, 73.5370, "Cultural"],
    ["Ahmedabad City", 23.0225, 72.5714, "Cultural"],
    ["Le Corbusier Buildings", 30.7333, 76.7794, "Cultural"],
    ["Khajuraho", 24.8516, 79.9210, "Cultural"],
    ["Mahabalipuram", 12.6167, 80.1910, "Cultural"],
    ["Jantar Mantar", 26.9246, 75.8235, "Cultural"],
    ["Red Fort", 28.6562, 77.2410, "Cultural"],
    ["Nanda Devi & Valley of Flowers", 30.7280, 79.6050, "Natural"],
    ["Ahom Moidams at Charaideo", 27.0023, 94.9487, "Cultural"],
    ["Sacred Ensembles of the Hoysalas", 12.9116, 76.8979, "Cultural"],
    ["Santiniketan", 23.6795, 87.6856, "Cultural"]
]

# Color code for categories
colors = {
    "Cultural": "darkblue",
    "Natural": "green",
    "Mixed": "orange"
}

# Add each site to the cluster group
for name, lat, lon, category in unesco_sites:
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(f"<b>{name}</b><br>Type: {category}", max_width=250),
        tooltip=name,
        icon=folium.Icon(color=colors.get(category, "blue"), icon="info-sign")
    ).add_to(marker_cluster)

# Save map to Windows path
unesco_map.save("d:/indiannn/lovely/unesco_india_cluster_map.html")
print("✅ Clustered UNESCO Map created successfully.")
