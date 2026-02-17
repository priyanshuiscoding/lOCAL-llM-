import os
import pickle
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

# ✅ Embedding model
HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-MiniLM-L3-v2")

# ✅ Vector DB paths
VECTOR_DB_DIR = "faiss_index"
VECTOR_DB_FILE = os.path.join(VECTOR_DB_DIR, "vectordb.pkl")

def create_vector_db(chunks):
    texts = [chunk.page_content for chunk in chunks if hasattr(chunk, "page_content")]
    metadatas = [chunk.metadata for chunk in chunks if hasattr(chunk, "metadata")]
    vectordb = FAISS.from_texts(texts, embedding_model, metadatas=metadatas)
    return vectordb

def ask_query(vectordb, query):
    llm = Ollama(model="mistral")
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})

    # Custom Prompt Template
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an expert assistant reading the Training and Placement Policy. 
Use only the context below to answer the question. Quote exact points or rules if available.

Context:
{context}

Question:
{question}

Answer:"""
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False,
        chain_type_kwargs={"prompt": prompt_template}
    )

    return qa.run(query)

def save_vector_db(vectordb):
    os.makedirs(VECTOR_DB_DIR, exist_ok=True)
    with open(VECTOR_DB_FILE, "wb") as f:
        pickle.dump(vectordb, f)

def load_vector_db():
    with open(VECTOR_DB_FILE, "rb") as f:
        return pickle.load(f)
