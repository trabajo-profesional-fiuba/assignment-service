import pytest
from src.model.formatter.output.lp_formatter import LPOutputFormatter


class TestLPOutputFormatter:
    @pytest.mark.formatter
    def test_get_result(self):
        assert 1 == 1
