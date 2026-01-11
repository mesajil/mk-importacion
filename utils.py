import pandas as pd
import io


def read_excel_skip_rows(file, skip_rows=6):
    """
    Lee un archivo Excel ignorando las primeras filas.
    """
    return pd.read_excel(file, skiprows=skip_rows)


def select_columns(df, column_indexes):
    """
    Selecciona columnas por índice (0=A, 1=B, etc).
    """
    max_index = max(column_indexes)
    if df.shape[1] <= max_index:
        raise ValueError("El archivo no tiene suficientes columnas")
    return df.iloc[:, column_indexes]


def dataframe_to_csv_string(df):
    """
    Convierte un DataFrame a CSV en memoria.
    """
    buffer = io.StringIO()
    df.to_csv(buffer, index=False, sep=",")
    return buffer.getvalue()
