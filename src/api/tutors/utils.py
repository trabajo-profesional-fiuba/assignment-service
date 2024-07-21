from io import StringIO
import pandas as pd

from src.api.tutors.exceptions import InvalidTutorCsv, TutorDuplicated


class TutorCsvFile:

    def __init__(self, csv):
        self._df = self._create_csv_df(csv)

    def _create_csv_df(self, csv: str):
        file = StringIO(csv)
        df = pd.read_csv(file)
        self._validate_csv_headers(df)
        self._check_duplicates(df)
        return df

    def _validate_csv_headers(self, df):
        if list(df.columns.values) != ["NOMBRE", "APELLIDO", "DNI", "MAIL"]:
            raise InvalidTutorCsv("Columns don't match with expected ones")
    
    def _check_duplicates(self, df):
        duplicate = df[df.duplicated()]
        if len(duplicate) > 0:
            raise TutorDuplicated("Duplicate values inside the csv file")

    def get_info_as_rows(self):
        rows = []
        self._df.apply(
            lambda row: rows.append(
                (row["NOMBRE"], row["APELLIDO"], row["DNI"], row["MAIL"])
            ),
            axis=1,
        )

        return rows
