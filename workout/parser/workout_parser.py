import re
from typing import List, Dict, Union

class WorkoutParser():

    patterns = {
        'date': r"[\d]{1,2}(?:[trns]\w*)? [ADFJMNOS]\w* [\d]{4}",
        'lines': r".*\S.*",
        'section_header': r"^.*:$",
        'exercise': r"(.+):(.+)",
        'rest': r"(?:\w+(?::)?\s)([\d]{1,2}\s?)(\w{1,4})",
        'exercise_reps': r"(?:x)(\d{1,2})(?:\+(\d\s?negs?))?",
        'negative_reps': r"(\d)\s?negs?",
    }
    
    def __init__(self, raw):
        self.raw = raw

    def parse(self):
        date = self._extract_date()
        lines = self._extract_lines()
        print(f"Lines: {lines}")
        sections = self._extract_sections(lines)
        print(f"Sections: {sections}")
        exercise_strings = [ex for section in sections for ex in section['exercises']]
        self.exercises = [self._extract_exercise(ex) for ex in exercise_strings]
        return {
            'date': date,
            'exercises': self.exercises
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
        section = {'name': None, 'exercises': [], 'rest': None}
        for i, line in enumerate(lines):
            print(line)
            if self._is_section_header(line):
                if section['name'] is not None:
                    sections.append(section)
                    section = {'name': None, 'exercises': [], 'rest': None}
                section['name'] = line
            elif 'rest' in line.lower():
                section['rest'] = self._parse_rest_string(line)
                sections.append(section)
                section = {'name': None, 'exercises': [], 'rest': None}
            else:
                if section['name'] is not None:
                    section['exercises'].append(line)
                else:
                    continue
        return sections

    def _parse_rest_string(self, string: str) -> int:
        p = re.compile(self.patterns['rest'])
        m = p.match(string)
        val, unit = m.groups()
        if unit == 'mins':
            return int(val) * 60
        return int(val)


    def _extract_exercise(self, text: str):
        print(f"Received: text: {text}")
        if type(text) != str:
            raise ValueError(f"Got {type(text)} expected 'str'")

        name, reps = text.split(':')
        
        p = re.compile(self.patterns['exercise_reps'])
        matches = p.findall(reps)
        if not matches:
            print(f"Not an exercise: {text}")
            return
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
        p = re.compile(self.patterns['negative_reps'])
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



if __name__ == '__main__':
    norm = 'Pullups: x5 x5 x5'
    negs = 'Ring Dips: x3+2 negs x3+2 negs x2+3negs'
    result = WorkoutParser(None)._extract_exercise(negs)
    print(result)