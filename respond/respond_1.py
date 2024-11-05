import streamlit as st
import pandas as pd
from datetime import datetime
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer

st.header("Recomendaciones Principales")

# Acceder a nuevo_dataframe
if "nuevo_dataframe" in st.session_state and not st.session_state.nuevo_dataframe.empty:
    #st.write("Datos recopilados:")
    #st.dataframe(st.session_state.nuevo_dataframe)

    # Datos de trabajo -- YA FILTRADO POR ESCDE = SI (TRABAJO PARA PERSONAS CON DISCAPACIDAD)
    trabajo = pd.read_csv("datos/datos_trabajo.csv", sep=";")

    # Filtrar datos de trabajo por la fecha actual
    today = "2024-10-21"  # Fecha actual fija para evitar problemas de pruebas
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

    # Concatenar los DataFrames
    datos = pd.concat([datos, user_data], ignore_index=True)

    # Definir la función de recomendación con pesos
    def recomendar_vecinos(data, input_index, k, pesos):
        # Paso 1: Combinar las columnas relevantes en un nuevo campo para recomendación aplicando los pesos
        data['COMBINED'] = ((data['NOMBREAVISO'] + ' ') * pesos['NOMBREAVISO'] +
                            (data['DEPARTAMENTO'] + ' ') * pesos['DEPARTAMENTO'] +
                            (data['PROVINCIA'] + ' ') * pesos['PROVINCIA'] +
                            (data['DISTRITO'] + ' ') * pesos['DISTRITO'] +
                            (data['SINEXPERIENCIA'] + ' ') * pesos['SINEXPERIENCIA'] +
                            (data['EXPERIENCIA_MESES'].astype(str) + ' ') * pesos['EXPERIENCIA_MESES'] +
                            (data['TIPOTIEMPOEXPERIENCIA'] + ' ') * pesos['TIPOTIEMPOEXPERIENCIA'] +
                            (data['ESCO'] + ' ') * pesos['ESCO'] +
                            (data['NOMBRECOMPETENCIA'] + ' ') * pesos['NOMBRECOMPETENCIA'])

        # Paso 2: Crear la matriz TF-IDF basada en la columna 'COMBINED'
        vectorizer = TfidfVectorizer(lowercase=True, stop_words=["y", "de"], token_pattern=r'\b\w+\b', use_idf=True)
        X = vectorizer.fit_transform(data['COMBINED'])

        # Paso 3: Entrenar el modelo de vecinos más cercanos usando la métrica de distancia coseno
        modelo = NearestNeighbors(n_neighbors=k+1, metric='cosine')  # k+1 porque queremos el aviso más k vecinos
        modelo.fit(X)

        # Paso 4: Obtener las recomendaciones (vecinos más cercanos)
        distances, indices = modelo.kneighbors(X[input_index], n_neighbors=k+1)  # k+1 para incluir el propio punto
        recommended_indices = indices[0][1:]  # Excluir el propio punto en la lista de recomendaciones

        # Retornar las recomendaciones sin incluir el propio punto
        recomendaciones = data.iloc[recommended_indices]

        return recomendaciones[['NOMBREAVISO', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO',
                                'FECHAINICIO', 'FECHAFIN', 'SINEXPERIENCIA', 'MODALIDADTRABAJO',
                                'TIEMPOEXPERIENCIA', 'TIPOTIEMPOEXPERIENCIA', 'SECTOR', 'ESCO',
                                'NOMBRECOMPETENCIA']]

    # Definir los pesos para cada columna
    pesos = {
        'NOMBREAVISO': 1,
        'DEPARTAMENTO': 1,
        'PROVINCIA': 2,
        'DISTRITO': 1,
        'SINEXPERIENCIA': 3,
        'EXPERIENCIA_MESES': 1,
        'TIPOTIEMPOEXPERIENCIA': 1,
        'ESCO': 4,
        'NOMBRECOMPETENCIA': 4
    }

    # Aplicar la función de recomendación
    st.write("Recomendaciones:")
    input_index = datos.index[-1]  # Índice del nuevo registro
    recomendaciones = recomendar_vecinos(datos, input_index, k=5, pesos=pesos)  # k=5 para 5 recomendaciones
    st.dataframe(recomendaciones)

    # Selección de recomendación para ver similares
    st.header("Otras Recomendaciones")
    seleccion = st.selectbox("Selecciona una recomendación para ver las similares", recomendaciones['NOMBREAVISO'])

    if seleccion:
        selected_index = datos[datos['NOMBREAVISO'] == seleccion].index[0]
        similares = recomendar_vecinos(datos, selected_index, k=5, pesos=pesos)
        st.write(f"Recomendaciones similares a '{seleccion}':")
        st.dataframe(similares)

else:
    st.write("No hay datos recopilados. Por favor, complete el formulario de registro primero.")