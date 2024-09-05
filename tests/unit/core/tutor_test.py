import pytest

from src.core.tutor import Tutor
from src.core.group import Group
import src.exceptions as e


class TestTutor:
    
    @pytest.mark.unit
    def test_tutor_assign_groups(self):
        tutor = Tutor(1, "test@fi.uba.ar", "Juan","Perez")
        g1 = Group(1)
        g2 = Group(2)
        g3 = Group(3)

        tutor.add_groups([g1, g2, g3])

        assert g1.tutor == tutor
        assert g2.tutor == tutor
        assert g3.tutor == tutor
