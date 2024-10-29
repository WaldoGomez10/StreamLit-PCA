import streamlit as st
import json
import csv
import pandas as pd 

# Título de la sección "INFORMACIÓN GENERAL"
st.header("INFORMACIÓN GENERAL")

# Primera fila
col1, col2 = st.columns(2)
col1.text_input("First names", key="first_name")
col2.text_input("Last names", key="last_name")

# Segunda fila
col3, col4 = st.columns(2)
col3.text_input("Edad", key="edad")
col4.text_input("Correo", key="correo")

# Tercera fila
default_educacion = "Selecciona un nivel educativo"
col5, col6 = st.columns(2)
col5.selectbox("Selecciona tu nivel educativo:", [
    "Sin Educación Formal",
    "Educación Primaria",
    "Educación Secundaria",
    "Educación Especial",
    "Educación Técnica",
    "Educación Universitaria",
    "Estudios de Maestría", 
    "Estudios de Doctorado"
], key="nivel_educativo")
col6.selectbox("Género", ["Femenino", "Masculino", "Otro"], key="genero")


# Suponiendo que tienes un archivo CSV con columnas: departamento, provincia, distrito
# Leer el CSV
df = pd.read_csv('datos/distritos.csv',sep=";")

# Crear un diccionario para almacenar las provincias y distritos
data = {}

# Llenar el diccionario
for _, row in df.iterrows():
    dep = row['DEPARTAMENTO']
    prov = row['PROVINCIA']
    dist = row['DISTRITO']
    
    if dep not in data:
        data[dep] = {}
    if prov not in data[dep]:
        data[dep][prov] = []
    
    data[dep][prov].append(dist)

# Crear columnas para Departamento, Provincia y Distrito
col7, col8, col9 = st.columns(3)

# Estado inicial de selección en cada selectbox
default_dep = "Selecciona un Departamento"
default_prov = "Selecciona una Provincia"
default_dist = "Selecciona un Distrito"

# Seleccionar departamento
with col7:
    selected_dep = st.selectbox("Departamento", [default_dep] + list(data.keys()))

# Seleccionar provincia basada en el departamento seleccionado (solo si se eligió un departamento)
with col8:
    if selected_dep != default_dep:
        provincias = list(data[selected_dep].keys())
        selected_prov = st.selectbox("Provincia", [default_prov] + provincias)
    else:
        selected_prov = st.selectbox("Provincia", [default_prov])

# Seleccionar distrito basado en la provincia seleccionada (solo si se eligió una provincia)
with col9:
    if selected_dep != default_dep and selected_prov != default_prov:
        distritos = data[selected_dep][selected_prov]
        selected_dist = st.selectbox("Distrito", [default_dist] + distritos)
    else:
        selected_dist = st.selectbox("Distrito", [default_dist])


# Conadis y Tipo de Discapacidad
col10, col11 = st.columns(2)
col10.selectbox("¿Tiene tarjeta CONADIS?", ["Sí", "No"], key="conadis")
col11.selectbox("¿Qué tipo de Discapacidad tiene?", ["Discapacidad Física o Motora", "Discapacidad Sensorial", 
                                                     "Discapacidad intelectual", "Discapacidad mental o psíquica"
                                                     ], key="discapacidad")

# Título de la sección "INFORMACIÓN LABORAL"
st.header("INFORMACIÓN LABORAL")

# Sector Preferente con máximo 3 selecciones
st.subheader("Sector Preferente")
sectores = [
    "Agricultura/Ganadería", "Agropecuaria", "Arquitectura", "Automotriz", "Autopistas",
    "Aviación/Aeronaves/Astilleros", "Banca/Finanzas/Seguros", "Científica", "Comercial",
    "Comercio mayorista", "Comercio minorista", "Construcción", "Consultoría en RRHH",
    "Consultoría/Asesorí­a", "Consumo Masivo", "Cosmética y Belleza", "Defensa",
    "Diseño y Decoración", "Educación", "Electrónica", "Entretenimiento", "Estudios Jurídicos",
    "Exportación e Importación", "Fabricación de sustancias y productos quí­micos",
    "Fabricación de vehículos y maquinaria", "Farmaceuticas", "Forestal/Papel y Celulosa",
    "Gobierno", "Hotelería / Turismo", "Imprenta / Editoriales", "Industria Metalmecánica",
    "Industrias varias", "Ingeniería", "Inmobiliaria y actividades de alquiler", "Internet",
    "Inversiones", "Investigación", "Laboratorio", "Logística / Distribución",
    "Manufactureras varias", "Maquinaria", "Materiales de Construcción",
    "Medios de Comunicación y Comunicaciones", "Minería e Hidrocarburos", "Naviera", "ONG",
    "Organizaciones y Órganos extraterritoriales", "Outsourcing",
    "Pesca, acuicultura y actividades relacionadas", "Producción de alimentos y bebidas",
    "Producción de madera y Fabricación de productos de madera y corcho", "Publicidad / RRPP",
    "Quí­mica", "Restaurantes", "Retail", "Seguridad", "Seguros / Previsión", "Servicios",
    "Servicios Profesionales", "Servicios sociales y de salud", "Siderurgia",
    "Suministro de electricidad, gas y agua", "Tecnologías de la información y Sistemas",
    "Telecomunicaciones", "Textil", "Transporte/Almacenamiento"
]

selected_sectores = st.multiselect("Selecciona hasta 3 sectores", sectores)

# Limitar la selección a un máximo de 3 opciones
if len(selected_sectores) > 3:
    st.error("Puedes seleccionar un máximo de 3 sectores.")


# Pregunta sobre experiencia laboral
st.subheader("Experiencia Laboral")
col12, col13 = st.columns(2)

with col12:
    experiencia = st.selectbox("¿Tiene experiencia laboral?", ["Sí", "No"], key="experiencia")

with col13:
    if experiencia == "Sí":
        tiempo_experiencia = st.number_input("¿Cuánto tiempo de experiencia laboral tiene? (en meses)", min_value=0, key="tiempo_experiencia")
    else:
        # Si selecciona "No", se establece en 0 y se deshabilita el input
        tiempo_experiencia = st.number_input("¿Cuánto tiempo de experiencia laboral tiene? (en meses)", value=0, min_value=0, disabled=True, key="tiempo_experiencia")

# Nueva sección "SKILL ASSESMENT"
st.header("SKILL ASSESMENT")

# Función para manejar la redirección
def redirect():
    st.experimental_set_query_params(page="request_2")

# Botón para redirigir a otra ventana llamada "request_2.py"
st.button("Ir a SKILL ASSESMENT", on_click=redirect)

# Mostrar valores de sesión (opcional)
st.write("First name:", st.session_state.first_name)
st.write("Last name:", st.session_state.last_name)
st.write("Edad:", st.session_state.edad)
st.write("Correo:", st.session_state.correo)
st.write("Nivel Educativo:", st.session_state.nivel_educativo)
st.write("¿Tiene tarjeta CONADIS?", st.session_state.conadis)
st.write("Género:", st.session_state.genero)
st.write("Tipo de Discapacidad:", st.session_state.discapacidad)
st.write("Departamento:", selected_dep if selected_dep != default_dep else 'No seleccionado')
st.write("Provincia:", selected_prov if selected_prov != default_prov else 'No seleccionada')
st.write("Distrito:", selected_dist if selected_dist != default_dist else 'No seleccionado')
st.write("Sectores Preferentes:", selected_sectores)
st.write("¿Tiene experiencia laboral?", st.session_state.experiencia)
st.write("Tiempo de experiencia laboral (meses):", tiempo_experiencia if experiencia == "Sí" else 0)

# Recopilar los datos en un diccionario
data_dict = {
    "First name": st.session_state.first_name,
    "Last name": st.session_state.last_name,
    "Edad": st.session_state.edad,
    "Correo": st.session_state.correo,
    "Nivel Educativo": st.session_state.nivel_educativo,
    "Género": st.session_state.genero,
    "Departamento": selected_dep if selected_dep != default_dep else 'No seleccionado',
    "Provincia": selected_prov if selected_prov != default_prov else 'No seleccionada',
    "Distrito": selected_dist if selected_dist != default_dist else 'No seleccionado',
    "¿Tiene tarjeta CONADIS?": st.session_state.conadis,
    "Tipo de Discapacidad": st.session_state.discapacidad,
    "Sectores Preferentes": ', '.join(selected_sectores),
    "¿Tiene experiencia laboral?": st.session_state.experiencia,
    "Tiempo de experiencia laboral (meses)": tiempo_experiencia if experiencia == "Sí" else 0
}

# Crear un DataFrame a partir del diccionario
data_df = pd.DataFrame([data_dict])

# Mostrar el DataFrame
st.dataframe(data_df)

# Mostrar valores de sesión (opcional)
st.write(data_df)