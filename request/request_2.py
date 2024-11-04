import streamlit as st
import pandas as pd

st.header("Skill Assesment")


skills_tipos = [
    'adaptarse', 'afrontar', 'analizar', 'aplicar', 'archivar', 'asegurar', 'asesorar', 'asistir', 'asumir', 
    'ayudar', 'calcular', 'cambiar', 'cargar', 'colaborar', 'comprobar', 'comunicarse', 'comunicar', 
    'conducir', 'conservar', 'consultar', 'controlar', 'coordinar', 'cosechar', 'crear', 'cuidar', 
    'cumplir', 'cultivar', 'desarrollar', 'desinfectar', 'detectar', 'determinar', 'diseñar', 'efectuar', 
    'elaborar', 'eliminar', 'emitir', 'emplear', 'empaquetar', 'enseñar', 'entregar', 'establecer', 
    'estándar', 'evaluar', 'examinar', 'ejecutar', 'facilitar', 'garantizar', 'gestionar', 'gestión', 
    'identificar', 'instalar', 'interpretar', 'leer', 'levantar', 'limpiar', 'manejar', 'mantener', 
    'mantenerse', 'manipular', 'negociar', 'observar', 'ofrecer', 'operar', 'organizar', 'pensar', 
    'planificar', 'practicar', 'presentar', 'preparar', 'procesar', 'proporcionar', 'proteger', 
    'promocionar', 'realizar', 'recibir', 'redactar', 'rellenar', 'reparar', 'resolver', 'respetar', 
    'responder', 'revisar', 'seguir', 'supervisar', 'tolerar', 'trabajar', 'utilizar'
]
skills = st.multiselect("Selecciona hasta 5 verbos con los que te sientas identificado", skills_tipos, key="skills")
if len(skills) > 5:
    st.error("Puedes seleccionar un máximo de 5 verbos.")

if st.button("Recomendaciones de Trabajo"):
    if "nuevo_dataframe" in st.session_state and not st.session_state.nuevo_dataframe.empty:
        st.session_state.nuevo_dataframe["Skills"] = ", ".join(skills)
        st.session_state.role = "Recomendaciones Principales"
        st.rerun()
    else:
        st.error("No se han recopilado datos previos. Por favor, complete el formulario de registro primero.")

# Acceder a nuevo_dataframe
if "nuevo_dataframe" in st.session_state and not st.session_state.nuevo_dataframe.empty:
    st.write("Datos previamente guardados:")
    st.dataframe(st.session_state.nuevo_dataframe)