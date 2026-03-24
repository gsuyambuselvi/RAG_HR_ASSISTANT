import streamlit as st
from QueryProcessor import process_user_query

st.set_page_config(page_title="HR Assistant", page_icon="💼", layout="centered")
st.title("💼 HR Policy Assistant")
st.caption("Ask me anything about the HR policy.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about HR policy..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = process_user_query(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
