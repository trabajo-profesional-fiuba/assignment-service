from io import (
    StringIO,
)  # StringIO makes us use a string as a file, so we can call read/write methods
import pandas as pd

from src.api.exceptions import InvalidCsv
from src.api.tutors.exceptions import TutorDuplicated
from src.core.tutor import Tutor


class TutorCsvFile:

    def __init__(self, csv):
        self._df = self._create_csv_df(csv)

    def _create_csv_df(self, csv: str):
        """
        crea un dataframe a partir de un csv como str
        """
        file = StringIO(csv)
        df = pd.read_csv(file)
        self._validate_csv_headers(df)
        self._check_duplicates(df)
        return df

    def _validate_csv_headers(self, df):
        """
        Checkea las columnas del csv
        """
        if list(df.columns.values) != [
            "NOMBRE",
            "APELLIDO",
            "DNI",
            "MAIL",
            "CAPACIDAD",
        ]:
            raise InvalidCsv("Columns don't match with expected ones")

    def _check_duplicates(self, df):
        """
        Verifica duplicados
        """
        duplicate = df[df.duplicated()]
        if len(duplicate) > 0:
            raise TutorDuplicated("Duplicate values inside the csv file")

    def get_info_as_rows(self):
        """
        Arma una lista de filas con la informacion de las columnas del csv
        """
        rows = []
        self._df.apply(
            lambda row: rows.append(
                (
                    row["NOMBRE"],
                    row["APELLIDO"],
                    row["DNI"],
                    row["MAIL"],
                    row["CAPACIDAD"],
                )
            ),
            axis=1,
        )

        return rows

    def get_tutors_id(self):
        """Obtiene los ids de los tutores del csv"""
        return list(self._df["DNI"].unique())

    def _add_tutor(self, row, tutors):
        """ Crea tutores a partir de los datos de las columnas del csv"""
        tutors[row["DNI"]] = Tutor(
            id=row["DNI"],
            email=row["MAIL"],
            name=row["NOMBRE"],
            last_name=row["APELLIDO"],
            capacity=row["CAPACIDAD"],
        )

    def get_tutors(self) -> dict[str, Tutor]:
        """Obtiene todos los tutores del csv"""
        tutors = {}
        self._df.apply(lambda row: self._add_tutor(row, tutors), axis=1)
        return tutors
