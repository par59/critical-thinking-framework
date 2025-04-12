import folium

# Jyotirlingas: Name, City, Coordinates
jyotirlingas = {
    "Somnath": ("Veraval, Gujarat", (20.8880, 70.4012)),
    "Mallikarjuna": ("Srisailam, Andhra Pradesh", (16.5745, 78.9461)),
    "Mahakaleshwar": ("Ujjain, Madhya Pradesh", (23.1765, 75.7864)),
    "Omkareshwar": ("Khandwa, Madhya Pradesh", (22.2426, 76.1511)),
    "Kedarnath": ("Rudraprayag, Uttarakhand", (30.7346, 79.0669)),
    "Bhimashankar": ("Pune, Maharashtra", (19.0710, 73.5538)),
    "Kashi Vishwanath": ("Varanasi, Uttar Pradesh", (25.3109, 83.0106)),
    "Trimbakeshwar": ("Nashik, Maharashtra", (19.9406, 73.5302)),
    "Vaidyanath": ("Deoghar, Jharkhand", (24.4551, 86.6974)),
    "Nageshwar": ("Dwarka, Gujarat", (22.2410, 69.0995)),
    "Ramanathaswamy": ("Rameswaram, Tamil Nadu", (9.2881, 79.3174)),
    "Grishneshwar": ("Aurangabad, Maharashtra", (19.8819, 75.1793))
}

# Create the map
jyoti_map = folium.Map(location=[22.5, 78.5], zoom_start=5.2, width="100%", height="85%")

# Add clean markers with modern location icons and styled text
for name, (city, coords) in jyotirlingas.items():
    label_html = f"""
        <div style="
            font-size: 12px;
            font-family: Arial, sans-serif;
            font-weight: 600;
            color: white;
            background-color: #007B5E;
            padding: 6px 10px;
            border-radius: 10px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.25);
            text-align: center;
            white-space: nowrap;
        ">
            <span style="font-size: 14px;">📌</span> {name}<br>
            <span style="font-weight: 400; font-size: 11px;">{city}</span>
        </div>
    """
    folium.Marker(
        location=coords,
        icon=folium.DivIcon(html=label_html),
        tooltip=f"{name} - {city}"
    ).add_to(jyoti_map)

# Save the map
jyoti_map.save("jyotirlinga_map_india.html")
print("✅ Map updated with clean icons and formatted text!")
