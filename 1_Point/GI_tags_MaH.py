import streamlit as st
import pandas as pd
import geopandas as gpd
import folium as fl
from streamlit_folium import folium_static
import matplotlib.pyplot as plt


# Set the page configuration to wide layout
st.set_page_config(layout="wide")

# Load the GeoJSON files (ensure CRS is set to EPSG:4326 for folium compatibility)
try:
    State_Layer = gpd.read_file(r"https://raw.githubusercontent.com/maptomeaning-muluk/30_Days_Map_Challenge/main/1_Point/Maharashtra.geojson").to_crs("EPSG:4326")
    GI_tag_Layer= gpd.read_file(r"https://raw.githubusercontent.com/maptomeaning-muluk/30_Days_Map_Challenge/main/1_Point/GI_tags_MH.geojson").to_crs("EPSG:4326")

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
    st.write("A geographical indication (GI) is a sign used on products that have a specific geographical origin and possess qualities or a reputation that are due to that origin. In order to function as a GI, a sign must identify a product as originating in a given place.")
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

    categories = GI_tag_Layer[['GI_Tag_Name', 'Category']].drop_duplicates()
    category_counts = categories['Category'].value_counts()

    # Define colors for each category
    color_map = {
        'Agriculture': 'green',
        'Handicraft': 'orange',
        'Manufacturing': 'purple'
    }
    colors = [color_map[category] for category in category_counts.index]

    # Plotting the pie chart with a black background
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('black')  # Set figure background to black
    ax.pie(
        category_counts,
        labels=category_counts.index,
        autopct='%1.1f%%',  # Display percentage
        startangle=90,  # Start angle for better layout
        colors=colors,  # Apply the defined colors
        wedgeprops={'edgecolor': 'black'}  # Edge color for visibility
    )
    ax.set_title("Distribution of GI Tags by Category", color='white')  # Set title color to white

    # Change the color of the labels to white
    for text in ax.texts:
        text.set_color('white')

    st.pyplot(fig)  # Display the pie chart in Streamlit

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

