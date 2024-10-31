import streamlit as st
import pandas as pd
from datetime import datetime
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer


st.header("Recomendaciones Principales")

# Acceder a nuevo_dataframe
if "nuevo_dataframe" in st.session_state and not st.session_state.nuevo_dataframe.empty:
    st.write("Datos recopilados:")
    st.dataframe(st.session_state.nuevo_dataframe)

    # Leer los datos de trabajo
    trabajo = pd.read_csv("datos/datos_trabajo.csv", sep=";")

    # Filtrar datos de trabajo por la fecha actual
    #today = datetime.today().strftime('%Y-%m-%d')
    today = "2024-10-21"
    datos = trabajo[trabajo["FECHAFIN"] >= today]

    # Crear una copia de nuevo_dataframe y renombrar las columnas para coincidir
    user_data = st.session_state.nuevo_dataframe.copy()
    user_data = user_data.rename(columns={
        "Departamento": "DEPARTAMENTO",
        "Provincia": "PROVINCIA",
        "Distrito": "DISTRITO",
        "¿Tiene experiencia laboral?": "SINEXPERIENCIA",
        "Sectores Preferentes": "SECTOR",
        "Skills": "NOMBRECOMPETENCIA",
        "Tiempo de experiencia laboral (meses)": "EXPERIENCIA_MESES"
    })

    # Invertir los valores de la columna SINEXPERIENCIA en user_data
    user_data["SINEXPERIENCIA"] = user_data["SINEXPERIENCIA"].apply(lambda x: "SI" if x == "No" else "NO")
    
    # Añadir las columnas faltantes a user_data con valores "-"
    columnas_faltantes = [col for col in datos.columns if col not in user_data.columns]
    for col in columnas_faltantes:
        user_data[col] = "-"

    # Seleccionar las columnas en el orden de datos
    user_data = user_data[datos.columns]

    # Concatenar los dataframes
    datos_combinados = pd.concat([datos, user_data], ignore_index=True)

    # Mostrar los datos combinados
    st.write("Datos combinados:")
    st.dataframe(datos_combinados)
else:
    st.write("No hay datos recopilados. Por favor, complete el formulario de registro primero.")

# Trabajando con los datos combinados
trabajo = pd.read_csv("datos/datos_trabajo.csv", sep=";")
datos = trabajo[trabajo["FECHAFIN"] >= "2024-10-21"]  # La fecha sería fecha de hoy que se actualiza diariamente

st.write(datos.columns)

# Crear la columna de números consecutivos
# datos['ID_CONSECUTIVO'] = range(1, len(datos) + 1)
# datos.reset_index(drop=True, inplace=True)

# st.write(datos)