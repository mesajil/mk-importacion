import pandas as pd
import io


def read_excel_skip_rows(file, skip_rows=6):
    """
    Lee el Excel preservando literalmente los valores
    (ceros, decimales, etc.).
    """
    return pd.read_excel(
        file,
        skiprows=skip_rows,
        header=None,
        dtype=str,
        engine="openpyxl",
        keep_default_na=False,
        na_filter=False,
    )


def select_columns(df, column_indexes):
    """
    Selecciona columnas por índice (0=A, 1=B, etc).
    """
    max_index = max(column_indexes)
    if df.shape[1] <= max_index:
        raise ValueError("El archivo no tiene suficientes columnas")
    return df.iloc[:, column_indexes].copy()


def dataframe_to_csv_string(df, delimiter=";"):
    """
    Convierte un DataFrame a CSV en memoria.
    """
    buffer = io.StringIO()
    df.to_csv(buffer, index=False, header=False, sep=delimiter)
    return buffer.getvalue()


def normalize_columns(df, original_indexes):
    """
    Normaliza las columnas según reglas A–F.
    original_indexes indica qué columna original (A=0, B=1, etc.)
    corresponde a cada columna del df filtrado.
    """

    for pos, original_idx in enumerate(original_indexes):
        col = df.iloc[:, pos]

        print(col)

        # Columna A: texto de 6 dígitos
        if original_idx == 0:
            df.iloc[:, pos] = col.astype(str).str.zfill(6)

        # Columna B: limpieza de texto
        elif original_idx == 1:
            df.iloc[:, pos] = (
                col.astype(str)
                .str.replace(r'[,";]', "", regex=True)
                .str.replace("/", "|", regex=False)
            )

        # Columnas C y D: 2 decimales
        elif original_idx in (2, 3):
            df.iloc[:, pos] = (
                col.astype(str)
                .str.replace(",", "", regex=False)
                .apply(lambda x: f"{float(x):.2f}" if x != "" else "")
            )

        # Columnas E y F: 3 decimales
        elif original_idx in (4, 5):
            df.iloc[:, pos] = (
                col.astype(str)
                .str.replace(",", "", regex=False)
                .apply(lambda x: f"{float(x):.3f}" if x != "" else "")
            )

    return df
