import pandas as pd
from src.model.delivery_date import DeliveryDate
from src.model.hour import Hour
from src.model.day import Day

class InputFormatter:
    WEEKS_DICT = {"Semana 1/7": 1, "Semana 8/7": 2, "Semana 15/7": 3, 
            "Semana 22/7": 4, "Semana 29/7": 5, "Semana 5/8": 6, 
            "Semana 12/8": 7}

    DAYS_DICT = {"Lunes": Day.MONDAY, "Martes": Day.TUESDAY, "Miércoles": Day.WEDNESDAY,
                    "Jueves": Day.THURSDAY, "Viernes": Day.FRIDAY}

    HOURS_DICT = {"9 a 10": Hour.H_9_10, "10 a 11": Hour.H_10_11,
                "11 a 12": Hour.H_11_12, "12 a 13": Hour.H_12_13,
                "14 a 15": Hour.H_14_15, "15 a 16": Hour.H_15_16,
                "16 a 17": Hour.H_16_17, "17 a 18": Hour.H_17_18,
                "18 a 19": Hour.H_18_19, "19 a 20": Hour.H_19_20,
                "20 a 21": Hour.H_20_21}
        
    def __init__(self, groups_availability_path: str):
        df = pd.read_csv(groups_availability_path)
        self._df = df
        
    def tutor_id(self, tutor_surname: str):
        tutors = self._df["Apellido del tutor"].unique()
        return "p" + tutors.index(tutor_surname)

    def availability_dates(self, row):
        dates = []
        for column, value in row.items():
            if "Semana" in column:
                columns_parts = column.split('[')
                week_part = columns_parts[0].strip()
                hour_part = columns_parts[1].replace(']', '').strip()
                if(hour_part != "No puedo"):
                    if(pd.isna(value) == False):
                        days = value.split(',')
                        for day in days:
                            day = day.strip().split(' ')[0].strip()
                            dates.append(DeliveryDate(self.WEEKS_DICT[week_part], 
                                                    self.DAYS_DICT[day], 
                                                    self.HOURS_DICT[hour_part]))
        return dates
    
    def groups(self):
        groups = self._df.apply(lambda x: {"group_id": x["Número de equipo"], 
                                           "tutor_id": x["Apellido del tutor"], 
                                           "availability_dates": self.availability_dates(x)}, axis=1)
        return groups
    



