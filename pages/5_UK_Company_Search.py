import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
import os
import csv
from io import StringIO

# company house rest api schema for the json output
# https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/resources/companyprofile?v=latest

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# Get API key from environment variable
API_KEY_LIVE = os.getenv('API_KEY_LIVE')



def fetch_sic_codes():
    url = "https://assets.publishing.service.gov.uk/media/5a7f8639e5274a2e87db65e1/SIC07_CH_condensed_list_en.csv"
    response = requests.get(url)
    csv_content = StringIO(response.text)
    
    sic_dict = {}
    csv_reader = csv.reader(csv_content)
    next(csv_reader)  # Skip header row
    
    for row in csv_reader:
        if len(row) >= 2:
            sic_code = row[0].strip()
            description = row[1].strip()
            sic_dict[sic_code] = description
    
    return sic_dict

def get_sic_description(sic_code, sic_dict):
    return sic_dict.get(sic_code, "SIC code not found")



# Streamlit application title
st.title("UK Companies House Company Search")

# Input: Company Number

# Top 5 questions
company_numbers = [
    "07991498", # MED-CREW, SIC: 46180, 85590, 86210, 86220
    "09134006", # IBU
    "00102498", # BP
    "03137479", # Vodafone UK
]

# Create a dropdown for top questions with an option for custom input
selected_option = st.selectbox(
    "Select a question or choose 'Custom' to type your own:",
    ["Custom"] + company_numbers,
    index=0,
    key="question_select"
)


# If 'Custom' is selected, show a text input field
if selected_option == "Custom":
    company_number = st.text_input("Type your question here:", key="custom_question", placeholder="Enter your company number...")
else:
    company_number = selected_option


# Button to trigger the search
if st.button("Search"):
    if company_number:
        # Construct the API URL
        BASE_URL = st.secrets["BASE_URL_COMPANY_SEARCH"]
        #BASE_URL_FMT = f"https://api.company-information.service.gov.uk/company/{company_number}"
        url = BASE_URL.format(company_number=company_number)
        
        # Use Basic Authentication to make the request
        response = requests.get(url, auth=(API_KEY_LIVE, ''))

        # Check the response status
        if response.status_code == 200:
            data = response.json()
            
            # Extracting required fields
            company_name = data.get('company_name', 'N/A')
            country = data.get('registered_office_address', {}).get('country', 'N/A')
            status = data.get('company_status', 'N/A')

            # Extracting SIC codes
            sic_codes = data.get('sic_codes', [])
            sic_codes_str = ', '.join(sic_codes) if sic_codes else 'N/A'




            sic_codes_dict = fetch_sic_codes()
            sic_codes = [code.strip() for code in sic_codes_str.split(',')]


            descriptions = []
            for code in sic_codes:
                desc = sic_codes_dict.get(code, f"Unknown SIC code: {code}")
                descriptions.append(desc)

            sic_code_descr = " and ".join(descriptions)


            # Prepare data for display in a DataFrame
            result_data = {
                "Company Number": [company_number],
                "Company Name": [company_name],
                "Country": [country],
                "Company Status": [status],
                "SIC Codes": [sic_codes_str], 
                "SIC Description": [sic_code_descr] 
            }

            df = pd.DataFrame(result_data)

            # Display the result in a table
            st.subheader("Company Information")
            st.table(df)

        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    else:
        st.warning("Please enter a valid company number.")


    addl_info = {
    "company house": ["https://find-and-update.company-information.service.gov.uk/company/07991498"],
    "sic codes": ["https://resources.companieshouse.gov.uk/sic/"]
    }

    addl_df = pd.DataFrame(addl_info)
    st.subheader("Demo: Additional Details")
    st.table(addl_df)
