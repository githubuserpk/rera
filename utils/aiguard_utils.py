import streamlit as st
import requests
import json

import base64
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry



def get_retry_session(total_retries=3, backoff_factor=1, status_forcelist=None):
    """
    Creates and returns a requests session with retry logic.
    
    Args:
        total_retries (int): Total number of retries.
        backoff_factor (float): Backoff factor for retries.
        status_forcelist (list): HTTP status codes to trigger a retry.

    Returns:
        requests.Session: Configured session with retry logic.
    """
    if status_forcelist is None:
        status_forcelist = [500, 502, 503, 504]
    
    retries = Retry(
        total=total_retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist
    )
    session = requests.Session()
    session.mount("http://", HTTPAdapter(max_retries=retries))
    return session



def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
    

def get_ai_response(query):

    if query and query != "Custom":
        session = get_retry_session()
        with st.spinner("Searching and generating response..."):
            try:
                # Make the API call to your Flask application
                response = session.post('http://127.0.0.1:5000/search', json={'query': query})
                
                # Parse the JSON response
                data = json.loads(response.text)
                
                # Extract the text content
                result = data['response']
                return result  # Return the result
            except requests.exceptions.RequestException as ex:
                st.error("Service is temporarily unavailable. Please try again later.")                
                return f"Error: {str(ex)}"  # Return an error message
    else:
        return "Please provide a valid query."  # Return a message for invalid queries




def get_recommendation(query):
    if query and query != "Custom":
        session = get_retry_session()
        with st.spinner("Searching and generating response..."):
            try:
                # Make the API call to your Flask application
                response = session.post('http://127.0.0.1:5000/recommendation', json={'query': query})
                
                # Parse the JSON response
                data = json.loads(response.text)
                
                # Extract the text content
                result = data['response']
                return result  # Return the result
            except requests.exceptions.RequestException as ex:
                st.error("Service is temporarily unavailable. Please try again later.")                
                return f"Error: {str(ex)}"  # Return an error message
    else:
        return "Please provide a valid query."  # Return a message for invalid queries