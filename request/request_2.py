import streamlit as st
import pandas as pd

st.header("Skill Assesment")
skills_tipos = ["realizar", "gestionar", "productos", "clientes", "limpieza", "equipos", "aplicar", "actividades", "registros", "comunicarse"]
skills = st.multiselect("Selecciona hasta 3 sectores", skills_tipos, key="skills")
if len(skills) > 3:
    st.error("Puedes seleccionar un máximo de 3 skills.")

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