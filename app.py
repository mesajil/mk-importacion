import streamlit as st
import pandas as pd
from datetime import datetime
import zipfile
import io

st.set_page_config(page_title="XLSX a CSV ZIP", layout="centered")

st.title("📊 Conversor XLSX → CSV (ZIP)")
st.write("Sube un archivo .xlsx y descarga un ZIP con 4 archivos CSV.")

uploaded_file = st.file_uploader("Selecciona un archivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Leer el archivo Excel (primera hoja)
        df = pd.read_excel(uploaded_file)

        # Fecha actual DD-MM-YY
        today = datetime.now().strftime("%d-%m-%y")

        # Crear ZIP en memoria
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for i in range(1, 5):
                filename = f"{today}-{i}.csv"

                # Convertir DataFrame a CSV en memoria
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False, sep=",")
                csv_content = csv_buffer.getvalue()

                # Agregar al ZIP
                zip_file.writestr(filename, csv_content)

        zip_buffer.seek(0)

        st.success("✅ Conversión completada")

        st.download_button(
            label="⬇️ Descargar ZIP",
            data=zip_buffer,
            file_name=f"{today}-csvs.zip",
            mime="application/zip",
        )

    except Exception as e:
        st.error(f"❌ Error procesando el archivo: {e}")
