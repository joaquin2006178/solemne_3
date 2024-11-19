# -*- coding: utf-8 -*-
"""Solemne 3

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17EC8eFnPZZcXlbFZMwXB7-1pEghtP0S8
"""

# Importar bibliotecas necesarias
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# Función para obtener datos de la API REST
@st.cache_data
def obtener_datos_api():
    url = "https://restcountries.com/v3.1/all"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        return datos
    else:
        st.error("No se pudieron obtener los datos de la API.")
        return None

# Función para procesar datos
def procesar_datos(datos):
    lista_paises = []
    for pais in datos:
        lista_paises.append({
            "Pais": pais.get("name", {}).get("common", "Desconocido"),
            "Continente": pais.get("region", "Desconocido"),
            "Poblacion": pais.get("population", 0),
            "Area": pais.get("area", 0),
            "Fronteras": len(pais.get("borders", [])),
            "Idiomas": len(pais.get("languages", {})),
            "Zonas horarias": len(pais.get("timezones", []))
        })
    return pd.DataFrame(lista_paises)

# Obtener y procesar los datos
datos_api = obtener_datos_api()
df_paises = procesar_datos(datos_api) if datos_api else pd.DataFrame()

# Configurar la estructura de la aplicación
st.title("Solemne 3 = Manipulación y funciones de Streamlit")
st.title("")
st.title("Datos de Países")
st.sidebar.title("Navegación")
pagina_seleccionada = st.sidebar.selectbox("Seleccione una página", ["Descripción", "Interacción con Datos", "Visualización Gráfica"])

# Página de Descripción
if pagina_seleccionada == "Descripción":
    st.header("Descripción del Proyecto")
    st.write("Esta aplicación web muestra datos de países obtenidos de una API pública.")
    st.write("Puedes explorar los datos, realizar análisis y visualizar gráficos.")

# Página de Interacción con Datos
elif pagina_seleccionada == "Interacción con Datos":
    st.header("Interacción con los Datos")
    st.write("Vista previa de los datos de países:")
    st.dataframe(df_paises)

    # Selección de columna y cálculos estadísticos
    columna_seleccionada = st.selectbox("Seleccione una columna para análisis estadístico", df_paises.select_dtypes(include=['float64', 'int']).columns)
    if columna_seleccionada:
        media = df_paises[columna_seleccionada].mean()
        mediana = df_paises[columna_seleccionada].median()
        desviacion = df_paises[columna_seleccionada].std()
        st.write(f"Media de {columna_seleccionada}: {media}")
        st.write(f"Mediana de {columna_seleccionada}: {mediana}")
        st.write(f"Desviación estándar de {columna_seleccionada}: {desviacion}")

    # Ordenar los datos
    ordenar_por = st.selectbox("Seleccione una columna para ordenar", df_paises.columns)
    orden_ascendente = st.checkbox("Orden ascendente", value=True)
    df_ordenado = df_paises.sort_values(by=ordenar_por, ascending=orden_ascendente)
    st.dataframe(df_ordenado)

    # Botón para descargar los datos filtrados
    def convertir_csv(df):
        return df.to_csv(index=False).encode("utf-8")

    csv = convertir_csv(df_ordenado)
    st.download_button("Descargar datos ordenados en CSV", data=csv, file_name="datos_ordenados.csv", mime="text/csv")

# Página de Visualización Gráfica
elif pagina_seleccionada == "Visualización Gráfica":
    st.header("Visualización Interactiva")
    tipo_grafico = st.selectbox("Seleccione el tipo de gráfico", ["Barra", "Dispersión", "Histograma"])
    x_var = st.selectbox("Seleccione el eje X", df_paises.columns)
    y_var = st.selectbox("Seleccione el eje Y", df_paises.select_dtypes(include=['float64', 'int']).columns)

    if tipo_grafico == "Barra":
        # Filtrar un máximo de 20 valores para evitar sobrecargar el gráfico porque si no falla :)
        df_paises_filtrado = df_paises.head(20)
        fig, ax = plt.subplots()
        ax.bar(df_paises_filtrado[x_var], df_paises_filtrado[y_var])
        ax.set_xlabel(x_var)
        ax.set_ylabel(y_var)
        plt.xticks(rotation=45)  # Rotar etiquetas del eje X
        st.pyplot(fig)

    elif tipo_grafico == "Dispersión":
        fig, ax = plt.subplots()
        ax.scatter(df_paises[x_var], df_paises[y_var])
        ax.set_xlabel(x_var)
        ax.set_ylabel(y_var)
        st.pyplot(fig)

    elif tipo_grafico == "Histograma":
        fig, ax = plt.subplots()
        ax.hist(df_paises[y_var], bins=20)
        ax.set_xlabel(y_var)
        st.pyplot(fig)

    # Botón para descargar el gráfico
    fig.savefig("grafico.png", format="png")
    with open("grafico.png", "rb") as file:
        st.download_button(
            label="Descargar gráfico en PNG",
            data=file,
            file_name="grafico.png",
            mime="image/png"
        )