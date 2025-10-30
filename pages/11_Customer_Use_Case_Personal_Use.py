import streamlit as st
from utils import rera_utils

def display_title():
    st.title("Customer Use Case - Personal use")

def display_adv_radio_button(options, placeholder_text, b_horizontal, key, index=0):
    selected_option = st.radio(placeholder_text, options, horizontal=b_horizontal, key=key,index=index,
                               help="This is a tooltip explaining the purpose of this radio button.")
    
    if selected_option == "Not sure":
        user_input = st.text_input("Please specify:", key=f"{key}_input")
        return selected_option, user_input
    else:
        return selected_option, None

def display_adv_radio_button_partner(options, placeholder_text, b_horizontal, key, index=0):
    selected_option = st.radio(placeholder_text, options, horizontal=b_horizontal, key=key, index=index)
    
    if selected_option == "Yes":
        user_input = st.text_input("Please specify:", key=f"{key}_input")
        return selected_option, user_input
    else:
        return selected_option, None
    

def display_radio_button(options, placeholder_text="Select an option:", b_horizontal=False, key="radio",index=0):
    selected_option = st.radio(placeholder_text, options, horizontal=b_horizontal, key=key, index=index)
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
    st.sidebar.title("Customer Use Case - Personal Use")

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
            index=1,
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
            index=2,
            key="select_model"
        )


        finetune = ["Fine tuning the models", "Not Fine tuning the models", "Not sure"]
        finetune_type = display_radio_button(finetune, "Are you fine tuning the Foundational / Frontier Model(s):", b_horizontal=True, key="finetune_selector")   

        ft_technique = ["LoRA / QLoRA", "PEFT", "SFT", "RLHF", "Not sure"]
        ft_technique_type = display_radio_button(ft_technique, "Are you fine tuning the Foundational / Frontier Model(s):", b_horizontal=True, key="ft_technique_selector") 


        ui_aiwork_str = "Please describe your AI system or your involvement with AI:"
        aiwork_ph = ui_aiwork_str
        ui_aiwork_value = display_input_box(ui_aiwork_str, aiwork_ph, key="ai_work")


        sic_desc = "Personal use for learning and poc proof of concept and research and not for profit and not for commercial purposes"
        query = f"""
                For {selected_custtype} and 
                Nature of business is {selected_nob} and 
                using {selected_series} and 
                using model {model_name} and 
                doing {finetune_type} 
                with {ft_technique_type} 
                and the entity is involved in the following {sic_desc}.
                 """
     
             
        if st.button("Submit"):            
            
            result = rera_utils.get_recommendation(query)

            # Display response 
            if result:  # Check if result is not None or empty
                st.text_area("Recommendations for Compliance:", value=result, height=500, disabled=False)
            else:
                st.error("No response received.")

   
    with st.container() as footer_container:
        display_disclaimer()

if __name__ == "__main__":
    main()
