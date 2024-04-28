import os
import streamlit as st
import google.generativeai as gen_ai
from PIL import Image  


tab1, tab2 = st.tabs(["Farm-Ez", "Vis-farm"])

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key="AIzaSyC5RiRjeKWNQkrUJxKWjfBr4w1oF12Wr8Y")
model = gen_ai.GenerativeModel('gemini-1.0-pro')
s = model.generate_content("Imagine you are a  professional Agriculture expert and you are helping a farmer to solve a problem. Provide valuable insights  to the farmer and it should be more specific in the context of Indian Agriculture?")

with tab1:
    
    # Function to translate roles between Gemini-Pro and Streamlit terminology
    def translate_role_for_streamlit(user_role):
        if user_role == "model":
            return "assistant"
        else:
            return user_role

    
    # Initialize chat session in Streamlit if not already present
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])


    st.title("🤖 Farm-Ezyyy!!!")


    

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.text_input("Ask ✨Farm-Ezy")
    if user_prompt:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

with tab2:
    img = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if img is not None:
        image = Image.open(img)
        st.image(img, caption='Uploaded Image.', use_column_width=True)
        vision_model = gen_ai.GenerativeModel('gemini-pro-vision')
        submit = st.button("Submit")
        if submit:
            response = vision_model.generate_content(["Explain the picture?",image])
            st.write(response.text)