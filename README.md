# RAGTavern-2D: RPG Sandbox con Inteligencia Artificial RAG Local

Un videojuego RPG en 2D desarrollado en **Pygame** que integra agentes **NPC inteligentes y autónomos** impulsados por modelos de lenguaje locales (**Ollama + Phi3**) mediante una arquitectura de Generación Aumentada por Recuperación (**RAG**). 

Los personajes no usan árboles de diálogo preescritos; en su lugar, consultan dinámicamente una base de datos vectorial de la taberna para hablar sobre el lore del reino, reaccionar a las acciones del jugador y recordar el historial de la conversación en tiempo real.

---

## Características Principales

*   **IA de NPCs mediante RAG Local:** Integración de LangChain y Ollama para ejecutar inferencia de LLMs 100% desconectada y privada.

*   **Lore Dinámico y Base de Datos Vectorial:** Los NPCs extraen información contextual sobre el Reino de Oakhaven, debilidades de dragones y misiones legendarias de forma semántica.
*   **Motor 2D desde Cero (Pygame):** Sistema de colisiones por separación de ejes (AABB), renderizado por sándwich de capas (profundidad detrás de la barra) y animaciones fluidas basadas en máquinas de estados por tiempo.
*   **Memoria de Conversación:** Soporte para historial de chat adaptado a la ventana gráfica del juego, limitando las respuestas de los modelos para encajar en cajas de diálogo RPG.

---

## Tecnologías Utilizadas

*   **Motor Gráfico:** Python 3.11+ / Pygame 2
*   **Orquestación de IA:** LangChain
*   **Modelos de Lenguaje:** Ollama (Phi3 / Mistral)
*   **Base de Datos Vectorial:** ChromaDB

---

## Arquitectura del Proyecto

El proyecto se divide en módulos limpios para separar el renderizado de la lógica cognitiva:

```
RAGTavern-2d/
├── game/
│   ├── assets/             # Spritesheets, fondos y recursos visuales
│   ├── classes.py          # Motores físicos del Player y los componentes de IA de Elena y Gimli
│   └── game.py             # Bucle principal del juego (Eventos, Updates y Renderizado 60 FPS)
├── rag/
│   ├── chain.py            # Cadena de rag
│   ├── config.py           # Configuración del llm en ollama
│   ├── embedder.py         # Crea la base de datos vectorial
│   ├── rag.py              # Llama a la cadena pasando la información necesaria para que funcione
├── tavern_vector_db/       # Base de datos vectorial creada la primera vez que se interactua con un NPC
│   └── chroma.sqlite3
├── .gitignore
├── requirements.txt
├── main.py                # Punto de entrada principal
└── README.md
```

## Instalación y Configuración

1. Prerrequisitos
Asegúrate de tener instalado Ollama en tu sistema local y descarga el modelo base:
```
ollama run phi3
```

2. Clonar el repositorio e instalar dependencias
```
git clone [https://github.com/TU_USUARIO/RAGTavern-2D.git](https://github.com/TU_USUARIO/RAGTavern-2D.git)
cd RAGTavern-2D
pip install -r requirements.txt
```

3. Ejecutar el juego
```
python main.py
```

## Cómo Jugar e Interactuar

* **Movimiento:** Usa las teclas W, A, S, D o las flechas de dirección.

* **Interactuar/Hablar:** Acércate a la barra (Gimli) o a la esquina (Elena) y presiona la tecla 2.

* **Escribir:** Cuando la caja de diálogo esté activa, escribe directamente tu mensaje y presiona ENTER para enviar al RAG.

* **Cerrar Chat:** Al presionar 2 nuevamente, la interfaz se limpiará automáticamente.

* **Mostrar Hitboxes:** Al presionar 1, se mostrarán las hitboxes del juego. (un pequeño detalle :D)

## Screenshots del juego
