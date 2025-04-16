from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

def embed_documents(documents: list):
    """
    Convert a list of documents into embeddings.
    """
    embeddings = OpenAIEmbeddings()  # Or use another embedding model
    return [embeddings.embed_document(doc) for doc in documents]

def store_embeddings(embeddings: list, vectorstore_path: str):
    """
    Store the generated embeddings in a FAISS vectorstore.
    """
    vectorstore = FAISS.from_embeddings(embeddings)
    vectorstore.save_local(vectorstore_path)  # Save it to a local file
    return vectorstore