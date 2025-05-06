import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="CSV GAP Cleaner", layout="centered")
st.title("🧼 CSV GAP Cleaner")
st.write("Subí tu archivo `.csv` de ventas offline y descargá una versión limpia.")

uploaded_file = st.file_uploader("📤 Seleccioná el archivo CSV", type=["csv"])

if uploaded_file is not None:
    # Leer CSV original
    df = pd.read_csv(uploaded_file, sep=";")

    st.subheader("📄 Vista previa del archivo original")
    st.dataframe(df.head(10))

    # Asegurarse de que los nombres de columnas estén limpios
    df.columns = df.columns.str.strip()

    # ✅ LIMPIEZA ROBUSTA DE FECHA
    st.write("📅 Fechas originales:")
    st.write(df['Fecha'].head(5))

    try:
        # 1. Convertir a texto y limpiar variaciones de AM/PM
        df['Fecha'] = df['Fecha'].astype(str)
        df['Fecha'] = df['Fecha'].str.replace(r"a\.?\s?m\.?", "", regex=True)
        df['Fecha'] = df['Fecha'].str.replace(r"p\.?\s?m\.?", "", regex=True)
        df['Fecha'] = df['Fecha'].str.replace(r"AM|PM|am|pm", "", regex=True)

        # 2. Remover espacios dobles y caracteres invisibles
        df['Fecha'] = df['Fecha'].str.replace(u"\xa0", " ", regex=False)
        df['Fecha'] = df['Fecha'].str.replace("\n", " ", regex=False)
        df['Fecha'] = df['Fecha'].str.replace("  ", " ", regex=False)
        df['Fecha'] = df['Fecha'].str.strip()

        # 3. Mostrar antes de convertir
        st.write("🛠️ Después de limpieza pero antes de convertir:")
        st.write(df['Fecha'].head(5))

        # 4. Convertir a datetime
        df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True, errors='coerce')
        df['Fecha'] = df['Fecha'].dt.strftime("%m/%d/%Y %H:%M")

        st.success("✅ Fechas convertidas correctamente.")
        st.write("🆕 Fechas convertidas:")
        st.write(df['Fecha'].head(5))

    except Exception as e:
        st.error(f"⚠️ Error al convertir fechas: {e}")

    # ✅ ELIMINAR COLUMNAS INNECESARIAS
    columnas_a_eliminar = ['Telefono', 'RUT', 'Descuento']
    columnas_presentes = [col for col in columnas_a_eliminar if col in df.columns]
    df.drop(columns=columnas_presentes, inplace=True)

    # ✅ FILTRAR FILAS SIN MAIL
    df = df[df['Mail'].notna() & (df['Mail'].astype(str).str.strip() != "")]

    # ✅ ELIMINAR FILAS CON TOTAL NEGATIVO
    if 'Total' in df.columns:
        df = df[df['Total'] >= 0]

    # ✅ GENERAR ARCHIVO PARA DESCARGA (sin encabezado)
    output = BytesIO()
    df.to_csv(output, index=False, sep=";", header=False)
    output.seek(0)

    st.subheader("✅ Archivo procesado correctamente")
    st.download_button(
        label="📥 Descargar archivo limpio (Offline Gap.csv)",
        data=output,
        file_name="Offline Gap.csv",
        mime="text/csv"
    )

    st.info("Si ves algo incorrecto, revisá el formato de la columna Fecha o los encabezados del archivo original.")