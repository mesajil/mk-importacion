import streamlit as st
import zipfile
import io
from datetime import datetime

from utils import read_excel_skip_rows, select_columns, dataframe_to_csv_string

st.set_page_config(page_title="XLSX a CSV ZIP", layout="centered")

st.title("📊 Conversor XLSX → CSV (ZIP)")
st.write("Sube un archivo .xlsx y descarga un ZIP con 4 CSV personalizados.")

uploaded_file = st.file_uploader("Selecciona un archivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        # Leer Excel sin las primeras 6 filas
        df = read_excel_skip_rows(uploaded_file, skip_rows=6)

        # Configuración de columnas por archivo
        column_sets = {
            1: [0, 1],  # A, B
            2: [0, 4, 5],  # A, E, F
            3: [0, 2],  # A, C
            4: [0, 3],  # A, D
        }

        today = datetime.now().strftime("%d-%m-%y")
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for i, cols in column_sets.items():
                filtered_df = select_columns(df, cols)
                csv_content = dataframe_to_csv_string(filtered_df)

                filename = f"{today}-{i}.csv"
                zip_file.writestr(filename, csv_content)

        zip_buffer.seek(0)

        st.success("✅ Archivos generados correctamente")

        st.download_button(
            label="⬇️ Descargar ZIP",
            data=zip_buffer,
            file_name=f"{today}-csvs.zip",
            mime="application/zip",
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
