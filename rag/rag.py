from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.documents import Document
from rag.config import persist_directory
from rag.chain import create_rag_chain
from rag.embedder import get_vector_db
import os

text_fragments = [
    "La Taberna del Drunken Dragon está ubicada en el cruce de caminos del reino de Oakhaven. Es un lugar ruidoso, iluminado por velas y huele a cerveza y madera quemada.", 
    "Gimli es el tabernero. Es un enano testarudo pero de buen corazón. Odia a los clientes que no pagan y le encanta hablar sobre armas y minería.",
    "Elena es una barda sentada en la esquina de la taberna. Es perspicaz, observadora, habla de forma elocuente y toca el laúd para ganarse la vida.",

    "El Reino de Oakhaven está gobernado por el Rey Aldous III. Recientemente el rey impuso un impuesto brutal sobre el oro y la cerveza, lo que tiene a los enanos y campesinos furiosos.",
    "Al norte del reino se encuentran las Montañas de Colmillo Gris, un lugar plagado de guivernos, ruinas antiguas y minas abandonadas llenas de piedras preciosas.",
    "Existe un rumor en la taberna de que los bandidos del Bosque Susurrante están planeando un asalto al cargamento de suministros reales que pasará cerca del cruce de caminos.",

    "Los dragones antiguos no han sido vistos en Oakhaven desde hace un siglo, pero las leyendas dicen que el dragón de ceniza, Ignis el Voraz, duerme bajo el volcán inactivo del este.",
    "Según los viejos pergaminos de los sabios, las escamas del vientre de un dragón son tan blandas como el cuero, siendo su único punto débil ante un arma forjada con acero rúnico.",
    "Los dragones se sienten fuertemente atraídos por el olor de la sangre real y los artefactos mágicos de la era de los elfos, los cuales acumulan en sus nidos.",

    "El jugador es el último portador del Fragmento Estelar, un amuleto místico que parpadea con una luz azul cuando hay peligro mágico o criaturas ancestrales cerca.",
    "La misión legendaria del jugador consiste en encontrar las tres llaves de obsidiana para sellar la Grieta del Vacío antes de que los no-muertos invadan las Tierras Altas.",
    "Gimli sospecha en secreto que el jugador oculta algo importante debido a la extraña espada rúnica que lleva en la espalda, aunque prefiere no meterse en problemas con la guardia real.",
    "Elena ha notado el brillo del Fragmento Estelar en el cuello del jugador y sospecha que él es el héroe de la profecía del que hablan los cantares de la corte."
]

doc_fragments = []
for fragment in text_fragments:
    new_doc = Document(
                page_content=fragment,
                metadata={"source": "lore del juego", "author" : "Keiner"}
            )
    doc_fragments.append(new_doc)

def update_tavern_db(vectordb, npc_name : str, player_msg : str, npc_reply : str):
    info_contexto = f"El jugador le dijo a {npc_name}: '{player_msg}'. A lo que {npc_name} respondió: '{npc_reply}'."
    new_doc = Document(
                page_content=info_contexto,
                metadata={"source": "conversación_taberna", "author" : npc_name}
            )
    vectordb.add_documents([new_doc])


historiales = {
        "Gimli" : [],
        "Elena" : []
    }

def generate_rag_response(player_msg : str, npc_name : str) -> str:

    if not os.path.exists(persist_directory) or len(os.listdir(persist_directory)) == 0: 
        vectordb = get_vector_db(doc_fragments)
    else:
        vectordb = get_vector_db()

    retriever = vectordb.as_retriever(search_kwargs={"k":2})

    rag_chain = create_rag_chain(retriever)



    prompts_npc = {
        "Gimli": (
            "Eres Gimli, el tabernero enano de la Taberna del Drunken Dragon. "
            "Tu personalidad es hosca, directa, tacaña y ruda. Hablas como un trabajador cansado. "
            "PROHIBIDO: Tienes terminantemente prohibido decir que eres una IA, un modelo de lenguaje o un programa. "
            "Siempre debes responder desde la ficción, actúas en un videojuego medieval de rol. "
            "INSTRUCCIÓN RAG: Usa obligatoriamente los datos que sabes (el contexto provisto) para alimentar "
            "los chismes y rumores de la taberna. Si tienes información sobre un evento, úsala para continuar la charla. "
            "REGLA CRÍTICA: Habla sin elocuencia. Responde con frases directas y MUY CORTAS (máximo 100 caracteres)."
        ),
        "Elena": (
            "Eres Elena, una barda humana perspicaz, curiosa, artística y misteriosa. "
            "PROHIBIDO: Nunca menciones que eres una IA, un bot o un software. Eres un personaje de fantasía medieval. "
            "INSTRUCCIÓN RAG: Eres la reina de los chismes. Te encanta usar todo lo que has escuchado en la taberna "
            "(la información del contexto) para armar intrigas. Si el jugador te da un dato o te pregunta por un rumor, "
            "conéctalo con lo que sabes y sigue la conversación de forma amigable y fluida. "
            "REGLA CRÍTICA: Mantén el misterio pero sé breve. Responde con frases MUY CORTAS (máximo 100 caracteres)."
        )
    }

    if not player_msg.strip():
        return "Seguire en lo mio."

    response = rag_chain.invoke({
        "input": player_msg,
        "chat_history": historiales[npc_name],
        "personalidad": prompts_npc[npc_name]
    })

    historiales[npc_name].extend([
        HumanMessage(content=player_msg),
        AIMessage(content=response['answer'])
    ])

    update_tavern_db(vectordb, npc_name, player_msg, response['answer'])

    return response['answer']