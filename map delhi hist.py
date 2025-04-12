import folium
from folium.plugins import FloatImage

# Define Delhi historical sites
delhi_sites = {
    "Red Fort": ("Lal Qila, Chandni Chowk", (28.6562, 77.2410)),
    "Qutub Minar": ("Mehrauli", (28.5244, 77.1855)),
    "India Gate": ("Rajpath", (28.6129, 77.2295)),
    "Humayun's Tomb": ("Nizamuddin East", (28.5933, 77.2507)),
    "Jama Masjid": ("Old Delhi", (28.6507, 77.2334)),
    "Lotus Temple": ("Kalkaji", (28.5535, 77.2588)),
    "Rashtrapati Bhavan": ("President’s Estate", (28.6143, 77.1990)),
    "Raj Ghat": ("Ring Road", (28.6400, 77.2506)),
    "Jantar Mantar": ("Connaught Place", (28.6272, 77.2166)),
    "Purana Qila": ("Mathura Road", (28.6096, 77.2431)),
}

# Create the map
delhi_map = folium.Map(
    location=[28.6139, 77.2090],
    zoom_start=12,
    tiles="CartoDB positron",  # Clean modern look
    control_scale=True
)

# Add logo or image if desired
# FloatImage('https://upload.wikimedia.org/wikipedia/commons/e/e3/Delhi_Circle_logo.png', bottom=8, left=85).add_to(delhi_map)

# Add markers and styled labels
for name, (description, coords) in delhi_sites.items():
    # Stylish popup
    popup_html = f"""
        <div style='font-family:Segoe UI; font-size:14px; padding:5px;'>
            <b style='font-size:16px;'>{name}</b><br>
            <i>{description}</i>
        </div>
    """
    # Marker with popup
    folium.Marker(
        location=coords,
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.Icon(color='cadetblue', icon='glyphicon-map-marker')
    ).add_to(delhi_map)

    # Visible name next to marker
    folium.Marker(
        location=[coords[0] + 0.002, coords[1] + 0.002],  # Slight offset to prevent overlap
        icon=folium.DivIcon(
            html=f"""
                <div style="
                    font-size: 13px;
                    font-family: 'Segoe UI', sans-serif;
                    background-color: white;
                    padding: 2px 6px;
                    border-radius: 6px;
                    box-shadow: 1px 1px 4px rgba(0,0,0,0.3);
                    color: #212121;
                    font-weight: 500;
                    ">
                    {name}
                </div>
            """
        )
    ).add_to(delhi_map)

# Save the map
delhi_map.save("delhi_historical_sites_clean_ui_map.html")
print("✅ Final polished map created as 'delhi_historical_sites_clean_ui_map.html'")
