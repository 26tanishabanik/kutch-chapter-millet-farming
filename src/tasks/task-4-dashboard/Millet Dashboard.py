import streamlit as st
import folium
import json
import geojson
from streamlit_folium import st_folium
from folium.plugins import Draw
import model # the script to make prediction

# Set the page layout to wide
st.set_page_config(layout="wide")

st.title("Best Millet For your Location")

st.write("""Draw a polygon on the following map for your area of interest.
            We will try to recommend the type of millet that is most suited for that location.""")

# Create a folium map object
m = folium.Map(location=[26, 85], zoom_start=12)

# Add a draw tool to the map
draw = Draw(
    draw_options={
        "polyline": False,
        "polygon": False, # Enable polygon drawing
        "circle": False,
        "circlemarker": False,
        "marker": False,
    },
    edit_options={"edit": True},
)
draw.add_to(m)

# Display the map in streamlit using st_folium with custom width and height
output = st_folium(m, width=1000, height=600)

# Get the draw data from streamlit
st.session_state.draw = output

# If there is draw data, extract the coordinates of the polygon
if output["all_drawings"] is not None:
    coords = output["last_active_drawing"]["geometry"]["coordinates"]
    
    # Convert to geojson
    geojson_obj = geojson.Polygon([coords])
    
    # Pass the geojson to the function to run prediction 
    model_result = model.run(geojson_obj)
    message = f"The best millet type for your location is : {model_result}."

if (not output["all_drawings"]) or (output["all_drawings"] is None): # If there is no draw data, reset the message
    message = "Please, draw your area of interest on the map above."

st.markdown(message)