import pytest
from src.output_formatter import SimplexOutputFormatter


class TestOutputSimplexFormatter:
    @pytest.fixture
    def simplex_output_formatter(self):
        return SimplexOutputFormatter()

    @pytest.mark.formatter
    def test_initialization(self, simplex_output_formatter):
        """Test that a SimplexOutputFormatter instance can be created."""
        assert isinstance(simplex_output_formatter, SimplexOutputFormatter)

    @pytest.mark.formatter
    def test_get_result_with_empty_list(self, simplex_output_formatter):
        """Test get_result with an empty list."""
        result = []
        assert simplex_output_formatter.get_result(result) == []

    @pytest.mark.formatter
    def test_get_result_with_valid_assignments(self, simplex_output_formatter):
        """Test get_result with a list of valid assignments."""
        result = ["assignment_1", "assignment_2"]
        expected_result = [("group", "topic", "tutor")] * 2
        assert simplex_output_formatter.get_result(result) == expected_result

    @pytest.mark.formatter
    def test_get_result_with_invalid_assignments(self, simplex_output_formatter):
        """Test get_result with a list containing invalid assignments."""
        result = ["assignment_1", "assignment_2", "invalid_assignment"]
        expected_result = [("group", "topic", "tutor")] * 2
        assert simplex_output_formatter.get_result(result) == expected_result

    @pytest.mark.formatter
    def test_get_result_with_malformed_assignments(self, simplex_output_formatter):
        """Test get_result with a list containing malformed assignments."""
        result = ["malformed_assignment"]
        assert simplex_output_formatter.get_result(result) == []
