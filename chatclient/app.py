import streamlit as st
from chatclient import ChatClient

st.set_page_config(page_title="ChatBot", layout="centered")

st.title("💬 ChatBot")

# Input field for backend URL
if "backend_url" not in st.session_state:
    st.session_state.backend_url = "https://capps-backend-gnbolbzn56rwi.blackisland-b81e2442.westeurope.azurecontainerapps.io"

backend_url = st.text_input("Backend URL", st.session_state.backend_url)
st.session_state.backend_url = backend_url

# Initialize chat client
if backend_url:
    client = ChatClient(backend_url)

    # Chat history
    if "history" not in st.session_state:
        st.session_state.history = []

    # Input field for message
    user_input = st.text_input("You:", "")

    if st.button("Send") and user_input:
        st.session_state.history.append(("You", user_input))
        bot_response = client.send_message(user_input)
        st.session_state.history.append(("Bot", bot_response))

    # Display chat history
    for speaker, msg in st.session_state.history:
        st.markdown(f"**{speaker}:** {msg}")
else:
    st.warning("Please enter a backend URL to begin.")

