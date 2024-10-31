import streamlit as st

st.header("Otras recomendaciones")
# Aquí va el contenido de otras recomendaciones.

# Acceder a nuevo_dataframe
if "nuevo_dataframe" in st.session_state and not st.session_state.nuevo_dataframe.empty:
    st.write("Datos recopilados:")
    st.dataframe(st.session_state.nuevo_dataframe)
