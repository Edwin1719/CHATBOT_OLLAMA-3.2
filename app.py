import streamlit as st
from langchain_ollama import ChatOllama
from st_social_media_links import SocialMediaIcons

# Configuración de la aplicación
st.set_page_config(page_title="ASISTENTE VIRTUAL DATABiQ", page_icon="https://i.postimg.cc/zDgSpFj7/LOGO-DATABi-Q.png")

# Mostrar logo y título centrados
logo_url = "https://i.postimg.cc/zDgSpFj7/LOGO-DATABi-Q.png"
st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center; padding: 10px;">
        <img src="{logo_url}" style="height: 100px; margin-right: 20px;">
        <h1 style="font-size: 2em; font-weight: bold;">ASISTENTE VIRTUAL DATABiQ</h1>
    </div>
    """, unsafe_allow_html=True)

# Inicializar estado
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hola, soy tu asistente virtual experto en Ciencia y Análisis de Datos. ¿En qué puedo ayudarte hoy?"}]
if "history" not in st.session_state:
    st.session_state["history"] = [("system", "Eres un asistente virtual experto en Ciencia y Análisis de Datos. Responde a las preguntas del usuario de forma técnica y detallada.")]

# Mostrar mensajes
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Procesar entrada del usuario
if prompt := st.chat_input():
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.session_state["history"].append(("human", prompt))
    st.chat_message("user").write(prompt)
    
    llm = ChatOllama(model="llama3.2", temperature=0)
    response = llm.invoke(st.session_state["history"])
    
    st.chat_message("assistant").write(response.content)
    st.session_state["messages"].append({"role": "assistant", "content": response.content})
    st.session_state["history"].append(("assistant", response.content))

# Pie de página
st.markdown("""
---
**Responsable:** Edwin Quintero Alzate/ 
**Email:** egqa1975@gmail.com
""")

social_media_links = [
    "https://www.facebook.com/edwin.quinteroalzate",
    "https://www.linkedin.com/in/edwinquintero0329/",
    "https://github.com/Edwin1719"]

SocialMediaIcons(social_media_links).render()
