from io import StringIO
import pandas as pd

from src.api.exceptions import InvalidCsv


class TopicCsvFile:

    def __init__(self, csv):
        self._df = self._create_csv_df(csv)

    def _create_csv_df(self, csv: str):
        file = StringIO(csv)
        df = pd.read_csv(file)
        self._validate_csv_headers(df)
        return df

    def _validate_csv_headers(self, df):
        if list(df.columns.values) != ["TEMA", "CATEGORIA", "TUTOR", "CAPACIDAD"]:
            raise InvalidCsv("Columns don't match with expected ones.")

    def get_info_as_rows(self):
        rows = []
        self._df.apply(
            lambda row: rows.append(
                (row["TEMA"], row["CATEGORIA"], row["TUTOR"], row["CAPACIDAD"])
            ),
            axis=1,
        )
        return rows

    def get_categories(self):
        categories = self._df['CATEGORIA'].unique()
        return list(categories)

    def get_topics(self):
        """
            Returns a list of tuples containing [(topic name, category name)]
        """
        df_topics_and_categories_only = self._df[['TEMA', 'CATEGORIA']]
        topics_and_cateogories = df_topics_and_categories_only.drop_duplicates()
        return list(topics_and_cateogories.itertuples(index=False, name=None))

    def get_topics_by_tutor(self):
        tutors = {}
        for _, row in self._df.iterrows():
            tutor = row['TUTOR']
            topic = row['TEMA']
            category = row['CATEGORIA']
            capacity = row['CAPACIDAD']

            if tutor not in tutors:
                tutors[tutor] = []

            tutors[tutor].append(
                {'topic': topic, 'category': category, 'capacity': capacity})

        return tutors
