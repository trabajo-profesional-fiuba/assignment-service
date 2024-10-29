from io import StringIO
import pandas as pd

from src.api.exceptions import InvalidCsv


class StudentCsvFile:

    def __init__(self, csv):
        self._df = self._create_csv_df(csv)

    def _create_csv_df(self, csv: str):
        """A partir de un csv como string, lo trata como archivo y crea un dataframe"""
        file = StringIO(csv)
        df = pd.read_csv(file)
        self._validate_csv_headers(df)
        return df

    def _validate_csv_headers(self, df):
        """Valida que las columnas del csv sean las esperadas"""

        if list(df.columns.values) != ["NOMBRE", "APELLIDO", "PADRON", "MAIL"]:
            raise InvalidCsv("Columns don't match with expected ones")

    def get_info_as_rows(self):
        """Colecta la informacion de cada fila del csv en una lista"""

        rows = []
        self._df.apply(
            lambda row: rows.append(
                (row["NOMBRE"], row["APELLIDO"], row["PADRON"], row["MAIL"])
            ),
            axis=1,
        )

        return rows
