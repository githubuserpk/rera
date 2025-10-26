import streamlit as st
import os

# Define your versions and image paths
versions = {
    "v0.0": ["images/v0.0/vh0-conceptual.jpg"],
    "v3.0": ["images/v3.0/vh3-safety.jpg", "images/v3.0/vh3.jpg", "images/v3.0/vh3-aboutus.jpg", "images/v3.0/vh3-assessmentform.jpg"],
    "v4.0": ["images/v4.0/s1.jpg", "images/v4.0/s2.jpg"],
    "v10": ["images/v10/vh10-main_page.jpg"],
}

# Create a dropdown for users to select the version
selected_version = st.sidebar.selectbox("Select Version", list(versions.keys()))

# Display images for the selected version
st.title(f"Version {selected_version} Screenshots")

if versions[selected_version]:  # Check if there are images
    for image_path in versions[selected_version]:
        if os.path.exists(image_path):  # Check if the image file exists
            try:
                #st.image(image_path, caption=os.path.basename(image_path), use_container_width=True)
                st.image(image_path, caption=os.path.basename(image_path), width=600)               
                st.markdown(f'<style>.stImage img{{border: 2px solid black;}}</style>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error opening '{image_path}': {str(e)}")
        else:
            st.write("No images found for this version.")
else:
    st.write("No images found.")
