import streamlit as st
import pandas as pd

# Inicializa los atributos en session_state si no existen
if "datos" not in st.session_state:
    st.session_state.datos = pd.DataFrame(columns=[
        "First name", "Last name", "Edad", "Correo", "Nivel Educativo",
        "Género", "Departamento", "Provincia", "Distrito",
        "¿Tiene tarjeta CONADIS?", "Tipo de Discapacidad",
        "Sectores Preferentes", "¿Tiene experiencia laboral?",
        "Tiempo de experiencia laboral (meses)", "Skills"
    ])

if "skills" not in st.session_state:
    st.session_state.skills = []

# Valores para el nivel educativo
educacion_values = [
    "Sin Educación Formal", "Educación Primaria", "Educación Secundaria",
    "Educación Especial", "Educación Técnica", "Educación Universitaria",
    "Estudios de Maestría", "Estudios de Doctorado"
]

# Título de la sección "INFORMACIÓN GENERAL"
st.header("INFORMACIÓN GENERAL")

# Inputs de información general
col1, col2 = st.columns(2)
col1.markdown("🧑‍🎓 Nombres")
col1.text_input("",key="first_name")
col2.text_input("Apellidos", key="last_name")
col3, col4 = st.columns(2)
col3.number_input("Edad", min_value=0, key="edad")
col4.text_input("Correo", key="correo")
col5, col6 = st.columns(2)
col5.selectbox("Selecciona tu nivel educativo:", educacion_values, key="nivel_educativo")
col6.selectbox("Sexo", ["Femenino", "Masculino"], key="genero")

st.write("¿Donde vive?")
# Leer el CSV y crear el diccionario de provincias y distritos
df = pd.read_csv('datos/distritos.csv', sep=";")
data = {}
for _, row in df.iterrows():
    dep = row['DEPARTAMENTO']
    prov = row['PROVINCIA']
    dist = row['DISTRITO']
    if dep not in data:
        data[dep] = {}
    if prov not in data[dep]:
        data[dep][prov] = []
    data[dep][prov].append(dist)

# Inputs de ubicación
col7, col8, col9 = st.columns(3)
selected_dep = col7.selectbox("Departamento", ["Selecciona un Departamento"] + list(data.keys()), key="selected_dep")
if selected_dep and selected_dep != "Selecciona un Departamento":
    provincias = list(data[selected_dep].keys())
    selected_prov = col8.selectbox("Provincia", ["Selecciona una Provincia"] + provincias, key="selected_prov")
    if selected_prov and selected_prov != "Selecciona una Provincia":
        distritos = data[selected_dep][selected_prov]
        selected_dist = col9.selectbox("Distrito", ["Selecciona un Distrito"] + distritos, key="selected_dist")
    else:
        selected_dist = "Selecciona un Distrito"
else:
    selected_prov, selected_dist = "Selecciona una Provincia", "Selecciona un Distrito"

# Inputs adicionales
col10, col11 = st.columns(2)
col10.selectbox("¿Está inscrito en CONADIS?", ["Sí", "No"], key="conadis")
col11.selectbox("¿Qué tipo de Discapacidad tiene?", [
    "Discapacidad Física o Motora", "Discapacidad Sensorial",
    "Discapacidad intelectual", "Discapacidad mental o psíquica"
], key="discapacidad")

# Título de la sección "INFORMACIÓN LABORAL"
st.header("INFORMACIÓN LABORAL")

# Sectores preferentes
df2 = pd.read_csv('datos/sector.csv', sep=";")
sectores = df2['Sector'].str.strip('"').unique().tolist()
selected_sectores = st.multiselect("Selecciona hasta 3 sectores", sectores, key="sectores")
if len(selected_sectores) > 3:
    st.error("Puedes seleccionar un máximo de 3 sectores.")

# Experiencia laboral
st.subheader("Experiencia Laboral")
col12, col13 = st.columns(2)
experiencia = col12.selectbox("¿Tiene experiencia laboral?", ["Sí", "No"], key="experiencia")
años_experiencia = col13.number_input("¿Cuánto tiempo? (meses)", min_value=0, key="años_experiencia") if experiencia == "Sí" else 0

# Botón para enviar
if st.button("Enviar"):
    if all([
        st.session_state.first_name, st.session_state.last_name, st.session_state.edad,
        st.session_state.correo, st.session_state.nivel_educativo, st.session_state.genero,
        selected_dep != "Selecciona un Departamento", selected_prov != "Selecciona una Provincia",
        selected_dist != "Selecciona un Distrito", st.session_state.conadis, st.session_state.discapacidad,
        selected_sectores, (experiencia == "Sí" and años_experiencia > 0) or experiencia == "No"
    ]):
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
            "¿Tiene experiencia laboral?": experiencia,
            "Tiempo de experiencia laboral (meses)": años_experiencia,
            "Skills": ""
        }
        # Guardar en el session_state
        st.session_state.nuevo_dataframe = pd.DataFrame([new_data])

        # Mostrar el DataFrame
        st.write("Datos recopilados:")
        st.dataframe(st.session_state.nuevo_dataframe)

        # Limpiar st.session_state.datos
        st.session_state.datos = pd.DataFrame(columns=st.session_state.datos.columns)

        # Confirmación de envío
        st.success("Datos enviados correctamente.")
        st.session_state.submitted = True  # Marcar como enviado
    else:
        st.error("Por favor completa todos los campos.")


#if "nuevo_dataframe" in st.session_state and not st.session_state.nuevo_dataframe.empty:
#    st.write("Apellidos:", st.session_state.nuevo_dataframe["Last name"])

# Botón para ir a Skill Assesment
if st.button("Ir a Skill Assesment"):
    st.session_state.role = "Skill Assesment"
    st.rerun()
    