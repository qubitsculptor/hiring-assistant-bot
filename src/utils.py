import streamlit as st
from prompts import exit_keywords

def check_exit(user_input):
    return any(kw in user_input.lower() for kw in exit_keywords)

def display_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})
    with st.chat_message(role):
        st.markdown(content)
