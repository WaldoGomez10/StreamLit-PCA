import streamlit as st
import pandas as pd

st.header("Skill Assesment")
if st.button("Recomendaciones de Trabajo"):
    st.session_state.role = "Recomendaciones Principales"
    st.rerun()