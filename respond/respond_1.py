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
    # today = datetime.today().strftime('%Y-%m-%d')
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

    # Concatenar los DataFrames
    datos = pd.concat([datos, user_data], ignore_index=True)

    # Mostrar los datos combinados
    st.write("Datos combinados:")
    st.dataframe(datos)

    # Definir la función de recomendación
    def recomendar_vecinos(data, input_index, k):
        # Paso 1: Combinar las columnas relevantes en un nuevo campo para recomendación
        data['COMBINED'] = (data['NOMBREAVISO'] + ' ' + data['DEPARTAMENTO'] + ' ' +
                            data['PROVINCIA'] + ' ' + data['DISTRITO'] + ' ' +
                            data['SINEXPERIENCIA'] + ' ' +
                            data['EXPERIENCIA_MESES'].astype(str) + ' ' +
                            data['TIPOTIEMPOEXPERIENCIA'] + ' ' + data['ESCO'] + ' ' +
                            data['NOMBRECOMPETENCIA'])
        
        # Paso 2: Crear la matriz TF-IDF basada en la columna 'COMBINED'
        vectorizer = TfidfVectorizer(lowercase=True, stop_words=["y", "de"], token_pattern=r'\b\w+\b', use_idf=True)
        X = vectorizer.fit_transform(data['COMBINED'])

        # Paso 3: Entrenar el modelo de vecinos más cercanos usando la métrica de distancia coseno
        modelo = NearestNeighbors(n_neighbors=k+1, metric='cosine')  # k+1 porque queremos el aviso más k vecinos
        modelo.fit(X)

        # Paso 4: Obtener las recomendaciones (vecinos más cercanos)
        distances, indices = modelo.kneighbors(X[input_index], n_neighbors=k+1)  # k+1 para incluir el propio punto
        recommended_indices = indices[0][1:]  # Excluir el propio punto en la lista de recomendaciones

        # Paso 5: Mostrar el propio aviso primero seguido de las recomendaciones
        propia_vacante = data.iloc[[input_index]]
        recomendaciones = data.iloc[recommended_indices]

        # Paso 6: Concatenar el propio aviso con las recomendaciones y retornar el resultado
        resultado = pd.concat([propia_vacante, recomendaciones])

        return resultado[['NOMBREAVISO', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO',
                          'FECHAINICIO', 'FECHAFIN', 'SINEXPERIENCIA', 'MODALIDADTRABAJO',
                          'TIEMPOEXPERIENCIA', 'TIPOTIEMPOEXPERIENCIA', 'SECTOR', 'ESCO',
                          'NOMBRECOMPETENCIA',"EXPERIENCIA_MESES"]]

    # Aplicar la función de recomendación
    st.write("Recomendaciones:")
    input_index = datos.index[-1]  # Índice del nuevo registro
    recomendaciones = recomendar_vecinos(datos, input_index, k=5)  # k=5 para 5 recomendaciones
    st.dataframe(recomendaciones)

else:
    st.write("No hay datos recopilados. Por favor, complete el formulario de registro primero.")

# Crear la columna de números consecutivos
# datos['ID_CONSECUTIVO'] = range(1, len(datos) + 1)
# datos.reset_index(drop=True, inplace=True)

# st.write(datos)