import os
import json
from pathlib import Path

from workout.parser import WorkoutParser

import pytest

class TestWorkoutParser():
        
    full_workout_data = [
        ('./data/20200803.txt', './data/20200803.json'),
        ('./data/20200814.txt', './data/20200814.json'),
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

    raw_sections_test_data = [
        (
            """Warm-up:\nBike (7): 7 mins\n\nStrength:\nPull-ups: x5 x5 x4+1 neg\nRest 90s

BB squat (40kg+bar): x6
BB squat (50kg+bar): x5
BB squat (40kg+bar): x5 x5
Rest: 2 mins

Dips: x5 x5 x5
Rest 2 mins

Bench press (bar): x10
Bench press (20kg+bar): x5 x5 x5
Rest: 2 mins

Machine Shoulder press (15kg): x8
Seated Dumbbell Shoulder Press (10kg): x8 x8 x8
Rest 90s

Dumbbell bicep curls (10kg): x8 x8 x8
Rest: 90s""",
            [
                """Warm-up:\nBike (7): 7 mins""",
                """Strength:\nPull-ups: x5 x5 x4+1 neg\nRest 90s""",
                """BB squat (40kg+bar): x6\nBB squat (50kg+bar): x5\nBB squat (40kg+bar): x5 x5\nRest: 2 mins""",
                """Dips: x5 x5 x5\nRest 2 mins""",
                """Bench press (bar): x10\nBench press (20kg+bar): x5 x5 x5\nRest: 2 mins""",
                """Machine Shoulder press (15kg): x8\nSeated Dumbbell Shoulder Press (10kg): x8 x8 x8\nRest 90s""",
                """Dumbbell bicep curls (10kg): x8 x8 x8\nRest: 90s"""

            ]
        )
    ]

    @pytest.mark.parametrize("text,expected", raw_sections_test_data)
    def test_extract_raw_sections(self, text, expected):
        result = WorkoutParser(text)._extract_raw_sections()
        assert result == expected

    is_section_header_test_data = [
        ('Warmup:', True),
        ('Warm-up:', True),
        ('Pair 1:', True),
        ('Bike (7): 7mins', False),
        ('Assisted Arch Hangs: x5', False),
        ('Pullups: x5 x5 x5', False),
        ('BB Squat (50kg+bar): x5 x5 x5', False),
        ('Rest: 2 mins', False),
        ('Rest: 90s', False),
        ('Rest 90s', False),
    ]
    
    @pytest.mark.parametrize("text,expected", is_section_header_test_data)
    def test_is_section_header(self, text, expected):
        result = WorkoutParser(None)._is_section_header(text)
        assert result == expected

    section_data = [
        (
            [
                'Warm-up:\nBike (7): 7 mins\nAssisted Arch Hangs: x5',
                'Strength:\nPull-ups: x5 x5 x4+1 neg\nRest 90s',
                'Strength:\nBB squat (40kg+bar): x6\nBB squat (50kg+bar): x5\nBB squat (40kg+bar): x5 x5\nRest: 2 mins',
                'Strength:\nDips: x5 x5 x5\nRest 2 mins',
                'Strength:\nBench press (bar): x10\nBench press (20kg+bar): x5 x5 x5\nRest: 2 mins',
                'Strength:\nMachine Shoulder press (15kg): x8\nSeated Dumbbell Shoulder Press (10kg): x8 x8 x8\nRest 90s',
                'Strength:\nDumbbell bicep curls (10kg): x8 x8 x8\nRest: 90s'
            ],
            [
                {
                    'name': 'Warm-up',
                    'exercises': [
                        'Bike (7): 7mins',
                        'Assisted Arch Hangs: x5',
                    ],
                },
                {
                    'name': 'Strength',
                    'exercises': [
                        'Pullups: x5 x5 x4+1neg\n'
                        'Rest: 90s',
                        'BB squat (40kg+bar): x6\n',
                        'BB squat (50kg+bar): x5\n',
                        'BB squat (40kg+bar): x5 x5\n',
                        'Rest: 2 mins',
                        'Dips: x5 x5 x5\n',
                        'Rest 2 mins',
                        'Bench press (bar): x10\n',
                        'Bench press (20kg+bar): x5 x5 x5\n',
                        'Rest: 2 mins',
                        'Machine Shoulder press (15kg): x8\n',
                        'Seated Dumbbell Shoulder Press (10kg): x8 x8 x8\n',
                        'Rest 90s',
                        'Dumbbell bicep curls (10kg): x8 x8 x8\n',
                        'Rest: 90s',
                    ],
                },
            ]
        )
    ]

    @pytest.mark.parametrize("lines,expected", section_data)
    def test_extract_sections(self, lines, expected):
        result = WorkoutParser(None)._extract_sections(lines)
        assert result == expected


    extract_section_test_data = [
        (
            'Warm-up:\nBike (7): 7 mins\nAssisted Arch Hangs: x5',
            {
                'name': 'Warm-up',
                'exercises': [
                    'Bike (7): 7mins',
                    'Assisted Arch Hangs: x5',
                ],
            },
        ),
        (
            'Strength:\nPull-ups: x5 x5 x4+1 neg\nRest 90s',
            {
                'section': 'Strength',
                'parts': [
                    'Pull-ups: x5 x5 x4+1 neg',
                    'Rest 90s'
                ],
            },
        )
    ]

    rest_string_test_data = [
        ('Rest: 90s', 90),
        ('Rest: 2 mins', 120),
        ('Rest 90s', 90),
        ('Rest 2mins', 120)
    ]

    @pytest.mark.parametrize("text,expected", rest_string_test_data)
    def test_parse_rest_string(self, text, expected):
        result = WorkoutParser(None)._parse_rest_string(text)
        assert result == expected


    exercise_data = [
        ('Bike (7): 7mins', [{"name": "Bike", "reps": [], "time": 420, "weight": 7}]),
        ('Assisted Arch Hangs: x5', [{"name": "Assisted Arch Hangs", "reps": [5], "time": 0, "weight": 0}]),
        ('Assisted Arch Hangs: x10', [{"name": "Assisted Arch Hangs", "reps": [10], "time": 0, "weight": 0}]),
        ('Pullups: x5 x5 x5', [{"name": "Pullups", "reps": [5, 5, 5], "time": 0, "weight": 0}]),
        (
            'Ring Dips: x3+2 negs x3+2 negs x2+3negs',
            [
                {"name": "Ring Dips", "reps": [3, 3, 2], "time": 0, "weight": 0},
                {"name": "Ring Dips negatives", "reps": [2, 2, 3], "time": 0, "weight": 0},
            ]
        ),
        (
            'Ring Dips: x8 x8 x3+2negs',
            [
                {"name": "Ring Dips", "reps": [8, 8, 3], "time": 0, "weight": 0},
                {"name": "Ring Dips negatives", "reps": [2], "time": 0, "weight": 0}
            ]
        )
    ]

    @pytest.mark.parametrize("text,expected", exercise_data)
    def test_extract_exercises(self, text, expected):
        result = WorkoutParser(None)._extract_exercises(text)
        assert result == expected
    
    negative_reps_test_data = [
        (
            "Ring Dips",
            ' x3+2 negs x3+2 negs x2+3negs',
            {
                'name': "Ring Dips negatives",
                'reps': [2, 2, 3],
                'time': 0,
                'weight': 0,
            }
        ),
        (
            "Ring Dips",
            'x3 x3 x2+3negs',
            {
                'name': "Ring Dips negatives",
                'reps': [3],
                'time': 0,
                'weight': 0,
            }
        )
    ]
    
    @pytest.mark.parametrize("name,reps,expected", negative_reps_test_data)
    def test_generate_negative(self, name, reps, expected):
        result = WorkoutParser(None)._generate_negative(name, reps)
        assert result == expected

    generate_exercise_test_data = [
        (
            {
                'name': 'Warm-up:', 
                'exercises': ['Assisted Arch Hangs: x5'],
                'rest': 0,
                'weight': 0,
                'time': 0
            },
            [
                {
                    'section': 'Warm-up:',
                    'name': 'Assisted Arch Hangs',
                    'reps': [5],
                    'rest': 0,
                    'weight': 0,
                    'time': 0
                }
            ]
        ),
        (
            {
                'name': 'Pair 1',
                'exercises': ['Pullups: x5 x5 x5'],
                'rest': 90,
                'weight': 0,
                'time': 0
            },
            [
                {
                    'section': 'Pair 1',
                    'name': 'Pullups',
                    'reps': [5, 5, 5],
                    'rest': 90,
                    'weight': 0,
                    'time': 0
                }
            ]
        )
    ]
    
    @pytest.mark.parametrize("section,expected", generate_exercise_test_data)
    def test_generate_exercises_from_section(self, section, expected):
        result = WorkoutParser(None)._generate_exercises_from_section(section)
        assert result == expected

    extract_weight_test_data = [
        ('Bike (7)', 7),
        ('BB squat (40kg+bar)', 40),
        ('Bench press (0kg+bar)', 0),
    ]

    @pytest.mark.parametrize("name,expected", extract_weight_test_data)
    def test_extract_weight(self, name, expected):
        result = WorkoutParser(None)._extract_weight_from_name(name)
        assert result == expected