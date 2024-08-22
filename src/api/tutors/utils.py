from io import (
    StringIO,
)  # StringIO makes us use a string as a file, so we can call read/write methods
import pandas as pd

from src.api.exceptions import InvalidCsv
from src.api.tutors.exceptions import TutorDuplicated


class TutorCsvFile:

    def __init__(self, csv):
        self._df = self._create_csv_df(csv)

    def _create_csv_df(self, csv: str):
        """
        Checks is the columns are the expected ones
        """
        file = StringIO(csv)
        df = pd.read_csv(file)
        self._validate_csv_headers(df)
        self._check_duplicates(df)
        return df

    def _validate_csv_headers(self, df):
        """
        Checks is the columns are the expected ones
        """
        if list(df.columns.values) != ["NOMBRE", "APELLIDO", "DNI", "MAIL"]:
            raise InvalidCsv("Columns don't match with expected ones")

    def _check_duplicates(self, df):
        """
        Checks for duplicated rows
        """
        duplicate = df[df.duplicated()]
        if len(duplicate) > 0:
            raise TutorDuplicated("Duplicate values inside the csv file")

    def get_info_as_rows(self):
        """
        Append a row to a list of rows and return it
        """
        rows = []
        self._df.apply(
            lambda row: rows.append(
                (row["NOMBRE"], row["APELLIDO"], row["DNI"], row["MAIL"])
            ),
            axis=1,
        )

        return rows
