import streamlit as st
if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Registrarse", "Skill Assesment","Recomendaciones Principales","Otras Recomendaciones"]

def login():
    st.header("Bienvenido")
    role = st.selectbox("Registrate", ROLES[:2])
    if st.button("Aceptar"):
        st.session_state.role = role
        st.rerun()

def logout():
    st.session_state.role = None
    st.rerun()

role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")

request_1 = st.Page(
    "request/request_1.py",
    title="Registrarse",
    icon=":material/app_registration:",
    default=(role == "Registrarse"),
)

request_2 = st.Page(
    "request/request_2.py", 
    title="Skill Assesment", 
    icon=":material/bug_report:", 
    default=(role == "Skill Assesment")
)
request_3 = st.Page(
    "respond/respond_1.py",
    title="Recomendaciones Principales",
    icon=":material/healing:",
    default=(role == "Recomendaciones Principales"),
)

request_4 = st.Page(
    "respond/respond_2.py", 
    title="Otras recomendaciones", 
    icon=":material/handyman:",
    default=(role == "Otras Recomendaciones")
)

account_pages = [logout_page, settings]
request_pages = [request_1]
request_pages2 = [request_1, request_2]
request_pages3 = [request_1,request_2,request_3,request_4]

st.title("SISTEMA DE RECOMENDACIÓN")
st.logo("images/logo_TAW.png", icon_image="images/icon_data.png")

page_dict = {}
if st.session_state.role == "Registrarse":
    page_dict["Información"] = request_pages
if st.session_state.role == "Skill Assesment":
    page_dict["Skill Assesment"] = request_pages2
if st.session_state.role == "Recomendaciones Principales":
    page_dict["Recomendaciones Principales"] = request_pages3


if len(page_dict) > 0:
    pg = st.navigation({"Cuenta": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()