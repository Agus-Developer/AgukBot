import streamlit as st
import groq

Modelos = ['Seleccionar un modelo', 'llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def sidebar():
    st.sidebar.title(":green[Menu General]")
    m = st.sidebar.selectbox("Eleji el modelo que desee", Modelos, index=0)
    st.sidebar.divider()
    st.sidebar.markdown("Creado por :green-background[Agustin Aguirre]")
    st.sidebar.markdown("Para :orange-background[TALENTO TECH]")

    if m == "Seleccionar un modelo":
        st.markdown("No se ha seleccionado ningun modelo :material/close:")
    elif m == "llama3-8b-8192":
        st.markdown("Modelo Seleccionado: :orange[llama3-8b-8192] :material/smart_toy:")
    elif m == "llama3-70b-8192":
        st.markdown("Modelo Seleccionado: :green[llama3-70b-8192] :material/smart_toy:")
    elif m == "mixtral-8x7b-32768":
        st.markdown("Modelo Seleccionado: :violet[mixtral-8x7b-32768] :material/smart_toy:")
    st.divider()
    return m

def config():
    st.set_page_config(
        page_title="AgukBot", 
        page_icon="🤖",
        layout="centered")
    st.title(":green[Agukbot:]:violet[   Chatbot IA 🤖]")
    st.markdown(":small[:green[AgukBot] es mi primer proyecto personal creado con Python. Este chatbot abarca dos modelos: :violet[Llama3 y Mixtral]]")
    st.divider()

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

        respuestas_modelo = obtener_respuesta_GROQ(cliente, modelo, st.session_state.mensajes)

        message_history("assistant", respuestas_modelo)

        mostrar_mensaje("assistant", respuestas_modelo)

if __name__ == "__main__":
    ejecute_app()