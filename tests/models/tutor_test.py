import pytest
from src.model.period import TutorPeriod
from src.model.tutor import Tutor
from src.model.group import Group
from src.model.utils.delivery_date import DeliveryDate
from src.model.utils.topic import Topic
import src.exceptions as e


class TestTutor:

    @pytest.mark.unit
    def test_when_it_is_initialized_it_not_has_periods(self):
        tutor = Tutor(1, "test@fi.uba.ar", "Juan Perez")

        result = len(tutor.periods)

        assert result == 0

    @pytest.mark.unit
    def test_tutor_can_add_periods(self):
        tutor = Tutor(1, "test@fi.uba.ar", "Juan Perez")
        period = TutorPeriod("1C2024", tutor=tutor)
        tutor.add_period(period)

        result = len(tutor.periods)

        assert result == 1

    @pytest.mark.unit
    def test_tutor_raise_error_if_duplicates_periods(self):
        tutor = Tutor(1, "test@fi.uba.ar", "Juan Perez")
        period = TutorPeriod("1C2024", tutor=tutor)
        tutor.add_period(period)

        with pytest.raises(e.PeriodAlreadyExists) as ex:
            tutor.add_period(period)

    @pytest.mark.unit
    def test_tutor_can_get_specific_period(self):
        tutor = Tutor(1, "test@fi.uba.ar", "Juan Perez")
        period1 = TutorPeriod("1C2024", tutor=tutor)
        period2 = TutorPeriod("2C2024", tutor=tutor)
        period3 = TutorPeriod("1C2023", tutor=tutor)

        tutor.add_period(period1)
        tutor.add_period(period2)
        tutor.add_period(period3)

        period = tutor.get_period("1C2024")

        assert period.period_name() == "1C2024"

    @pytest.mark.unit
    def test_tutor_raise_error_if_tutor_has_not_period(self):
        tutor = Tutor(1, "test@fi.uba.ar", "Juan Perez")

        with pytest.raises(e.PeriodNotFound) as ex:
            tutor.get_period("1C2024")

    @pytest.mark.unit
    def test_tutor_assign_groups(self):
        tutor = Tutor(1, "test@fi.uba.ar", "Juan Perez")
        period1 = TutorPeriod("1C2024", tutor=tutor)
        tutor.add_period(period1)
        g1 = Group(1)
        g2 = Group(2)
        g3 = Group(3)

        tutor.add_groups_to_period([g1, g2, g3], "1C2024")

        assert g1.tutor == tutor
        assert g2.tutor == tutor
        assert g3.tutor == tutor
