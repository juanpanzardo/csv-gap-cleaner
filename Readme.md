# CSV GAP Cleaner

Esta es una aplicación creada con [Streamlit](https://streamlit.io/) que permite transformar archivos CSV generados desde sistemas de ventas offline.

### ✅ Funcionalidades:

- Convierte la columna **Fecha** al formato `MM/DD/YYYY HH:MM`
- Elimina columnas innecesarias: `Telefono`, `RUT`, `Descuento`
- Filtra filas sin valor en la columna **Mail**
- Elimina filas con valores negativos en la columna **Total**
- Permite descargar el archivo CSV procesado directamente desde la app

### 📤 ¿Cómo usarla?

1. Subí tu archivo `.csv` original (con separador `;`)
2. Esperá unos segundos mientras se procesa
3. Descargá el archivo limpio y listo para usar

---

### 🚀 Probar la aplicación

[![Abrir en Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://csv-gap-cleaner.streamlit.app)

> ⚠️ Si el botón aún no funciona, asegurate de que ya hayas desplegado la app en [Streamlit Cloud](https://streamlit.io/cloud)

---

### 📁 Estructura esperada del archivo de entrada

El archivo original debe incluir al menos estas columnas:

- `Fecha` (en formato `DD/MM/YYYY HH:MM:SS`)
- `Código`
- `Nombre`
- `Mail`
- `Total`
- (y opcionalmente: `Telefono`, `RUT`, `Descuento`)

---

### 🧱 Requisitos para correr localmente

Si querés correr esta app localmente:

```bash
pip install -r requirements.txt
streamlit run app.py