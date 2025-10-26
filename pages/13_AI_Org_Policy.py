import streamlit as st
from utils import aiguard_utils

def display_title():
    st.title("AI Policies")

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

def main():
    st.sidebar.title("AI Policies")

    with st.container() as main_container:
        display_title()


        # model series
        model_types = [
            "Closed Model (Eg: Chat GPT, Gemini)",
            "Open Model (Eg: Meta Llama, Google Gemma)"        
        ]

        model_types_radio = display_radio_button(model_types, "Model Types Allowed:", b_horizontal=True, key="modeltypes_selector")   

        # Define the list of models
        model_options = [
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


        st.write("Select Models:")


        # Create two rows of columns
        row1 = st.columns(4)
        row2 = st.columns(4)
        row3 = st.columns(4)

        # Distribute checkboxes across the three rows
        for i, option in enumerate(model_options):
            if i < 4:
                with row1[i]:
                    st.checkbox(option, key=f"checkbox_{i}")
            elif i < 8:  # Note: use 'elif' instead of 'else if'
                with row2[i-4]:
                    st.checkbox(option, key=f"checkbox_{i}")
            elif i < 12:
                with row3[i-8]:  # Note: use i-8 for the third row
                    st.checkbox(option, key=f"checkbox_{i}")


        finetune = ["Yes - Fine tuning is allowed", "No - Fine tuning is not allowed"]
        finetune_type = display_radio_button(finetune, "Is Fine Tuning of Models Allowed:", b_horizontal=True, key="finetune_selector")   

        ft_technique = ["LoRA / QLoRA", "PEFT", "SFT", "RLHF", "Not sure"]
        ft_technique_type = display_radio_button(ft_technique, "Are you fine tuning the Foundational / Frontier Model(s):", b_horizontal=True, key="ft_technique_selector") 

      
        if st.button("Submit"):            
            
            result = f"""Defined Policies:

            1. Model Types Allowed: {model_types_radio}

            2. Selected Models: {model_options}

            3. Fine Tuning Allowed: {finetune_type}

            4. Fine Tuning Technique: {ft_technique_type}
            """
                        

            # Display response 
            if result:  # Check if result is not None or empty
                st.text_area("Policies:", value=result, height=350, disabled=False)

            else:
                st.error("No response received.")

   
if __name__ == "__main__":
    main()
