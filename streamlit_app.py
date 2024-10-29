import streamlit as st

if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Registrarse", "Iniciar Sesión"]


def login():

    st.header("Bienvenido")
    role = st.selectbox("Inicia Sesion o Registrate", ROLES)

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
    "request/request_2.py", title="Skill Assesment", icon=":material/bug_report:"
)
respond_1 = st.Page(
    "respond/respond_1.py",
    title="Respond 1",
    icon=":material/healing:",
    default=(role == "Iniciar Sesión"),
)


respond_2 = st.Page(
    "respond/respond_2.py", title="Respond 2", icon=":material/handyman:"
)


account_pages = [logout_page, settings]
request_pages = [request_1, request_2]
respond_pages = [respond_1, respond_2]


st.title("SISTEMA DE RECOMENDACIÓN")
st.logo("images/logo_TAW.png", icon_image="images/icon_blue.png")

page_dict = {}
if st.session_state.role in ["Registrarse", "Admin"]:
    page_dict["Request"] = request_pages
if st.session_state.role in ["Iniciar Sesión", "Admin"]:
    page_dict["Respond"] = respond_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()