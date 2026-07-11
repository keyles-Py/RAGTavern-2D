from langchain_ollama import OllamaEmbeddings, ChatOllama

embeddings = OllamaEmbeddings(model="nomic-embed-text")

llm = ChatOllama(
    model="phi3",
    temperature=0.7
)

persist_directory = "./tavern_vector_db"