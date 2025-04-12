import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import pandas as pd

# Data for top wheat-producing states
wheat_data = [
    ["Uttar Pradesh", 26.8467, 80.9462, 30.0],
    ["Punjab", 31.1471, 75.3412, 18.5],
    ["Haryana", 29.0588, 76.0856, 12.0],
    ["Madhya Pradesh", 23.2599, 77.4126, 11.0],
    ["Rajasthan", 26.9124, 75.7873, 9.0]
]

# Convert to DataFrame
df = pd.DataFrame(wheat_data, columns=["State", "Latitude", "Longitude", "Production (MT)"])

# ---------------- STREAMLIT UI ----------------
st.set_page_config(layout="wide", page_title="India Wheat Production Dashboard")

st.title("🌾 India Wheat Production Dashboard")
st.markdown("This dashboard displays the top 5 wheat-producing states in India with production data and geolocation.")

# Summary stats
total_production = df["Production (MT)"].sum()
top_state = df.loc[df["Production (MT)"].idxmax(), "State"]

st.subheader("🔢 Summary")
col1, col2 = st.columns(2)
col1.metric("Total Wheat Production", f"{total_production} million tons")
col2.metric("Top Producing State", top_state)

# Show data table
st.subheader("📋 Data Table")
st.dataframe(df, use_container_width=True)

# Map
st.subheader("🗺️ Cluster Map of Top Wheat-Producing States")
wheat_map = folium.Map(location=[23.0, 79.0], zoom_start=5, tiles="CartoDB positron")
marker_cluster = MarkerCluster().add_to(wheat_map)

for state, lat, lon, production in wheat_data:
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(f"<b>{state}</b><br>Production: {production} MT", max_width=250),
        tooltip=state,
        icon=folium.Icon(color="green", icon="leaf")
    ).add_to(marker_cluster)

folium_static(wheat_map)
