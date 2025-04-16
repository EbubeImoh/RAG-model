import streamlit as st
from main import handle_query

st.title("Multi-Source RAG Assistant")

user = st.text_input("Your Name:")
role = st.selectbox("Your Role:", ["admin", "employee", "guest"])
query = st.text_input("Ask a question:")
feedback = st.text_area("Feedback (Optional):")

if query:
    result = handle_query(query, user=user, role=role, feedback=feedback)
    st.markdown(f"**Source:** {result['source']}")
    st.subheader("Answer:")
    st.write(result['response'])
