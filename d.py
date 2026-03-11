import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página (Debe ser la primera línea de Streamlit)
st.set_page_config(page_title="Visor Macroeconómico", layout="wide", page_icon="📈")

# 2. Carga de datos optimizada (el caché evita que el Excel se lea cada vez que haces clic)
@st.cache_data
def cargar_datos():
    # Cargamos tu base limpia
    df = pd.read_excel('global_imbalances_panel_filled.xlsx', sheet_name=0)
    # Aseguramos que el año sea numérico entero para la gráfica
    df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
    return df

df = cargar_datos()

# 3. Encabezado de la aplicación
st.title("🌍 Explorador de Panel Macroeconómico")
st.markdown("Herramienta interactiva para el análisis de tendencias previas al modelado de la Cuenta Corriente.")
st.divider()

# 4. Barra lateral (Sidebar) para los filtros
st.sidebar.header("⚙️ Controles del Gráfico")

# Selector de Países
paises_unicos = sorted(df['iso3'].dropna().unique())
# Ponemos algunos países clave por defecto para que no aparezca en blanco
paises_seleccionados = st.sidebar.multiselect(
    "1. Selecciona Países a comparar:", 
    options=paises_unicos, 
    default=['USA', 'CHN', 'DEU', 'MEX'] # Puedes cambiar estos defaults
)

# Selector de Variables (Excluimos identificadores)
columnas_no_graficables = ['iso3', 'country', 'year']
variables_graficables = sorted([col for col in df.columns if col not in columnas_no_graficables])

variable_seleccionada = st.sidebar.selectbox(
    "2. Selecciona la Variable Macro:", 
    options=variables_graficables
)

# 5. Área principal: Generación del gráfico
if not paises_seleccionados:
    st.info("👈 Por favor, selecciona al menos un país en la barra lateral para comenzar.")
else:
    # Filtramos la base según los países elegidos
    df_filtrado = df[df['iso3'].isin(paises_seleccionados)]
    
    # Quitamos años donde la variable seleccionada esté vacía para no graficar huecos raros
    df_filtrado = df_filtrado.dropna(subset=[variable_seleccionada, 'year'])

    # Creamos el gráfico interactivo con Plotly
    fig = px.line(
        df_filtrado, 
        x='year', 
        y=variable_seleccionada, 
        color='iso3',
        markers=True,
        title=f"Evolución de: {variable_seleccionada}",
        template="simple_white" # Un tema muy limpio y profesional
    )
    
    # Mejoramos el formato de los ejes y la leyenda
    fig.update_layout(
        xaxis_title="Año",
        yaxis_title="Valor",
        hovermode="x unified", # Muestra una línea vertical con todos los datos de ese año
        legend_title="País (ISO-3)",
        font=dict(size=14)
    )

    # Mostramos el gráfico ocupando todo el ancho
    st.plotly_chart(fig, use_container_width=True)
    
    # Opcional: Mostrar la tabla de datos crudos debajo del gráfico
    with st.expander("Ver tabla de datos subyacente"):
        # Mostramos la tabla pivoteada para que sea fácil de leer
        tabla_resumen = df_filtrado.pivot(index='year', columns='iso3', values=variable_seleccionada)
        st.dataframe(tabla_resumen.sort_index(ascending=False))
