import os
import json
from pathlib import Path

from workout.parser import WorkoutParser

import pytest

class TestWorkoutParser():
        
    full_workout_data = [
        ('./data/20200803.txt', './data/20200803.json'),
        # ('./data/20200814.txt', './data/20200814.json'),
        # ('./data/recommended_routine.txt', './data/recommended_routine.json'),
        # ('./data/starting_strength_example_workout.txt', './data/starting_strength_example_workout.json'),
    ]

    @pytest.mark.parametrize("workout_path,expected_path", full_workout_data)
    def test_workout_parser(self, workout_path, expected_path):
        with open(workout_path) as f:
            workout_raw = f.read()

        with open(expected_path) as f:
            expected = json.loads(f.read())

        result = WorkoutParser(workout_raw).parse()
        assert result == expected

    date_data = [
        ("""3 August 2020\nSomeother Stuff and numbers: 21041""", "3 August 2020"),
        ("""6th August 2020\n\nWarmup:\nBand Shoulder routine: x10""", "6th August 2020"),
        ("3 August 2020\nSomeot", "3 August 2020"),
        ("3rd August 2020\nSomeot", "3rd August 2020"),
        ("6th August 2020\nSomeot", "6th August 2020"),
        ("15th August 2020\nSomeot", "15th August 2020"),
        ("21st November 2020\nSomeot", "21st November 2020"),
        ("2nd October 2020\nSomeot", "2nd October 2020"),
    ]

    @pytest.mark.parametrize("date_text,expected", date_data)
    def test_extract_date(self, date_text, expected):
        result = WorkoutParser(date_text)._extract_date()
        assert result == expected

    section_data = [
        (
            ['3 August 2020', 'Warm-up:', 'Assisted Arch Hangs: x5', 'Pair 1:', 'Pullups: x5 x5 x5'],
            {
                'Warm-up:': [
                    'Assisted Arch Hangs: x5'
                ],
                'Pair 1:': [
                    'Pullups: x5 x5 x5'
                ]
            }
        )
    ]

    @pytest.mark.parametrize("lines,expected", section_data)
    def test_extract_sections(self, lines, expected):
        result = WorkoutParser(None)._extract_sections(lines)
        assert result == expected

    exercise_data = [
        ('Assisted Arch Hangs: x5', ("Assisted Arch Hangs", "x5")),
        ('Pullups: x5 x5 x5', ("Pullups", "x5 x5 x5")),
    ]

    @pytest.mark.parametrize("text,expected", exercise_data)
    def test_extract_exercise(self, text, expected):
        result = WorkoutParser(None)._extract_exercise(text)
        assert result == expected
    