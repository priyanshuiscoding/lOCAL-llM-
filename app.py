import os
import shutil
import streamlit as st
from utils import (
    load_file,
    chunk_documents,
    save_to_vectordb,
    query_vectordb,
    save_file
)

st.set_page_config(page_title="Local LLM", layout="wide")
st.title("🧠 Local LLM For Data Quering ")

# Chat history initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar: PostgreSQL Integration
st.sidebar.subheader("🛢️ PostgreSQL Database")
use_postgres = st.sidebar.checkbox("Use PostgreSQL instead of uploading files")

if use_postgres:
    host = st.sidebar.text_input("Host", "localhost")
    dbname = st.sidebar.text_input("Database", "testdb")
    user = st.sidebar.text_input("User", "postgres")
    password = st.sidebar.text_input("Password", type="password")
    table = st.sidebar.text_input("Table", "employees")

    if st.sidebar.button("Fetch from PostgreSQL"):
        from utils import load_from_postgres
        st.info("Fetching data from database...")
        try:
            docs = load_from_postgres(host, dbname, user, password, table)
            chunks = chunk_documents(docs)
            shutil.rmtree("faiss_index", ignore_errors=True)
            os.makedirs("faiss_index", exist_ok=True)
            save_to_vectordb(chunks)
            st.success("✅ PostgreSQL data loaded and indexed successfully!")
        except Exception as e:
            st.error(f"❌ Error fetching data from PostgreSQL: {e}")

# Sidebar for file uploads
st.sidebar.header("📂 Upload Files")

uploaded_files = st.sidebar.file_uploader(
    "Upload your files (PDF, TXT, CSV, DOCX, JPG, PNG)",
    type=["pdf", "txt", "csv", "docx", "jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Clear previous indexes if new files uploaded
if uploaded_files:
    shutil.rmtree("faiss_index", ignore_errors=True)
    os.makedirs("faiss_index", exist_ok=True)

    all_chunks = []
    with st.spinner("📄 Processing uploaded files..."):
        shutil.rmtree("uploads", ignore_errors=True)
        os.makedirs("uploads", exist_ok=True)

        for uploaded_file in uploaded_files:
            file_path = save_file(uploaded_file)
            try:
                docs = load_file(file_path)
                chunks = chunk_documents(docs)
                all_chunks.extend(chunks)
                st.success(f"✅ Processed `{uploaded_file.name}` with {len(chunks)} chunks.")
            except Exception as e:
                st.error(f"❌ Failed to process `{uploaded_file.name}`: {str(e)}")

    if all_chunks:
        save_to_vectordb(all_chunks)
        st.success("🧠 All files processed and indexed successfully.")
    else:
        st.warning("⚠️ No valid content found in uploaded files.")

# Question/Answer section
st.header("❓ Ask a question about your documents")
query = st.text_input("Enter your question:")

if query:
    with st.spinner("🔍 Searching for answers..."):
        try:
            result = query_vectordb(query)

            # Save to chat history
            st.session_state.chat_history.append({"question": query, "answer": result})

            # Display current result
            st.markdown("## ✅ Answer:")
            st.write(result)
        except Exception as e:
            st.error(f"❌ Error while answering: {e}")

# Display chat history
if st.session_state.chat_history:
    st.sidebar.subheader("📜 Chat History")
    for idx, chat in enumerate(st.session_state.chat_history):
        with st.sidebar.expander(f"Chat {idx+1}"):
            st.sidebar.markdown(f"**Q:** {chat['question']}")
            st.sidebar.markdown(f"**A:** {chat['answer']}")
