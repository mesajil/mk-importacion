import streamlit as st
import zipfile
import io
from datetime import datetime

from utils import (
    read_excel_skip_rows,
    select_columns,
    dataframe_to_csv_string,
    normalize_columns,
)

st.set_page_config(page_title="XLSX a CSV ZIP", layout="centered")
st.title("📊 Conversor XLSX → CSV (ZIP)")

uploaded_file = st.file_uploader("Selecciona un archivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = read_excel_skip_rows(uploaded_file, skip_rows=6)

        column_sets = {
            1: [0, 1],  # A, B
            2: [0, 4, 5],  # A, E, F
            3: [0, 2],  # A, C
            4: [0, 3],  # A, D
        }

        # today = datetime.now().strftime("%d-%m-%y") # Ya no se usa la fecha para el nombre de los archivos generados
        base_name = os.path.splitext(uploaded_file.name)[0]
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for i, cols in column_sets.items():
                filtered_df = select_columns(df, cols)

                normalize_df = normalize_columns(filtered_df, cols)

                csv_content = dataframe_to_csv_string(normalize_df, delimiter=";")

                zip_file.writestr(f"{base_name}{i}.csv", csv_content)

        zip_buffer.seek(0)

        st.success("✅ Archivos generados correctamente")
        st.download_button(
            "⬇️ Descargar ZIP", zip_buffer, f"{base_name}.zip", "application/zip"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")

st.divider()
st.caption("Versión 1.2 · Conversor XLSX → CSV")
