import streamlit as st
import requests
import json

from utils import aiguard_utils

# Add a "Back to Menu" link
#st.page_link("Main.py", label="Back to Menu", icon="🏠")
#st.markdown('<a href="http://localhost:8501/Main" target="_self">🏠 Main Page</a>', unsafe_allow_html=True)
st.markdown('<a href="/Main" target="_self">🏠 Main Page</a>', unsafe_allow_html=True)

st.sidebar.title("EU AI Act Advaned Search Engine")
st.title("EU AI Act Advanced Search Engine")

# def get_ai_response(query):
#     if query and query != "Custom":
#         with st.spinner("Searching and generating response..."):
#             try:
#                 # Make the API call to your Flask application
#                 response = requests.post('http://127.0.0.1:5000/search', json={'query': query})
                
#                 # Parse the JSON response
#                 data = json.loads(response.text)
                
#                 # Extract the text content
#                 result = data['response']
#                 return result  # Return the result
#             except requests.exceptions.RequestException as ex:
#                 st.error("Service is temporarily unavailable. Please try again later.")                
#                 return f"Error: {str(ex)}"  # Return an error message
#     else:
#         return "Please provide a valid query."  # Return a message for invalid queries
                

def main():
    try:

        # Top 5 questions
        top_questions = [
            "Who is a Provider?",
            "What is difference between AI Model and AI System?",            
            "What is AI Literacy, which article talks about it?",
            "What are High Risk AI Systems?",
            "What are Prohibited AI Systems ? When is it coming into effect?",
            "Which Articles talk about the Transparency Obligations?",
            "What are the responsibilities of AI Office?"
        ]

        # Create a dropdown for top questions with an option for custom input
        selected_option = st.selectbox(
            "Select a question or choose 'Custom' to type your own:",
            ["Custom"] + top_questions,
            index=0,
            key="question_select"
        )

        # If 'Custom' is selected, show a text input field
        if selected_option == "Custom":
            query = st.text_input("Type your question here:", key="custom_question", placeholder="Enter your question...")
        else:
            query = selected_option

        if st.button("Submit"):
            # Invoke ai api to get response
            result = aiguard_utils.get_ai_response(query)

            # Display response 
            if result:  # Check if result is not None or empty
                st.text_area("Answer:", value=result, height=300, disabled=True)
            else:
                st.error("No response received.")
            
            # if query and query != "Custom":
            #     with st.spinner("Searching and generating response..."):
            #         try:
            #             # Make the API call to your Flask application
            #             response = requests.post('http://127.0.0.1:5000/search', json={'query': query})
                        
            #             # Parse the JSON response
            #             data = json.loads(response.text)
                        
            #             # Extract the text content
            #             result = data['response']
                        
            #             # Display the text to the user
            #             st.text_area("Answer:", value=result, height=300, disabled=True)
            #         except requests.exceptions.RequestException:
            #             st.error("Service is temporarily unavailable. Please try again later.")
            # else:
            #     st.warning("Please select a question or enter your own.")


    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()


