import streamlit as st
import pandas as pd
import plotly.express as px

def cargar_datos_excel(ruta_excel):
    """
    Carga un archivo Excel y devuelve un DataFrame. Verifica las columnas.
    """
    try:
        # Cargar Excel con pandas
        df = pd.read_excel(ruta_excel, engine='openpyxl', parse_dates=["Fecha"])
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None

def calcular_ventas_mensuales(df):
    """
    Calcula las Ventas Mensuales agrupando por mes.
    """
    df['Mes'] = df['Fecha'].dt.to_period('M')
    df_ventas = df.groupby('Mes')['MontoVenta'].sum().reset_index()
    df_ventas['Mes'] = df_ventas['Mes'].astype(str)
    df_ventas.columns = ['Mes', 'VentasTotales']
    return df_ventas

def calcular_ganancias_mensuales(df):
    """
    Calcula las Ganancias Mensuales agrupando por mes.
    """
    df['Ganancia'] = df['MontoVenta'] - df['Costo']
    df['Mes'] = df['Fecha'].dt.to_period('M')
    df_ganancias = df.groupby('Mes')['Ganancia'].sum().reset_index()
    df_ganancias['Mes'] = df_ganancias['Mes'].astype(str)
    df_ganancias.columns = ['Mes', 'GananciaTotal']
    return df_ganancias

# Streamlit App
def main():
    st.title("Dashboard de KPIs")
    st.write("Carga un archivo Excel con datos de ventas para calcular los KPIs.")
    
    # Cargar archivo
    archivo_subido = st.file_uploader("Sube tu archivo Excel:", type=["xlsx"])
    
    if archivo_subido:
        # Cargar datos del archivo Excel
        df = cargar_datos_excel(archivo_subido)
        if df is not None:
            st.write("### Vista previa de los datos cargados:")
            st.dataframe(df.head())
            
            # Menú para seleccionar KPI
            kpi_opcion = st.selectbox("Selecciona un KPI:", ["Ventas Mensuales", "Ganancias Mensuales"])
            
            if kpi_opcion == "Ventas Mensuales":
                # Calcular Ventas Mensuales
                df_ventas = calcular_ventas_mensuales(df)
                st.write("### Ventas Mensuales")
                st.dataframe(df_ventas)
                
                # Graficar
                fig = px.bar(df_ventas, x='Mes', y='VentasTotales', title="Ventas Mensuales")
                st.plotly_chart(fig)
            
            elif kpi_opcion == "Ganancias Mensuales":
                # Calcular Ganancias Mensuales
                df_ganancias = calcular_ganancias_mensuales(df)
                st.write("### Ganancias Mensuales")
                st.dataframe(df_ganancias)
                
                # Graficar
                fig = px.bar(df_ganancias, x='Mes', y='GananciaTotal', title="Ganancias Mensuales")
                st.plotly_chart(fig)

if __name__ == "__main__":
    main()
