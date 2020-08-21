import re
from typing import List, Dict, Union
from itertools import chain

class WorkoutParser():

    patterns = {
        'date': r"[\d]{1,2}(?:[trns]\w*)? [ADFJMNOS]\w* [\d]{4}",
        'lines': r".*\S.*",
        'section_header': r"^.*:$",
        'exercise': {
            'exercise': r"(.+):(.+)",
            'exercise_reps': r"(?:x)(\d{1,2})(?:\+(\d\s?negs?))?",
            'exercise_time': r".+(\d)?:(\s?\d\s?mins?)",
            'exercise_weight': r".+\((\d{0,2}).*\)",
            'negative_reps': r"(\d)\s?negs?",
        },
        'rest': r"(?:\w+(?::)?\s)([\d]{1,2}\s?)(\w{1,4})",
        
    }
    
    def __init__(self, raw):
        self.raw = raw

    def parse(self):
        date = self._extract_date()
        lines = self._extract_lines()
        print(f"Lines: {lines}")
        sections = self._extract_sections(lines)
        print(f"Sections: {sections}")
        exercises = list(chain.from_iterable([self._generate_exercises_from_section(section) for section in sections]))
        print(f"Exercises: {exercises}")
        return {
            'date': date,
            'exercises': exercises
        }

    def _extract_date(self):
        p = re.compile(self.patterns['date'])
        return p.search(self.raw).group()

    def _extract_lines(self):
        p = re.compile(self.patterns['lines'])
        return re.findall(p, self.raw)

    def _is_section_header(self, text: str):
        p = re.compile(self.patterns['section_header'])
        return bool(p.match(text))

    def _extract_sections(self, lines: List[str]) -> dict:
        sections = []
        section = {'name': None, 'exercises': [], 'rest': 0}
        for i, line in enumerate(lines):
            print(f"Working on line: {line}")
            if self._is_section_header(line):
                if section['name'] is not None:
                    sections.append(section)
                    print(f"Finished section: {section}")
                    section = {'name': None, 'exercises': [], 'rest': 0}
                section['name'] = line.split(':')[0]
            elif 'rest' in line.lower():
                section['rest'] = self._parse_rest_string(line)
            else:
                if section['name'] is not None:
                    section['exercises'].append(line)
                else:
                    continue
        sections.append(section)
        return sections

    def _parse_rest_string(self, string: str) -> int:
        p = re.compile(self.patterns['rest'])
        m = p.match(string)
        val, unit = m.groups()
        if unit == 'mins':
            return int(val) * 60
        return int(val)

    def _generate_exercises_from_section(self, section: Dict[str, Union[str, List[str]]]) -> List[dict]:
        exercises: List[Dict[str, Union[str, List[int]]]] = []
        section_name = section['name']
        section_rest = section['rest']
        exercise_list: List[Dict[str, Union[str, List[int]]]] = []
        for exercise_text in section['exercises']:
            exercise = self._extract_exercise(exercise_text)
            if type(exercise) == list:
                for ex in exercise:
                    exercise_list.append({
                    'section': section_name,
                    'name': ex['name'],
                    'reps': ex['reps'],
                    'rest': section_rest
                })
            else:
                exercise_list.append({
                    'section': section_name,
                    'name': exercise['name'],
                    'reps': exercise['reps'],
                    'rest': section_rest
                })
        return exercise_list

    def _extract_exercise(self, text: str):
        print(f"Received: text: {text}")
        if type(text) != str:
            raise ValueError(f"Got {type(text)} expected 'str'")

        name, reps = text.split(':')
        print(f"Name: '{name}' - reps: '{reps}'")
        p = re.compile(self.patterns['exercise']['exercise_reps'])
        matches = p.findall(reps)
        print(f"Reps matches: {matches}")
        if not matches:
            p = re.compile(self.patterns['exercise']['exercise_time'])
            matches = p.findall(reps)
            print(f"Time matches: {matches}")
            if not matches:
                raise ValueError(f"No match for {text}")
        print(f"Matches: {matches}")
        reps = [int(pair[0]) for pair in matches]
        negs = [pair[1] for pair in matches]
        has_negs = [bool(neg) for neg in negs]
        if any(has_negs):
            neg_exercise = self._generate_negative(name.strip(), negs)
            return [
                {"name": name.strip(), "reps": reps},
                neg_exercise,
            ]
        return {"name": name.strip(), "reps": reps}

    def _generate_negative(self, name: str, reps: List[str]) -> Dict[str, Union[str, List[int]]]:
        p = re.compile(self.patterns['exercise']['negative_reps'])
        reps_vals: List[int] = []
        for rep in reps:
            match = p.match(rep)
            if not match:
                reps_vals.append(0)
            else:
                reps_vals.append(int(match.group(1)))
        return {
            "name": name + ' negatives',
            "reps": reps_vals
        }

    def _extract_weight_from_name(self, name):
        p = re.compile(self.patterns['exercise']['exercise_weight'])
        matches = p.match(name)
        if not matches:
            raise ValueError(f"No match for {name}")
        return matches.group(1)



if __name__ == '__main__':
    norm = 'Pullups: x5 x5 x5'
    negs = 'Ring Dips: x3+2 negs x3+2 negs x2+3negs'
    result = WorkoutParser(None)._extract_exercise(negs)
    print(result)