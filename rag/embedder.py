import os
from langchain_chroma import Chroma
from rag.config import persist_directory, embeddings

def get_vector_db(documents=None):
    if os.path.exists(persist_directory) and len(os.listdir(persist_directory)) > 0:
        return Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )

    if documents:
        return Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=persist_directory
        )
    
    raise ValueError("db doesn't exist and no document was attached")