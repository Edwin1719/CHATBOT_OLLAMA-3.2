import threading
import streamlit as st
from fastapi import FastAPI
from langchain_ollama import ChatOllama
import uvicorn
import requests
from st_social_media_links import SocialMediaIcons

# Configuración de FastAPI
app = FastAPI()
llm = ChatOllama(model="llama3.2", temperature=0)

@app.get("/ask")
async def ask_question(question: str):
    # Llama al modelo y obtiene la respuesta
    response = llm.invoke([("human", question)])
    return {"answer": response.content}

# Función para correr el servidor FastAPI en un hilo separado
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Correr el servidor FastAPI en un hilo
threading.Thread(target=run_fastapi, daemon=True).start()

# Definiendo la aplicación de Streamlit
st.set_page_config(page_title="ASISTENTE VIRTUAL DATABiQ", page_icon="https://i.postimg.cc/zDgSpFj7/LOGO-DATABi-Q.png")

# Enlace directo a la imagen en Google Drive
logo_url = "https://i.postimg.cc/zDgSpFj7/LOGO-DATABi-Q.png"

# Mostrar el logo en la parte superior derecha y centrar el título
st.markdown(
    f"""
    <style>
    .logo-container {{
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding: 10px;
    }}
    .logo {{
        height: 100px;  /* Ajusta este valor para cambiar el tamaño del logo */
    }}
    .title-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px;
    }}
    .title {{
        font-size: 2em;
        font-weight: bold;
    }}
    </style>
    <div class="logo-container">
        <img src="{logo_url}" class="logo">
    </div>
    <div class="title-container">
        <h1 class="title">ASISTENTE VIRTUAL DATABiQ</h1>
    </div>
    """,
    unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hola, ¿cómo puedo asistirte hoy?"}]

if "history" not in st.session_state:
    st.session_state["history"] = [("system", "Eres un asistente virtual que responde preguntas al usuario de forma amable y eficiente")]

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.session_state["history"].append(("human", prompt))
    st.chat_message("user").write(prompt)

    # Hacer la petición a la API de FastAPI
    response = requests.get("http://localhost:8000/ask", params={"question": prompt})
    answer = response.json().get("answer", "No response")

    st.chat_message("assistant").write(answer)
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    st.session_state["history"].append(("assistant", answer))

# Pie de página con información del desarrollador y logos de redes sociales
st.markdown("""
---
**Responsable:** Edwin Quintero Alzate/ 
**Email:** egqa1975@gmail.com
""")

social_media_links = [
    "https://www.facebook.com/edwin.quinteroalzate",
    "https://www.linkedin.com/in/edwinquintero0329/",
    "https://github.com/Edwin1719"]

social_media_icons = SocialMediaIcons(social_media_links)
social_media_icons.render()
