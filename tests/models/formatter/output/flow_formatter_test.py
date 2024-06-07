import pytest
from src.model.formatter.output.flow_formatter import FlowOutputFormatter
from src.exceptions import WrongDateFormat


class TestFlowOutputFormatter:
    formatter = FlowOutputFormatter()

    @pytest.mark.unit
    def test_create_date_with_correct_format(self):
        assert "1-1-1" == self.formatter._create_date("date-1-1-1").label()

    @pytest.mark.unit
    def test_create_date_with_wrong_format(self):
        with pytest.raises(WrongDateFormat):
            assert "1-1-1" == self.formatter._create_date("1-1-1").label()
