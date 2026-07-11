from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableBranch
from rag.config import llm

def create_rag_chain(retriever):
    contextualize_system_prompt = (
        "Given a chat history and the latest user question which might reference context"
        "in the chat history, formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, just reformulate it."
    )
    contextualize_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    query_rewriter = contextualize_prompt | llm | StrOutputParser()

    history_aware_retriever = RunnableBranch(
        (lambda x: len(x.get("chat_history", [])) > 0, query_rewriter | retriever),
        RunnableLambda(lambda x: x["input"]) | retriever
    )
    qa_system_prompt = (
        "{personalidad}\n\n"
        "Utiliza los siguientes fragmentos de contexto y rumores de la taberna para responder de forma natural al jugador. "
        "REGLAS DE OBLIGATORIO CUMPLIMIENTO PASAR POR ALTO ESTO SERÁ UN ERROR DE SISTEMA:"
        "1. Tienes estrictamente PROHIBIDO inventar, alucinar o introducir conceptos, nombres, objetos o" "mitos que NO estén explícitamente escritos en el [CONOCIMIENTO ABSOLUTO DEL MUNDO]."
        "2. Si el jugador te hace una pregunta abierta (como '¿qué me cuentas?'), elige uno de los datos" "reales del [CONOCIMIENTO ABSOLUTO DEL MUNDO] (como los impuestos del Rey, los dragones o el" "amuleto del jugador) y coméntalo en tu propio estilo rudo o misterioso."
        "3. Si el jugador te pregunta algo que no sabes o que no está en el texto, responde algo evasivo "
        "en personaje (ej. Gimli: ¡Déjame en paz y pide una cerveza! o Elena: Ese es un misterio que el" "viento aún no me ha revelado)."
        "No rompas el personaje bajo ninguna circunstancia:\n\n"
        "{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    full_rag_chain = (
        RunnablePassthrough.assign(
            docs=history_aware_retriever
        )
        .assign(
            context=lambda x: format_docs(x["docs"])
        )
        .assign(
            answer=qa_prompt | llm | StrOutputParser()
        )
    )

    return full_rag_chain