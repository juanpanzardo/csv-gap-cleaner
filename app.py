import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Procesador de CSV - Ventas GAP")

uploaded_file = st.file_uploader("Subí tu archivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=";")

    # Normalizamos los nombres por si hay espacios
    df.columns = df.columns.str.strip()

    # 1. Reformat Fecha
    df['Fecha'] = pd.to_datetime(df['Fecha'], format="%d/%m/%Y %H:%M:%S", errors='coerce')
    df['Fecha'] = df['Fecha'].dt.strftime("%m/%d/%Y %H:%M")

    # 2. Eliminar columnas no deseadas
    columnas_a_eliminar = ['Telefono', 'RUT', 'Descuento']
    columnas_presentes = [col for col in columnas_a_eliminar if col in df.columns]
    df.drop(columns=columnas_presentes, inplace=True)

    # 3. Eliminar filas sin Mail
    df = df[df['Mail'].notna() & (df['Mail'].astype(str).str.strip() != "")]

    # 4. Eliminar filas con Total negativo
    if 'Total' in df.columns:
        df = df[df['Total'] >= 0]

    # 5. Generar archivo descargable
    output = BytesIO()
    df.to_csv(output, index=False, sep=";")
    output.seek(0)

    st.success("Archivo procesado correctamente.")
    st.download_button(
        label="📥 Descargar archivo limpio",
        data=output,
        file_name="Offline Gap.csv",
        mime="text/csv"
    )