import streamlit as st
from utils import aiguard_utils

def display_title():
    st.title("EU AI Act Questionnaire")

def display_adv_radio_button(options, placeholder_text, b_horizontal, key):
    selected_option = st.radio(placeholder_text, options, horizontal=b_horizontal, key=key)
    
    if selected_option == "Not sure":
        user_input = st.text_input("Please specify:", key=f"{key}_input")
        return selected_option, user_input
    else:
        return selected_option, None

def display_adv_radio_button_partner(options, placeholder_text, b_horizontal, key):
    selected_option = st.radio(placeholder_text, options, horizontal=b_horizontal, key=key)
    
    if selected_option == "Yes":
        user_input = st.text_input("Please specify:", key=f"{key}_input")
        return selected_option, user_input
    else:
        return selected_option, None
    

def display_radio_button(options, placeholder_text="Select an option:", b_horizontal=False, key="radio"):
    selected_option = st.radio(placeholder_text, options, horizontal=b_horizontal, key=key)
    return selected_option
    
def display_input_box(user_input_box, placeholder, key):
    return st.text_input(user_input_box, placeholder=placeholder, key=key)

def display_text_box(user_input_txt, key):
    return st.text_area(user_input_txt, placeholder="Enter the description of AI Work that you are doing", key=key)

def display_disclaimer():
    disclaimer_message = st.secrets["disclaimer_message"]
    # disclaimer_text = (
    #     "This is not legal advice. We make a best effort to check against "
    #     "the Regulation and Directives and the applicable Articles, Annexes and Recitals to you within the EU AI Act."
    # )

    disclaimer_text = disclaimer_message

    st.markdown(
        f"<div style='background-color: #f1f1f1; padding: 10px; text-align: center; border-top: 1px solid #ccc;'><span style='color: red;'>{disclaimer_text}</span></div>",
        unsafe_allow_html=True
    )


def main():
    st.sidebar.title("EU AI Act Compliance")

    with st.container() as main_container:
        display_title()


        custtype = ["An Individual using AI Models in personal capacity", 
                    "Entity based in UK providing AI services in EU",
                    "Entity based in EU or Subsidiary in EU and providing AI services in EU", 
                    "Entity based outside of EU (Eg: US, India, Australia etc) and providing services to company(ies) in EU", 
                    "Not touching EU in any way"
                   ]

        selected_custtype = st.selectbox(
            "You are: ",
            custtype,
            index=0,
            key="custtype_selector"
        )  

        # nature of business
        natureof_business = [
            "Biometrics",
            "Critical Infrastructure",            
            "Education and vocational training",
            "Employment, workers management and access to self-employment",
            "Essential private services and essential public services",
            "Law enforcement",
            "Migration, asylum and border control management",
            "Administration of justice and democratic processes"
        ]

        # Create a dropdown for top questions with an option for custom input
        selected_nob = st.selectbox(
            "Nature of your business:",
            natureof_business,
            index=0,
            key="select_nob"
        )


        # model series
        model_series = [
            "Closed Model (Eg: Chat GPT, Gemini)",
            "Open Model (Eg: Meta Llama, Google Gemma)"        
        ]

        # Create a dropdown for top questions with an option for custom input
        selected_series = st.selectbox(
            "Model Series:",
            model_series,
            index=0,
            key="select_series"
        )

        # model name
        model_name = [
            "Chat GPT o1",
            "Chat GPT 4",
            "Chat GPT 4o",       
            "Chat GPT 3.5",     
            "Gemini 1.5",    
            "Gemini 1.5 Flash", 
            "Gemini 2.0 Experimental",
            "Gemma", 
            "Meta Llama", 
            "Perplexity", 
            "Claude Anthropic", 
            "Mistral"
        ]

        # Create a dropdown for top questions with an option for custom input
        selected_model = st.selectbox(
            "Model Series:",
            model_name,
            index=0,
            key="select_model"
        )


        finetune = ["Fine tuning the models", "Not Fine tuning the models", "Not sure"]
        finetune_type = display_radio_button(finetune, "Are you fine tuning the Foundational / Frontier Model(s):", b_horizontal=True, key="finetune_selector")   

        technique = ["LoRA / QLoRA", "PEFT", "SFT", "RLHF", "Not sure"]
        technique_type = display_radio_button(technique, "Are you fine tuning the Foundational / Frontier Model(s):", b_horizontal=True, key="technique_selector") 

        partnerInfo = ["No", "Yes"]
        selected_partnerInfo, partner_role = display_adv_radio_button_partner(partnerInfo, "Are you partnering for AI Services with another company:", b_horizontal=True, key="partnerInfo_selector")

        if partner_role:
            st.write(f"You selected: {selected_partnerInfo}")
            st.write(f"Partner role: {partner_role}")
        else:
            st.write(f"You selected: {selected_partnerInfo}")

        ui_company_str = "Company Number (applicable UK companies): "
        company_ph = "Enter your Company Number"
        ui_company_value = display_input_box(ui_company_str, company_ph, key="company_number")

        companyStage = ["Startup, Bootstrapped","Startup, VC Funded", "Not applicable"]
        selected_companyStage = display_radio_button(companyStage, "Select your Company Details:", b_horizontal=True, key="companyStage_selector")

        numbEmp = ["1 - 500", "501 - 3000","3001 - 7000", "Beyond 7000"]
        selected_numbEmp = display_radio_button(numbEmp, "Company Staff:", b_horizontal=True, key="numbEmp_selector")

        compRev = ["< 500,000 GBP", "Between 500,001 - 1M GBP","Between 1M - 5M GBP", "Beyond 5M GBP"]
        selected_compRev = display_radio_button(compRev, "Annual Revenue:", b_horizontal=True, key="compRev_selector")

        ui_aiwork_str = "Please describe your AI system or your involvement with AI:"
        aiwork_ph = ui_aiwork_str
        ui_aiwork_value = display_input_box(ui_aiwork_str, aiwork_ph, key="ai_work")

        roles = ["Provider", "Deployer", "Distributor", "Importer", "Not sure"]
        selected_roletype, cust_role = display_adv_radio_button(roles, "Do you know your role:", b_horizontal=True, key="roletype_selector")

        if cust_role:
            st.write(f"You selected: {selected_roletype}")
            st.write(f"Custom role: {cust_role}")
        else:
            st.write(f"You selected: {selected_roletype}")


             
        if st.button("Submit"):
            st.write(f"You selected: {selected_nob}")
            st.write(f"Model Series: {selected_series}")
            st.write(f"Your Model: {selected_model}")            
            st.write(f"Selected Role: {selected_custtype}")
            st.write(f"Services provided: {finetune_type}")   
            st.write(f"Services provided: {technique_type}")                      
            st.write(f"Company Number: {ui_company_value}")
            st.write(f"Company Status: {selected_companyStage}")   
            st.write(f"Company Status: {selected_numbEmp}")              
            st.write(f"Company Revenue: {selected_compRev}")   

            st.write(f"AI Work Details: {ui_aiwork_value}")    
            st.write(f"Foundation Models Used: {selected_model}")       

    
    with st.container() as footer_container:
        display_disclaimer()

if __name__ == "__main__":
    main()
