import streamlit as st
import groq

Modelos = ['Seleccionar un modelo', 'openai/gpt-oss-120b', 'llama-3.3-70b-versatile', 'qwen/qwen3-32b']

def client():
    groqkey = st.secrets["GROQ_API_KEY"]
    return groq.Groq(api_key=groqkey)

def init_state_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def prompt_input():
    return st.chat_input("Enviar un Mensaje")

def message_history(role, content):
    st.session_state.mensajes.append({"role":role, "content":content})

def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(f"**{content}**")

def mostrar_historial_chat():
    for mensajes in st.session_state.mensajes:
        with st.chat_message(mensajes["role"]):
            st.markdown(mensajes["content"])

def obtener_respuesta_GROQ(cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        stream = False
    )
    return respuesta.choices[0].message.content

def ejecute_app():
    config()
    modelo = sidebar()
    cliente = client()
    init_state_chat()
    mostrar_historial_chat()
    mensaje_user = prompt_input()
    print(mensaje_user)

    if mensaje_user:
        message_history("user", mensaje_user)
        mostrar_mensaje("user", mensaje_user)

        if modelo == "Seleccionar un modelo":
            mostrar_mensaje("assistant", "No se ha seleccionado ningun modelo :material/close:")

        respuestas_modelo = obtener_respuesta_GROQ(cliente, modelo, st.session_state.mensajes)

        message_history("assistant", respuestas_modelo)

        mostrar_mensaje("assistant", respuestas_modelo)

def sidebar():
    st.sidebar.title(":green[Menu General]")
    m = st.sidebar.selectbox("Elegi el modelo que desee", Modelos, index=0)
    st.sidebar.divider()
    st.sidebar.markdown("Creado por :green-background[Agustin Aguirre]")
    st.sidebar.markdown("Para :orange-background[TALENTO TECH | GCBA]")
    
    if m.startswith("openai/gpt-oss-120b"):
        st.sidebar.markdown(":orange[**openai/gpt-oss-120b es un modelo de lenguaje desarrollado por OpenAI, diseñado para ofrecer respuestas rápidas y eficientes con un tamaño de 8 mil millones de parámetros.**]")
    elif m.startswith("llama-3.3-70b-versatile"):
        st.sidebar.markdown(":green[**Llama 3.3-70b-versatile es un modelo de lenguaje desarrollado por Meta, diseñado para ofrecer respuestas versátiles y eficientes con un tamaño de 70 mil millones de parámetros.**]")
    elif m.startswith("qwen/qwen3-32b"):
        st.sidebar.markdown(":violet[**Qwen3-32b es un modelo de lenguaje desarrollado por Alibaba, diseñado para ofrecer respuestas precisas y eficientes con un tamaño de 32 mil millones de parámetros.**]")


    if m == "Seleccionar un modelo":
        st.markdown("No se ha seleccionado ningun modelo :material/close:")
        st.session_state.mensajes = []
    elif m == "openai/gpt-oss-120b":
        st.markdown("Modelo Seleccionado: :orange[openai/gpt-oss-120b] :material/smart_toy:")
        st.session_state.mensajes = []
    elif m == "llama-3.3-70b-versatile":
        st.markdown("Modelo Seleccionado: :green[llama-3.3-70b-versatile] :material/smart_toy:")
        st.session_state.mensajes = []
    elif m == "qwen/qwen3-32b":
        st.markdown("Modelo Seleccionado: :violet[qwen/qwen3-32b] :material/smart_toy:")
        st.session_state.mensajes = []
    st.divider()
    return m

def config():
    st.set_page_config(
        page_title="AgukBot", 
        page_icon="🤖",
        layout="centered")
    st.title(":green[Agukbot:]:violet[   Chatbot IA 🤖]")
    st.markdown(":small[:green[AgukBot] es mi primer proyecto personal creado con Python. Este chatbot abarca tres modelos: :blue[openai/gpt-oss-120b, Llama 3.3 y Qwen3-32b]. El objetivo de este proyecto es aprender a integrar modelos de lenguaje en aplicaciones prácticas, y explorar las capacidades de la inteligencia artificial en el procesamiento del lenguaje natural. :material/smart_toy:]")
    st.divider()

if __name__ == "__main__":
    ejecute_app()