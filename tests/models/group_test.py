import pytest

from src.core.group import Group
from src.core.tutor import Tutor
from src.core.period import TutorPeriod
from src.core.topic import Topic
from src.core.delivery_date import DeliveryDate


class TestGroup:

    @pytest.mark.unit
    def test_group_starts_with_id_and_no_tutor(self):
        group = Group(1)

        assert group.id() == 1
        assert group.tutor is None

    @pytest.mark.unit
    def test_group_can_be_assigned_to_a_tutor(self):
        period = TutorPeriod("1C2024")
        tutor = Tutor(1, "fake@fi.uba.ar", "Juan")
        tutor.add_period(period)
        group = Group(1)

        period.add_groups([group])
        group.assign_tutor(tutor)

        assert group.is_tutored_by(1) is True

    @pytest.mark.unit
    def test_group_can_have_topics(self):
        topics = [Topic(1, "topic1", 1), Topic(2, "topic2", 2), Topic(3, "topic3", 3)]
        group = Group(1)

        group.add_topics(topics)

        assert group.preference_of(Topic(1, "topic1", 1)) == 1

    @pytest.mark.unit
    def test_group_can_have_available_dates(self):
        dates = [DeliveryDate(2, 2, 3), DeliveryDate(2, 2, 4), DeliveryDate(2, 2, 5)]
        group = Group(1)
        group.add_available_dates(dates)

        expected_cost = (5 * 11) - 3
        result = group.cost_of_week(2)
        assert expected_cost == result

    @pytest.mark.unit
    def test_group_can_calculate_cost_per_week(self):
        dates = [
            DeliveryDate(2, 2, 1),
            DeliveryDate(2, 2, 2),
            DeliveryDate(2, 2, 3),
            DeliveryDate(2, 2, 4),
            DeliveryDate(2, 2, 5),
            DeliveryDate(2, 2, 6),
            DeliveryDate(2, 2, 7),
            DeliveryDate(2, 2, 8),
            DeliveryDate(2, 2, 9),
            DeliveryDate(2, 4, 1),
            DeliveryDate(2, 4, 2),
            DeliveryDate(2, 4, 3),
            DeliveryDate(2, 4, 4),
            DeliveryDate(2, 4, 5),
            DeliveryDate(2, 4, 6),
            DeliveryDate(2, 4, 7),
            DeliveryDate(2, 4, 8),
            DeliveryDate(2, 4, 9),
        ]
        group = Group(1)
        group.add_available_dates(dates)

        expected_cost = (5 * 11) - 18
        result = group.cost_of_week(2)
        assert expected_cost == result

    @pytest.mark.unit
    def test_group_can_calculate_cost_per_date(self):
        dates = [
            DeliveryDate(2, 2, 1),
            DeliveryDate(2, 2, 2),
            DeliveryDate(2, 2, 3),
            DeliveryDate(2, 2, 4),
            DeliveryDate(2, 2, 5),
            DeliveryDate(2, 2, 6),
            DeliveryDate(2, 2, 7),
            DeliveryDate(2, 2, 8),
            DeliveryDate(2, 2, 9),
        ]
        group = Group(1)
        group.add_available_dates(dates)

        expected_cost = 11 - 9
        result = group.cost_of_date(DeliveryDate(2, 2, 1))
        assert expected_cost == result
