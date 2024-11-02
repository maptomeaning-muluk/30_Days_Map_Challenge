import streamlit as st
import folium
import geopandas as gpd
from streamlit_folium import folium_static

st.set_page_config(layout="wide")

# Load the GeoJSON file
geojson_file = r'https://raw.githubusercontent.com/maptomeaning-muluk/30_Days_Map_Challenge/main/2_Line/shapes.geojson'  # Update with your GeoJSON file path
gdf = gpd.read_file(geojson_file)

# Create a base map
map_center = [18.52221821180045, 73.85665638906731]
m = folium.Map(location=map_center, tiles='Cartodb Positron', zoom_start=11)


# Function to add GeoJSON to the map
def add_geojson_to_map(gdf):
    for _, row in gdf.iterrows():
        # Extract attributes
        trip_id = row['Trip_ID']
        trip_name = row['Trip_Name']
        route_color = row['routes_colour']

        # Create a popup with the route details
        popup_html = f"""
            <b>Route Number:</b> {trip_id}<br>
            <b>Route Name:</b> {trip_name}<br>
        """
        popup = folium.Popup(popup_html, max_width=250)

        # Create a GeoJSON feature and add it to the map
        geojson = folium.GeoJson(
            row.geometry,
            style_function=lambda x, color=route_color: {
                'color': f'#{color}',
                'weight': 3,  # Adjust line thickness
                'opacity': 0.7
            },
            popup=popup  # Attach the popup here
        )

        geojson.add_to(m)


# Add the GeoJSON layer to the map
add_geojson_to_map(gdf)

# Create columns in Streamlit with specified ratios to center the map
col1, col2, col3 = st.columns([1, 4, 1])

# Display the map in the central column (col2) to center it
with col2:
    st.title("PMPML Service Area with Bus Routes")
    folium_static(m, height=700, width=1000)
