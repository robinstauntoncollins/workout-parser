import re
from typing import List

class WorkoutParser():

    patterns = {
        'date': r"[\d]{1,2}(?:[trns]\w*)? [ADFJMNOS]\w* [\d]{4}",
        'lines': r".*\S.*",
        'section_header': r"^.*:$",
        'exercise': r"(.+):(.+)"
    }
    
    def __init__(self, raw):
        self.raw = raw

    def parse(self):
        date = self._extract_date()
        lines = self._extract_lines()
        print(f"Lines: {lines}")
        sections = self._extract_sections(lines)
        print(f"Sections: {sections}")
        self.exercises = self._extract_exercise
        exercises = [
            {
                "section": section,
                "name": self._extract_exercise(exercise)[0]
            }
            for section, exercises in sections.items()
            for exercise in exercises
        ]
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
        sections = {}
        section = None
        for i, line in enumerate(lines):
            if self._is_section_header(line):
                section = line
            else:
                if not section:
                    continue
                else:
                    if section not in sections:
                        sections[section] = [line]
                    else:
                        sections[section].append(line)
        self.sections = sections
        return sections

    def _extract_exercise(self, text: str):
        print(f"Received: text: {text}")
        if type(text) != str:
            raise ValueError(f"Got {type(text)} expected 'str'")
        p = re.compile(self.patterns['exercise'])
        matches = p.search(text)
        if not matches:
            raise ValueError(f"Did not match string: {text}")
        name = matches.group(1)
        setrep_string = matches.group(2)
        return (name.strip(), setrep_string.strip())


        


    