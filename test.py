import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

df = pd.DataFrame(np.random.randn(10, 3), columns=["a", "b", "c"])
c = (
    alt.Chart(df)
    .mark_circle()
    .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
)

st.write(c)

st.write("Hello word")
st.write("1 + 1 = ", 2)

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

st.table(df)

'''Grafico chart INTERACTIVO'''
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])
st.line_chart(chart_data)


'''Grafico de mapas'''
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

## PARA AGREGAR TEXTO Y PODER ALMACENARLO##
st.text_input("Your name", key="name")

# You can access the value at any point with:
st.session_state.name

#####################################

#Hacer click y cambia de texto
st.button("Reset", type="primary")
if st.button("Say hello"):
    st.write("Why hello there")
else:
    st.write("Goodbye")

#Hacer click y cambia de texto, se le puede agregar acciones
left, middle, right = st.columns(3)
if left.button("Plain button", use_container_width=True,help="Use esto si se siente tal"):
    left.markdown("You clicked the plain button.")
if middle.button("Emoji button", icon="😃"):
    middle.markdown("You clicked the emoji button.")
if right.button("Material button", icon=":material/mood:", use_container_width=True):
    right.markdown("You clicked the Material button.")


#PARA OCULTAR O NO
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data


#PARA TENER OPCIONES
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option
