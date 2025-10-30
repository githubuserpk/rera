import streamlit as st
import mammoth
import os

# Add a "Back to Menu" link
#st.page_link("Main.py", label="Back to Menu", icon="🏠")
st.markdown('<a href="/Main" target="_self">🏠 Main Page</a>', unsafe_allow_html=True)


st.title("AI Adoption ")
# Add your settings content here
st.sidebar.title("AI Governance ")



def display_document():
    # Specify the full path to the Word document
    document_path = "Documents/RERA_REGULATIONS_2022.pdf"    

    if os.path.exists(document_path):

        with open(document_path, "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html = result.value
        
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.error(f"Specified content not found {document_path}")



if __name__ == "__main__":
    if 'slide_index' not in st.session_state:
        st.session_state.slide_index = 0
    display_document()  
