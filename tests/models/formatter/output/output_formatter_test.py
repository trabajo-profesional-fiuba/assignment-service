import pytest
from unittest.mock import MagicMock
from src.model.formatter.output.flow_formatter import FlowOutputFormatter
from src.model.formatter.output.lp_formatter import LPOutputFormatter
from src.exceptions import ResultFormatNotFound
from src.model.formatter.output.output_formatter import OutputFormatter


class TestOutputFormatter:
    @pytest.fixture
    def output_formatter(self):
        return OutputFormatter()

    @pytest.mark.unit
    def test_initialization(self, output_formatter):
        """Test that the OutputFormatter initializes correctly."""
        assert isinstance(output_formatter, OutputFormatter)

    @pytest.mark.unit
    def test_format_result_with_dict(self, output_formatter):
        """Test formatting result with a dictionary."""
        mock_flow_formatter = MagicMock(FlowOutputFormatter)
        mock_flow_formatter.get_result.return_value = "Formatted dict result"
        output_formatter.FORMATTERS[dict] = mock_flow_formatter

        result = {"key": "value"}
        formatted_result = output_formatter.format_result(result, [], [])

        mock_flow_formatter.get_result.assert_called_once_with(result, [], [])
        assert formatted_result == "Formatted dict result"

    @pytest.mark.unit
    def test_format_result_with_list(self, output_formatter):
        """Test formatting result with a list."""
        mock_lp_formatter = MagicMock(LPOutputFormatter)
        mock_lp_formatter.get_result.return_value = "Formatted list result"
        output_formatter.FORMATTERS[list] = mock_lp_formatter

        result = ["item1", "item2"]
        formatted_result = output_formatter.format_result(result, [], [])

        mock_lp_formatter.get_result.assert_called_once_with(result, [], [])
        assert formatted_result == "Formatted list result"

    @pytest.mark.unit
    def test_format_result_with_unrecognized_type(self, output_formatter):
        """Test that ResultFormatNotFound is raised for unrecognized result types."""
        result = 123  # An unrecognized type (neither dict nor list)
        with pytest.raises(ResultFormatNotFound):
            output_formatter.format_result(result, [], [])
