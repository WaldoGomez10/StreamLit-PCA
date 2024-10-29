import streamlit as st

if "role" not in st.session_state:
    st.session_state.role = None

if "page" not in st.session_state:
    st.session_state.page = "request_1"  # Página inicial

ROLES = [None, "Registrarse", "Iniciar Sesión"]

def login():
    st.header("Bienvenido")
    role = st.selectbox("Inicia Sesion o Registrate", ROLES)
    if st.button("Aceptar"):
        st.session_state.role = role
        st.session_state.page = "request_1"  # Resetear página a request_1 al iniciar sesión o registrarse
        st.rerun()

def logout():
    st.session_state.role = None
    st.rerun()

role = st.session_state.role

# Páginas de la cuenta y configuración
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")

# Páginas de la sección "Registrarse"
request_1 = st.Page(
    "request/request_1.py",
    title="Registrarse",
    icon=":material/app_registration:",
    default=(role == "Registrarse" and st.session_state.page == "request_1"),
)

request_2 = st.Page(
    "request/request_2.py",
    title="Skill Assessment",
    icon=":material/bug_report:",
    default=(role == "Registrarse" and st.session_state.page == "request_2"),
)

# Páginas de la sección "Iniciar Sesión"
respond_1 = st.Page(
    "respond/respond_1.py",
    title="Recomendaciones Principales",
    icon=":material/healing:",
    default=(role == "Iniciar Sesión"),
)

respond_2 = st.Page(
    "respond/respond_2.py", title="Otras recomendaciones", icon=":material/handyman:"
)

# Definir las páginas de cada sección
account_pages = [logout_page, settings]
request_pages = [request_1, request_2]
respond_pages = [respond_1, respond_2]

# Título y logo de la aplicación
st.title("SISTEMA DE RECOMENDACIÓN")
st.logo("images/logo_TAW.png", icon_image="images/icon_data.png")

# Crear el diccionario de páginas
page_dict = {}
if st.session_state.role in ["Registrarse"]:
    page_dict["Información"] = request_pages
if st.session_state.role in ["Iniciar Sesión"]:
    page_dict["Recomendaciones"] = respond_pages

# Configurar la navegación
if len(page_dict) > 0:
    pg = st.navigation({"Cuenta": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()