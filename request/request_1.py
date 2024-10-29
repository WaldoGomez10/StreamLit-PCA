import streamlit as st
import pandas as pd

# Inicializa los atributos en session_state si no existen
if "datos" not in st.session_state:
    st.session_state.datos = pd.DataFrame(columns=[
        "First name", "Last name", "Edad", "Correo", "Nivel Educativo",
        "Género", "Departamento", "Provincia", "Distrito",
        "¿Tiene tarjeta CONADIS?", "Tipo de Discapacidad",
        "Sectores Preferentes", "¿Tiene experiencia laboral?",
        "Tiempo de experiencia laboral (meses)"
    ])

educacion_values = [
    "Sin Educación Formal",
    "Educación Primaria",
    "Educación Secundaria",
    "Educación Especial",
    "Educación Técnica",
    "Educación Universitaria",
    "Estudios de Maestría",
    "Estudios de Doctorado"
]

# Título de la sección "INFORMACIÓN GENERAL"
st.header("INFORMACIÓN GENERAL")

# Primera fila
col1, col2 = st.columns(2)
col1.text_input("First names", key="first_name")
col2.text_input("Last names", key="last_name")

# Segunda fila
col3, col4 = st.columns(2)
col3.number_input("Edad", min_value=0, key="edad")
col4.text_input("Correo", key="correo")

# Tercera fila
col5, col6 = st.columns(2)
col5.selectbox("Selecciona tu nivel educativo:", educacion_values, key="nivel_educativo")
col6.selectbox("Género", ["Femenino", "Masculino", "Otro"], key="genero")

# Leer el CSV
df = pd.read_csv('datos/distritos.csv', sep=";")

# Crear un diccionario para almacenar las provincias y distritos
data = {}

# Llenar el diccionario
for i, row in df.iterrows():
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
    selected_dep = st.selectbox("Departamento", [default_dep] + list(data.keys()), key="selected_dep")

# Seleccionar provincia
with col8:
    if selected_dep != default_dep:
        provincias = list(data[selected_dep].keys())
        selected_prov = st.selectbox("Provincia", [default_prov] + provincias, key="selected_prov")
    else:
        selected_prov = default_prov  # Mantener en el valor por defecto

# Seleccionar distrito
with col9:
    if selected_dep != default_dep and selected_prov != default_prov:
        distritos = data[selected_dep][selected_prov]
        selected_dist = st.selectbox("Distrito", [default_dist] + distritos, key="selected_dist")
    else:
        selected_dist = default_dist  # Mantener en el valor por defecto

# Conadis y Tipo de Discapacidad
col10, col11 = st.columns(2)
col10.selectbox("¿Tiene tarjeta CONADIS?", ["Sí", "No"], key="conadis")
col11.selectbox("¿Qué tipo de Discapacidad tiene?", ["Discapacidad Física o Motora", "Discapacidad Sensorial", 
                                                     "Discapacidad intelectual", "Discapacidad mental o psíquica"], key="discapacidad")

# Título de la sección "INFORMACIÓN LABORAL"
st.header("INFORMACIÓN LABORAL")

# Sector Preferente con máximo 3 selecciones
df2 = pd.read_csv('datos/sector.csv', quotechar='"',sep=";")

# Obtener los valores únicos de la columna "Sector" y eliminar comillas
sectores_unicos = df2['Sector'].unique()
sectores = [sector.strip('"') for sector in sectores_unicos]

selected_sectores = st.multiselect("Selecciona hasta 3 sectores", sectores, key="sectores")

# Limitar la selección a un máximo de 3 opciones
if len(selected_sectores) > 3:
    st.error("Puedes seleccionar un máximo de 3 sectores.")

# Pregunta sobre experiencia laboral
st.subheader("Experiencia Laboral")
col12, col13 = st.columns(2)

# Creación del selectbox
with col12:
    experiencia = st.selectbox("¿Tiene experiencia laboral?", options=["Sí", "No"], index=1, key="experiencia")

with col13:
    if experiencia == "Sí":
        años_experiencia = st.number_input("¿Cuánto tiempo? (meses)", min_value=0, key="años_experiencia")
    else:
        años_experiencia = 0

# Botón para enviar
if st.button("Enviar"):
    # Validar que todos los campos necesarios están llenos
    if (st.session_state.first_name and st.session_state.last_name and 
        st.session_state.edad and st.session_state.correo and 
        st.session_state.nivel_educativo and st.session_state.genero and 
        selected_dep != default_dep and selected_prov != default_prov and 
        selected_dist != default_dist and st.session_state.conadis and 
        st.session_state.discapacidad and selected_sectores and 
        (st.session_state.experiencia == "Sí" and años_experiencia > 0 or st.session_state.experiencia == "No")):

        # Crear el nuevo registro
        new_data = {
            "First name": st.session_state.first_name,
            "Last name": st.session_state.last_name,
            "Edad": st.session_state.edad,
            "Correo": st.session_state.correo,
            "Nivel Educativo": st.session_state.nivel_educativo,
            "Género": st.session_state.genero,
            "Departamento": selected_dep,
            "Provincia": selected_prov,
            "Distrito": selected_dist,
            "¿Tiene tarjeta CONADIS?": st.session_state.conadis,
            "Tipo de Discapacidad": st.session_state.discapacidad,
            "Sectores Preferentes": ", ".join(selected_sectores),
            "¿Tiene experiencia laboral?": st.session_state.experiencia,
            "Tiempo de experiencia laboral (meses)": años_experiencia
        }

        # Agregar el nuevo registro al DataFrame en session_state
        st.session_state.datos = pd.concat([st.session_state.datos, pd.DataFrame([new_data])], ignore_index=True)

        # Mostrar el DataFrame
        st.write("Datos recopilados:")
        st.dataframe(st.session_state.datos)

        # Confirmación de envío
        st.success("Datos enviados correctamente.")
        
        # Marcar como enviado
        st.session_state.submitted = True

    else:
        st.error("Por favor completa todos los campos.")

if st.button("Ir a Skill Assesment"):
    st.session_state.role = "Skill Assesment"
    st.rerun()