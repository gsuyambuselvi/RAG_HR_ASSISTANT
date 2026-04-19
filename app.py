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
        if message.get("scores"):
            with st.expander("Eval Scores", expanded=False):
                scores = message["scores"]
                col1, col2, col3 = st.columns(3)
                col1.metric("Faithfulness", f"{scores['faithfulness']:.0%}")
                col2.metric("Answer Relevancy", f"{scores['answer_relevancy']:.0%}")
                col3.metric("Context Relevancy", f"{scores['context_relevancy']:.0%}")

if prompt := st.chat_input("Ask a question about HR policy..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = process_user_query(prompt)

        if result["blocked"]:
            st.warning(result["answer"])
        else:
            st.markdown(result["answer"])
            if result["scores"]:
                with st.expander("Eval Scores", expanded=False):
                    scores = result["scores"]
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Faithfulness", f"{scores['faithfulness']:.0%}")
                    col2.metric("Answer Relevancy", f"{scores['answer_relevancy']:.0%}")
                    col3.metric("Context Relevancy", f"{scores['context_relevancy']:.0%}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "scores": result["scores"] if not result["blocked"] else None
    })
