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

# Inicializa los atributos necesarios en session_state
if "first_name" not in st.session_state:
    st.session_state.first_name = ""
if "last_name" not in st.session_state:
    st.session_state.last_name = ""
if "edad" not in st.session_state:
    st.session_state.edad = ""
if "correo" not in st.session_state:
    st.session_state.correo = ""
if "nivel_educativo" not in st.session_state:
    st.session_state.nivel_educativo = ""
if "genero" not in st.session_state:
    st.session_state.genero = ""
if "conadis" not in st.session_state:
    st.session_state.conadis = ""
if "discapacidad" not in st.session_state:
    st.session_state.discapacidad = ""
if "experiencia" not in st.session_state:
    st.session_state.experiencia = "No"
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Botón para reiniciar los campos
if st.button("Reiniciar"):
    for key in ["first_name", "last_name", "edad", "correo", "nivel_educativo", "genero", "conadis", "discapacidad"]:
        st.session_state[key] = ""
    st.session_state.selected_dep = None
    st.session_state.selected_prov = None
    st.session_state.selected_dist = None
    st.session_state.selected_sectores = []
    st.session_state.experiencia = "No"
    st.session_state.submitted = False  # Resetear el estado de enviado

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
educacion_options = [
    "Sin Educación Formal",
    "Educación Primaria",
    "Educación Secundaria",
    "Educación Especial",
    "Educación Técnica",
    "Educación Universitaria",
    "Estudios de Maestría",
    "Estudios de Doctorado"
]

col5, col6 = st.columns(2)
col5.selectbox("Selecciona tu nivel educativo:", [default_educacion] + educacion_options, key="nivel_educativo")
col6.selectbox("Género", ["Femenino", "Masculino", "Otro"], key="genero")

# Leer el CSV
df = pd.read_csv('datos/distritos.csv', sep=";")

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
        años_experiencia = st.number_input("¿Cuántos años de experiencia tiene?", min_value=0, key="años_experiencia")
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
            "Sectores Preferentes": ', '.join(selected_sectores),
            "¿Tiene experiencia laboral?": st.session_state.experiencia,
            "Tiempo de experiencia laboral (meses)": años_experiencia if st.session_state.experiencia == "Sí" else 0
        }

        # Agregar el nuevo registro al DataFrame en session_state
        st.session_state.datos = pd.concat([st.session_state.datos, pd.DataFrame([new_data])], ignore_index=True)

        # Mostrar el DataFrame
        st.write("Datos recopilados:")
        st.dataframe(st.session_state.datos)

        # Establecer que el formulario fue enviado
        st.session_state.submitted = True
        st.success("Datos enviados y campos reiniciados.")
        
    else:
        st.error("Por favor, complete todos los campos obligatorios.")

# Reiniciar campos si el formulario fue enviado
if st.session_state.submitted:
    # No reiniciar los campos aquí ya que ya fueron reiniciados al hacer click en el botón "Reiniciar"
    st.session_state.submitted = False  # Resetear para futuras entradas