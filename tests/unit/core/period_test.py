import pytest
from src.core.period import TutorPeriod
from src.core.tutor import Tutor
from src.core.group import Group
from src.core.delivery_date import DeliveryDate
from src.core.topic import Topic
import src.exceptions as e


class TestTutorPeriod:

    @pytest.mark.unit
    def test_when_it_is_initialized_it_just_has_id(self):
        # Arrange
        period = TutorPeriod(period="1C2024")
        # Assert multiple
        assert len(period.available_dates) == 0
        assert len(period.as_tutor_dates) == 0
        assert len(period.as_evaluator_dates) == 0
        assert len(period.groups) == 0
        assert len(period.topics) == 0
        assert period.is_evaluator() is False
        assert period.tutor is None
        assert period.capacity == 0

    @pytest.mark.unit
    def test_should_have_a_reference_to_its_parent(self):
        # Arrange
        parent = Tutor(1, "f@fi.uba.ar", "Juan")
        period = TutorPeriod(period="1C2024")
        period.add_parent(parent)
        # Act & Assert
        assert period.id() == 1

    @pytest.mark.unit
    def test_raise_error_if_it_has_no_tutor(self):
        # Arrange
        period = TutorPeriod(period="1C2024")
        # Act & Assert
        with pytest.raises(e.PeriodWithoutParentError):
            period.id()

    @pytest.mark.unit
    def test_should_change_evaluator_status(self):
        # Arrange
        period = TutorPeriod(period="1C2024")
        # Act
        period.make_evaluator()
        # Assert
        assert period.is_evaluator() is True

    @pytest.mark.unit
    def test_period_has_empty_dates(self):
        # Arrange
        period = TutorPeriod(period="1C2024")
        # Act
        available_dates = period.available_dates
        # Assert
        assert len(available_dates) == 0

    @pytest.mark.unit
    def test_period_dates_if_they_are_passed(self):
        # Arrange
        dates = [DeliveryDate(1, 2, 3), DeliveryDate(1, 4, 1), DeliveryDate(1, 3, 2)]
        period = TutorPeriod(period="1C2024")

        # Act
        period.add_available_dates(dates)
        available_dates = period.available_dates
        # Assert
        assert len(available_dates) == 3

    @pytest.mark.unit
    def test_period_is_avaliable_on_date(self):
        # Arrange
        dates = [DeliveryDate(1, 2, 3), DeliveryDate(1, 4, 1), DeliveryDate(1, 3, 2)]
        period = TutorPeriod(period="1C2024")
        period.add_available_dates(dates)

        # Act
        is_avaliable = period.is_avaliable(dates[1].label())
        # Assert
        assert is_avaliable is True

    @pytest.mark.unit
    def test_period_can_have_substitute_dates(self):
        # Arrange
        dates = [DeliveryDate(1, 2, 3), DeliveryDate(1, 4, 1), DeliveryDate(1, 3, 2)]
        period = TutorPeriod(period="1C2024")
        period.add_available_dates(dates)
        subst_date = DeliveryDate(2, 2, 4)

        # Act
        period.add_substitute_date(subst_date)

        # Assert
        assert period.substitute_dates[0] == subst_date

    @pytest.mark.unit
    def test_period_evaluate_date(self):
        # Arrange
        date = DeliveryDate(2, 2, 5)
        period = TutorPeriod(period="1C2024")

        # Act & Assert
        assert len(period.as_evaluator_dates) == 0
        period.evaluate_date(date)
        assert len(period.as_evaluator_dates) == 1

    @pytest.mark.unit
    def test_period_tutor_date(self):
        # Arrange
        date = DeliveryDate(2, 2, 5)
        period = TutorPeriod(period="1C2024")

        # Act & Assert
        assert len(period.as_tutor_dates) == 0
        period.tutor_date(date)
        assert len(period.as_tutor_dates) == 1

    @pytest.mark.unit
    def test_period_can_have_topics(self):
        t1 = Topic(1, "foo", 1, 0)
        t2 = Topic(2, "bar", 1, 0)
        period = TutorPeriod(period="1C2024")

        period.add_topic(t1)
        period.add_topic(t2)

        assert len(period._topics) == 2

    @pytest.mark.unit
    def test_period_can_filter_mutual_dates(self):
        # Arrange
        dates = [DeliveryDate(1, 2, 3), DeliveryDate(1, 4, 1), DeliveryDate(1, 3, 2)]
        period = TutorPeriod(period="1C2024")
        period.add_available_dates(dates)
        expected = [dates[1].label(), dates[2].label()]

        # Act & Assert
        dates_filtered = period.find_mutual_dates([dates[1], dates[2]])
        assert all(e in dates_filtered for e in expected)

    @pytest.mark.unit
    def test_period_can_have_groups(self):
        g1 = Group(1)
        g2 = Group(2)
        period = TutorPeriod(period="1C2024")

        period.add_groups([g1, g2])

        assert len(period._groups) == 2

    @pytest.mark.unit
    def test_period_can_return_groups_ids(self):
        g1 = Group(1)
        g2 = Group(2)
        period = TutorPeriod(period="1C2024")
        period.add_groups([g1, g2])

        result = period.groups_ids()

        assert result == [1, 2]
