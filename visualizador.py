import streamlit as st
import pandas as pd
import plotly.express as px




def pagina_principal():
    st.title("Visualizador de estadísticas")
    st.write("Usa el menú de la izquierda para navegar entre las opciones")

def Visualizar_datos():
    st.title("Visualización de datos")
    st.write("carga un archivo excel para visualizar los datos de la dependencia")
    archivo_cargado = st.file_uploader("elige un archivo", type="xlsx", key="visualizar")
    
    if archivo_cargado is not None:
        df = pd.read_excel(archivo_cargado)
        st.write("datos del archivo xlsx:")
        st.write(df)
        st.write("Estadistica descriptiva:")
        st.write(df.describe())
        st.write("editar")
        st.data_editor(df, num_rows="dynamic")

def graficos_interactivos():
    st.title("Gráficos")
    st.write("carga un archivo excel para crear gráficos interactivos")
    archivo_cargado = st.file_uploader("elige un archivo", type="xlsx", key="graficos")

    if archivo_cargado is not None:
        df = pd.read_excel(archivo_cargado)
        
        # Contenedor para todos los filtros en la barra lateral
        st.sidebar.header("Filtros")
        
        # Filtro de fechas
        st.sidebar.subheader("Filtros de Fecha")
        columna_fecha = st.sidebar.selectbox(
            "Selecciona la columna de fecha",
            df.select_dtypes(include=['datetime64', 'object']).columns
        )
        
        # Filtro por columna específica
        st.sidebar.subheader("Filtro por Columna")
        # Seleccionar la columna a filtrar
        columna_filtro = st.sidebar.selectbox(
            "Selecciona la columna para filtrar",
            df.columns,
            key="columna_filtro"
        )
        
        # Obtener valores únicos de la columna seleccionada
        valores_unicos = df[columna_filtro].unique()
        # Crear un multiselect para permitir selección múltiple de valores
        valores_seleccionados = st.sidebar.multiselect(
            f"Selecciona valores de {columna_filtro}",
            options=valores_unicos,
            default=valores_unicos
        )
        
        # Aplicar filtro por valores seleccionados
        df_filtrado = df[df[columna_filtro].isin(valores_seleccionados)]
        
        # Filtro de fechas
        try:
            df_filtrado[columna_fecha] = pd.to_datetime(df_filtrado[columna_fecha])
            fecha_min = df_filtrado[columna_fecha].min()
            fecha_max = df_filtrado[columna_fecha].max()
            
            fecha_inicio, fecha_fin = st.sidebar.date_input(
                "Selecciona el rango de fechas",
                [fecha_min.date(), fecha_max.date()],
                min_value=fecha_min.date(),
                max_value=fecha_max.date()
            )
            
            # Aplicar filtro de fechas
            df_filtrado = df_filtrado[
                (df_filtrado[columna_fecha].dt.date >= fecha_inicio) & 
                (df_filtrado[columna_fecha].dt.date <= fecha_fin)
            ]
            
            # Mostrar información de los filtros aplicados
            st.write(f"Mostrando datos desde {fecha_inicio} hasta {fecha_fin}")
            st.write(f"Filtrado por {columna_filtro}: {', '.join(map(str, valores_seleccionados))}")
            
        except Exception as e:
            st.warning(f"No se pudo convertir la columna {columna_fecha} a formato fecha. Por favor, selecciona una columna válida.")
        
        # Mostrar número de registros después del filtrado
        st.write(f"Número de registros después del filtrado: {len(df_filtrado)}")
        
        # Selección de ejes para gráficos
        st.write("Elige una columna para el eje X")
        eje_x = st.selectbox("Eje X", df_filtrado.columns)
        st.write("Elige una columna para el eje Y")
        eje_y = st.selectbox("Eje y", df_filtrado.columns)
        st.write("Elige una columna para diferenciar por colores")
        color = st.selectbox("color", df_filtrado.columns)

        # Botones para crear diferentes tipos de gráficos
        if st.button("Crear Gráfico en barras"):
            fig = px.bar(df_filtrado, x=eje_x, y=eje_y, title=f"{eje_y} por {eje_x}")
            st.plotly_chart(fig)

        if st.button("Crear Gráfico en histograma -solo eje x-"):
            fig = px.histogram(df_filtrado, x=eje_x) 
            st.plotly_chart(fig)

        if st.button("Crear Gráfico comparativo -ejes x, y + color-"):
            fig = px.bar(df_filtrado, x=eje_x, y=eje_y, color=color, 
                        pattern_shape=color, pattern_shape_sequence=[".", "x", "+"])
            st.plotly_chart(fig)

        if st.button("Crear Gráfico torta -eje x= cantidad, color= separación"):
            fig = px.pie(df_filtrado, values=eje_x, names=color, title=color)
            st.plotly_chart(fig)

        # Botón para descargar datos filtrados
        if st.sidebar.button("Descargar Datos Filtrados"):
            csv = df_filtrado.to_csv(index=False)
            st.sidebar.download_button(
                label="Descargar como CSV",
                data=csv,
                file_name="datos_filtrados.csv",
                mime="text/csv")

def main():
    st.sidebar.title("Navegación")
    pagina = st.sidebar.selectbox("selección de dependencia", 
                                 ["Página Principal", "Visualización de datos", "Gráficos"])

    if pagina == "Página Principal":
        pagina_principal()
    elif pagina == "Visualización de datos":
        Visualizar_datos()
    elif pagina == "Gráficos":
        graficos_interactivos()


if __name__ == "__main__":
    main()







   