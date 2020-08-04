import pytest

from workout.parse import parse_date

class TestParseDate():

    test_data = [
        ('3 August 2020', '2020-08-03T00:00:00')
    ]

    @pytest.mark.parametrize('raw,expected', test_data)
    def test_parse_date(self, raw, expected):
        date = parse_date(raw)
        assert date == expected