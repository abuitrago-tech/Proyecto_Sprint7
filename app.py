# Cargar liberias
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Cargar datos
car_data = pd.read_csv('vehicles_us.csv')
car_data["type"] = car_data["type"].astype(str)

# Poner título
st.header('Listado de vehículos en venta', divider = "gray")

if "model" in car_data.columns:
    car_data['Fabricante'] = car_data['model'].str.split(' ').str[0].str.split('-').str[0]

st.dataframe(
    car_data,
    use_container_width=True,
    height=600  
)

# Descargar dataset
st.download_button(
    label = "Descargar dataset", 
    data = car_data.to_csv(index=False), 
    file_name = "car_data.csv"
)

st.divider()


# Visualizar histograma 1
fig_fabricantes = px.histogram(
    car_data, 
    x= "Fabricante", 
    color="type",  
    width = 700, 
    height = 600, 
    title= "Tipo de vehículos por fabricante"
)
st.plotly_chart(fig_fabricantes, use_container_width=True)

st.divider()

# Visualizar histograma 2
fig_model_year = px.histogram(
    car_data,
    x= "model_year",
    color="condition",
    width = 700,
    height = 600,
    title= "Condición de Vehículos"
) 
st.plotly_chart(fig_model_year, use_container_width=True)


# Seleccionar 2 variables cualquiera
opciones = list(car_data.columns)[0:14]
v = st.multiselect(
    label = "Seleccione máximo 2 variables:",
    options = opciones,
    max_selections = 2
)

# Ejecutar análisis
analisis_b = st.button(
    label = "Analizar"
)

st.divider()


if analisis_b:
    try:
        if len(v) != 2:
            st.warning("Selecciona exactamente 2 variables para el gráfico de dispersión")
        
        # Visualizar dispersion entre variables
        fig_price = px.scatter(
            car_data,
            x = v[1],
            y = v[0],
            color = "type",
            title = f"Dispersión {v[0]} vs. {v[1]}",
            width = 700,
            height = 400
            ) 
        st.plotly_chart(fig_price, use_container_width=True)

        c1, c2, c3 = st.columns(3)

        with c1: 
            prom = np.mean(car_data[v[0]])
            st.metric(
                    label = "Media",
                    value = "{:.1f}".format(prom)
                )
        with c2:
            med = np.median(car_data[v[0]])
            st.metric(
                    label = "Mediana",
                    value = "{:.1f}".format(med)
                )
        with c3:
            desv = np.std(car_data[v[0]])
            st.metric(
                    label = "Desviación",
                    value = "{:.1f}".format(desv)
                )
    except:
        st.write("App con listado de vehículos en venta") 
