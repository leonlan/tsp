import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("🗺️ Map")

df = st.session_state.orders_df

center_lat = 52.1326
center_lon = 5.2913
zoom_start = 7
width = 400
height = 420
point_radius = 0.1
point_color = "red"
line_color = "blue"
line_weight = 2

fmap = folium.Map(
    location=[df["Latitude"].mean(), df["Longitude"].mean()],
    zoom_start=zoom_start,
    tiles="Cartodb positron",
    width=width,
    height=height,
)

for _, row in df.iterrows():
    popup = f"{row['Name']}" if "Name" in df.columns else None
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=point_radius,
        popup=popup,
        color=point_color,
        fill=True,
        fill_color=point_color,
        fill_opacity=0,
    ).add_to(fmap)

if "tour" in st.session_state:
    tour = st.session_state.tour
    coordinates = []
    for idx in tour:
        row = df.iloc[idx]
        coordinates.append([row["Latitude"], row["Longitude"]])

    if tour[0] != tour[-1]:
        coordinates.append(coordinates[0])

    folium.PolyLine(
        locations=coordinates,
        color="blue",
        weight=2,
        opacity=0.7,
    ).add_to(fmap)

st_folium(fmap, width=700, height=500)
