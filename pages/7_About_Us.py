import streamlit as st
import base64
import os

# Add a "Back to Menu" link
#st.page_link("Main.py", label="Back to Menu", icon="🏠")
st.markdown('<a href="/Main" target="_self">🏠 Main Page</a>', unsafe_allow_html=True)

st.sidebar.title("About us")


def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def main():

    # Get the base64 string of the images
    image_path = "images/Pradeep-photo.jpg"  # Adjust this path as needed
    img_base64 = get_image_base64(image_path)
    image1_path = "images/Abhijit-photo.jpg"
    img1_base64 = get_image_base64(image1_path)

    # Add a smaller dark grey banner at the top
    st.markdown("""
        <div style="background-color: #333333; color: white; text-align: center; padding: 0.8px; border-radius: 10px;">
            <h1 style="margin: 0; font-size: 24px; line-height: 1.2;">Welcome to Our AI Solutions</h1>
            <p style="margin: 1px 0; line-height: 1.2;">Explore our innovative tools and resources</p>
        </div>
        <br>  <!-- Line break for spacing -->
    """, unsafe_allow_html=True)    

    # Create two columns
    col1, col2 = st.columns(2)

    # Set a fixed height for the boxes
    box_height = "400px"

    # Card 1

    with col1:
        st.markdown(f"""
            <a href="https://www.linkedin.com/in/pradeep-krishnarao/" target="_blank" style="text-decoration: none; color: inherit;">
                <div style="border: 1px grey; padding: 20px; border-radius: 10px; height: {box_height}; display: flex; flex-direction: column; justify-content: space-between; overflow: hidden; cursor: pointer; background-color: #f0f0f0;">
                    <div style="display: flex; justify-content: center; align-items: center; height: 300px; overflow: hidden;">
                        <img src="data:image/jpeg;base64,{img_base64}" alt="Pradeep Photo" style="max-width: 80%; max-height: 80%; object-fit: contain;">
                    </div>
                    <div style="padding: 15px;">
                        <h3 style="margin: 10px 0;">Lead AI Safety & Responsible AI</h3>
                    </div>
                </div>
                <p style="margin-bottom: 10px;">Global Technology lead specialising in AI Ethics and Responsible AI.</p>
            </a>
        """, unsafe_allow_html=True)


    # Card 2
    with col2:
        st.markdown(f"""
            <a href="https://www.linkedin.com/in/abhibang/" target="_blank" style="text-decoration: none; color: inherit;">                                                            
            <div style="border: 1px grey; padding: 20px; border-radius: 10px; height: {box_height}; display: flex; flex-direction: column; justify-content: space-between; overflow: hidden; cursor: pointer; background-color: #f0f0f0;">
                <div style="display: flex; justify-content: center; align-items: center; height: 300px; overflow: hidden;">
                    <img src="data:image/jpeg;base64,{img1_base64}" alt="Abhijit Photo" style="max-width: 80%; max-height: 80%; object-fit: contain;">
                </div>
                <div style="padding: 15px;">
                    <h3 style="margin: 10px 0;">Lead AI Governance and Risk</h3>
                </div>
            </div>
            <p style="margin-bottom: 10px;">Global AI leader with expertise in Banking, AI Governance and Adoption.</p> 
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()