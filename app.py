import streamlit as st
from chatbot import LionSightsChatbot
import config

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = LionSightsChatbot()
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Set page config
st.set_page_config(
    page_title=config.STREAMLIT_TITLE,
    page_icon="🦁",
    layout="wide"
)

# Header
st.title(config.STREAMLIT_TITLE)
st.markdown(config.STREAMLIT_DESCRIPTION)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about Singapore!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get chatbot response
    with st.chat_message("assistant"):
        response = st.session_state.chatbot.get_response(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Add a clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.chatbot.clear_memory()
    st.rerun()

# Add some helpful information in the sidebar
st.sidebar.markdown("""
### About LionSights
LionSights is your intelligent Singapore tourism companion. You can ask about:
- Tourist attractions
- Local food recommendations
- Transportation options
- Hidden gems
- Current events
- And much more!
""") 