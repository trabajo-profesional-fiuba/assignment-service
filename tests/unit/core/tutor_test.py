import pytest
from src.core.delivery_date import DeliveryDate
from src.core.topic import Topic
from src.core.tutor import Tutor
from src.core.group import Group
import src.exceptions as e


class TestTutor:

    @pytest.mark.unit
    def test_when_it_is_initialized_it_just_has_id(self):
        # Arrange
        tutor = Tutor(1, "test@fi.uba.ar", "Juan","Perez")
        # Assert multiple
        assert len(tutor.available_dates) == 0
        assert len(tutor.as_tutor_dates) == 0
        assert len(tutor.as_evaluator_dates) == 0
        assert len(tutor.groups) == 0
        assert len(tutor.topics) == 0
        assert tutor.is_evaluator() is False
        assert tutor.capacity == 0

    @pytest.mark.unit
    def test_should_change_evaluator_status(self):
        # Arrange
        tutor = Tutor(1, "test@fi.uba.ar", "Juan","Perez")
        # Act
        tutor.make_evaluator()
        # Assert
        assert tutor.is_evaluator() is True

    @pytest.mark.unit
    def test_tutor_has_empty_dates(self):
        # Arrange
        tutor = Tutor(1, "test@fi.uba.ar", "Juan","Perez")
        # Act
        available_dates = tutor.available_dates
        # Assert
        assert len(available_dates) == 0

    @pytest.mark.unit
    def test_tutor_dates_if_they_are_passed(self):
        # Arrange
        dates = [DeliveryDate(1, 2, 3), DeliveryDate(1, 4, 1), DeliveryDate(1, 3, 2)]
        tutor = Tutor(1, "test@fi.uba.ar", "Juan","Perez")

        # Act
        tutor.add_available_dates(dates)
        available_dates = tutor.available_dates
        # Assert
        assert len(available_dates) == 3

    @pytest.mark.unit
    def test_tutor_is_avaliable_on_date(self):
        # Arrange
        dates = [DeliveryDate(1, 2, 3), DeliveryDate(1, 4, 1), DeliveryDate(1, 3, 2)]
        tutor = Tutor(1, "test@fi.uba.ar", "Juan","Perez")
        tutor.add_available_dates(dates)

        # Act
        is_avaliable = tutor.is_avaliable(dates[1].label())
        # Assert
        assert is_avaliable is True

    @pytest.mark.unit
    def test_tutor_can_have_substitute_dates(self):
        # Arrange
        dates = [DeliveryDate(1, 2, 3), DeliveryDate(1, 4, 1), DeliveryDate(1, 3, 2)]
        tutor = Tutor(1, "test@fi.uba.ar", "Juan","Perez")
        tutor.add_available_dates(dates)
        subst_date = DeliveryDate(2, 2, 4)

        # Act
        tutor.add_substitute_date(subst_date)

        # Assert
        assert tutor.substitute_dates[0] == subst_date

    @pytest.mark.unit
    def test_tutor_evaluate_date(self):
        # Arrange
        date = DeliveryDate(2, 2, 5)
        tutor = Tutor(1, "test@fi.uba.ar", "Juan","Perez")

        # Act & Assert
        assert len(tutor.as_evaluator_dates) == 0
        tutor.evaluate_date(date)
        assert len(tutor.as_evaluator_dates) == 1

    
    @pytest.mark.unit
    def test_tutor_date(self):
        # Arrange
        date = DeliveryDate(2, 2, 5)
        tutor = Tutor(1, "test@fi.uba.ar", "Juan","Perez")

        # Act & Assert
        assert len(tutor.as_tutor_dates) == 0
        tutor.tutor_date(date)
        assert len(tutor.as_tutor_dates) == 1
    
    @pytest.mark.unit
    def test_tutor_can_have_topics(self):
        t1 = Topic(id=1, title="foo", capacity=1, category="Category A")
        t2 = Topic(id=2, title="bar", capacity=1, category="Category A")
        tutor = Tutor(1, "test@fi.uba.ar", "Juan","Perez")

        tutor.add_topic(t1)
        tutor.add_topic(t2)

        assert len(tutor._topics) == 2

    @pytest.mark.unit
    def test_tutor_can_filter_mutual_dates(self):
        # Arrange
        dates = [DeliveryDate(1, 2, 3), DeliveryDate(1, 4, 1), DeliveryDate(1, 3, 2)]
        tutor = Tutor(1, "test@fi.uba.ar", "Juan","Perez")
        tutor.add_available_dates(dates)
        expected = [dates[1].label(), dates[2].label()]

        # Act & Assert
        dates_filtered = tutor.find_mutual_dates([dates[1], dates[2]])
        assert all(e in dates_filtered for e in expected)

    @pytest.mark.unit
    def test_tutor_assign_groups(self):
        tutor = Tutor(1, "test@fi.uba.ar", "Juan","Perez")
        g1 = Group(1)
        g2 = Group(2)

        tutor.add_groups([g1, g2])

        assert len(tutor._groups) == 2

    @pytest.mark.unit
    def test_tutor_can_return_groups_ids(self):
        g1 = Group(1)
        g2 = Group(2)
        tutor = Tutor(1, "test@fi.uba.ar", "Juan","Perez")
        tutor.add_groups([g1, g2])

        result = tutor.groups_ids()

        assert result == [1, 2]