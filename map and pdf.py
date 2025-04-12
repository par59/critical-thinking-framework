# to map delhi historical places  
import folium
from folium.plugins import MarkerCluster

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

# Create base map
jyoti_map = folium.Map(location=[22.5, 78.5], zoom_start=5.2, tiles="OpenStreetMap", width="100%", height="90%")

marker_cluster = MarkerCluster().add_to(jyoti_map)

for name, (city, coords) in jyotirlingas.items():
    popup_html = f"""
    <div style="font-family:'Segoe UI'; font-size:14px">
        <b>{name}</b><br>{city}
    </div>
    """
    folium.Marker(
        location=coords,
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=f"{name} ({city})",
        icon=folium.Icon(color="darkred", icon="glyphicon-map-marker")
    ).add_to(marker_cluster)

jyoti_map.save("change _jyotirlinga_map.html")
print("✅ Clean map with labels and no overlap created: 'change_jyotirlinga_map.html'")
