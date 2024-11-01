# import streamlit as st
# import pandas as pd
# import geopandas as gpd
# import folium as fl
# from streamlit_folium import folium_static
# import json
#
# # Load the GeoJSON files (ensure CRS is set to EPSG:4326 for folium compatibility)
# try:
#     State_Layer = gpd.read_file(r"D:\30_days_Map_Challenge\1_Point\Maharashtra.geojson").to_crs("EPSG:4326")
#     GI_tag_Layer= gpd.read_file(r"D:\30_days_Map_Challenge\1_Point\GI_tags_MH_Final.geojson").to_crs("EPSG:4326")
#
# except Exception as e:
#     st.error(f"Error loading files: {e}")
#
#
#
# st.title("GI Tags in Maharashtra")
# st.write("Click on a point on the map to view details about each GI Tag.")
#
#
# # Calculate the centroid for the map center
# centroid = State_Layer.geometry.centroid.iloc[0]
# map_center = [centroid.y, centroid.x]
#
# # Initialize the map
# Map = fl.Map(location=map_center, tiles='Cartodb Positron', zoom_start=7)
#
# # Add state boundary layer with styling
# state_style_function = lambda x: {
#     'fillColor': '#3186cc',
#     'color': 'black',
#     'fillOpacity': 0.0,
#     'weight': 1
# }
# fl.GeoJson(State_Layer, style_function=state_style_function).add_to(Map)
#
# # Define colors for each category
# category_colors = {
#     'Handicraft': 'darkorange',
#     'Manufacturing': 'purple',
#     'Agriculture': 'green'
# }
#
# # Add GI Tag points as CircleMarkers with categorized colors and labels
# for _, row in GI_tag_Layer.iterrows():
#     category = row["Category"]
#     color = category_colors.get(category, 'blue')  # default to blue if category not found
#
#     # Popup content
#     popup_html = f"""
#     <b>GI Tag Name:</b> {row["GI_Tag_Name"]}<br>
#     <b>Place Name:</b> {row["Place Name"]}<br>
#     <b>Category:</b> {category}<br>
#     <b>Information:</b> {row["Information"]}
#     """
#
#     # Add CircleMarker with specific color for the category and tooltip
#     marker = fl.CircleMarker(
#         location=[row.geometry.y, row.geometry.x],
#         radius=6,
#         color=color,
#         fill=True,
#         fill_color=color,
#         fill_opacity=0.7,
#         popup=fl.Popup(popup_html, max_width=250),
#         tooltip=row["GI_Tag_Name"]  # Add label from GI_Tag_Name
#     )
#     marker.add_to(Map)
#
# # unique_counts = GI_tag_Layer['GI_Tag_Name'].drop_duplicates()
# # unique_counts = len(unique_counts)
# # st.write(unique_counts)
#
# unique_counts = GI_tag_Layer['GI_Tag_Name'].nunique()  # Directly get the unique count
# st.metric(label="Number of GI Tags", value=unique_counts)
#
# # Display map
# folium_static(Map, height=700, width=1000)

import streamlit as st
import pandas as pd
import geopandas as gpd
import folium as fl
from streamlit_folium import folium_static
import json

# Set the page configuration to wide layout
st.set_page_config(layout="wide")

# Load the GeoJSON files (ensure CRS is set to EPSG:4326 for folium compatibility)
try:
    State_Layer = gpd.read_file(r"D:\30_days_Map_Challenge\1_Point\Maharashtra.geojson").to_crs("EPSG:4326")
    GI_tag_Layer= gpd.read_file(r"D:\30_days_Map_Challenge\1_Point\GI_tags_MH_Final.geojson").to_crs("EPSG:4326")

except Exception as e:
    st.error(f"Error loading files: {e}")

# Set up page title
st.title("GI Tags in Maharashtra")
# st.write("Click on a point on the map to view details about each GI Tag.")

# Calculate the centroid for the map center
centroid = State_Layer.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Set up columns for layout
col1, col2 = st.columns([1, 3])  # 1/3 for col1, 2/3 for col2

with col1:
    # Display the metric with larger text using HTML/CSS
    unique_counts = GI_tag_Layer['GI_Tag_Name'].nunique()
    st.markdown(
        f"""
        <div style="font-size:30px; font-weight:bold; margin-top:20px;">
            Number of GI Tags: <span style="color:#3186cc;">{unique_counts}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    # Initialize the map
    Map = fl.Map(location=map_center, tiles='Cartodb Positron', zoom_start=7)

    # Add state boundary layer with styling
    state_style_function = lambda x: {
        'fillColor': '#3186cc',
        'color': 'black',
        'fillOpacity': 0.0,
        'weight': 1
    }
    fl.GeoJson(State_Layer, style_function=state_style_function).add_to(Map)

    # Define colors for each category
    category_colors = {
        'Handicraft': 'darkorange',
        'Manufacturing': 'purple',
        'Agriculture': 'green'
    }

    # Add GI Tag points as CircleMarkers with categorized colors and labels
    for _, row in GI_tag_Layer.iterrows():
        category = row["Category"]
        color = category_colors.get(category, 'blue')  # default to blue if category not found

        # Popup content
        popup_html = f"""
        <b>GI Tag Name:</b> {row["GI_Tag_Name"]}<br>
        <b>Place Name:</b> {row["Place Name"]}<br>
        <b>Category:</b> {category}<br>
        <b>Information:</b> {row["Information"]}
        """

        # Add CircleMarker with specific color for the category and tooltip
        marker = fl.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=fl.Popup(popup_html, max_width=250),
            tooltip=row["GI_Tag_Name"]
        )
        marker.add_to(Map)

    # Display map
    folium_static(Map, height=600, width=1200)

