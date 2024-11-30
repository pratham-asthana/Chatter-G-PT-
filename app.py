#importing necessary libraries.
import streamlit as st                 #importing streamlit for building an interactive GUI.
import os                              #importing os to access environmental variables on the system.
       #importing this to load environmental variables(API key here) to runtime environment.
import google.generativeai as gen_ai   #importing google's generativeAI module to use Google's AI model.

#loading .env file (containing API key).


#setting page configuration like the title, icon, layout, etc.
st.set_page_config(
    page_title = 'Chatter-G',
    page_icon=":face_with_monocle:",
    layout="centered"
)

#assigning API key to a variable GOOGLE_API_KEY.
GOOGLE_API_KEY = st.secrets("GOOGLE_API_KEY")

#setting up the model. 
gen_ai.configure(api_key = GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

#defining a function to translate the role to be served by streamlit (helpful when working with saving history).
def translate_role(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

#this ensures that if there's no existing chat session then the bot has to start a new chat session and start it's history.
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history = [])

#assigning the bot a creative name. 
st.title("Chatter-G (PT)")

#iterating through history and keeping each prompt with it's answer like a conversation.
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role(message.role)): #using translate_role function to save the history as 2 distinguish personalities(user and assistant).
        st.markdown(message.parts[0].text)

#providing an input box to enter prompt.
user_prompt = st.chat_input("Ask Chatterji...")

#when prompt is provided, the prompt is first displayed.
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    #generating response according to the provided prompt and storing it in a variable.
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    
    #displaying the generated responses at assistant's side.
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)