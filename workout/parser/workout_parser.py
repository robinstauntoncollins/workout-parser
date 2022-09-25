import re
from typing import List, Dict, Union
from itertools import chain

# from entities import Exercise

class WorkoutParser():

    patterns = {
        'date': r"[\d]{1,2}(?:[trns]\w*)? [ADFJMNOS]\w* [\d]{4}",
        'lines': r".*\S.*",
        'section_header': r"^.*:$",
        'exercise': {
            'exercise': r"(.+):(.+)",
            'exercise_reps': r"(?:x)(\d{1,2})(?:\+(\d\s?negs?))?",
            'exercise_reps_only': r"(?:x)(\d{1,2})",
            'exercise_time': r"(?:\s?(\d+)\s?mins?)",
            'exercise_weight': r".+\((\d{0,2}).*\)",
            'negative_reps': r"(\d)\s?negs?",
        },
        'rest': r"(?:\w+(?::)?\s)([\d]{1,2}\s?)(\w{1,4})",
        
    }
    
    def __init__(self, raw):
        self.raw = raw

    def parse(self):
        date = self._extract_date()
        logging.info(f"Date: {date}")
        raw_sections = self._extract_raw_sections()
        logging.debug(f"Raw sections: {raw_sections}")
        for section in raw_sections[1::]:
            logging.debug(f"Parsing section: {section}")
            for line in section:
                logging.debug(f"Parsing line: {line}")
                exercises = self._extract_exercises(line)
                logging.debug(f"Exercises: {exercises}")
        # lines = self._extract_lines()
        # logging.info(f"Lines: {lines}")
        # sections = self._extract_sections(lines)
        # logging.info(f"Sections: {sections}")
        # exercises = list(
        #     chain.from_iterable(
        #         [
        #             self._generate_exercises_from_section(section)
        #             for section in sections
        #         ]
        #     )
        # )
        # logging.info(f"Exercises: {exercises}")
        # return {
        #     'date': date,
        #     'exercises': exercises
        # }

    def _extract_date(self):
        p = re.compile(self.patterns['date'])
        return p.search(self.raw).group()

    def _extract_raw_sections(self):
        sections = self.raw.split('\n\n')
        sections = [section.split('\n') for section in sections[1::]]
        return sections

    def _extract_lines(self):
        p = re.compile(self.patterns['lines'])
        return re.findall(p, self.raw)

    def _is_section_header(self, text: str):
        p = re.compile(self.patterns['section_header'])
        return bool(p.match(text))

    def _extract_section(self, section: str):
        parts = section.split('\n')
        if self._is_section_header(parts[0]):
            section_name = parts[0].split(':')[0]
        return {'name': section_name, 'parts': parts[1::]}

    def _extract_exercise_name(self, text: str) -> str:
        p = re.compile(self.patterns['exercise'])
        matches = p.match(text)


    def _extract_section_exercises(self, section: List[str]) -> dict:
        exercises = []
        exercise = {
            'name': '',
            'sets': [
                {
                    'weight': int,
                    'reps': int
                },
                {
                    'weight': int,
                    'reps': int
                },
                {
                    'weight': int,
                    'reps': int
                }
            ]
        }
        for line in section:
            logging.debug(f"Extracting line: {line}")
            name = self._extract_exercise_name(line)
            logging.debug(name)
            # weight = self._extract_weight_from_name(line)
            # reps = self._extract_reps(line)
            

    # def _extract_sections(self, sections: List[str]) -> dict:
    #     sections = []
    #     section = {'name': None, 'exercises': [], 'rest': 0, 'time': 0, 'weight': 0}
    #     for i, line in enumerate(sections):
    #         logging.debug(f"Working on line: {line}")
    #         if self._is_section_header(line):
    #             if section['name'] is not None:
    #                 sections.append(section)
    #                 logging.debug(f"Finished section: {section}")
    #                 section = {'name': None, 'exercises': [], 'rest': 0, 'time': 0, 'weight': 0}
    #             section['name'] = line.split(':')[0]
    #         elif 'rest' in line.lower():
    #             section['rest'] = self._parse_rest_string(line)
    #         else:
    #             if section['name'] is not None:
    #                 section['exercises'].append(line)
    #             else:
    #                 continue
    #     sections.append(section)
    #     return sections

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
            exercise = self._extract_exercises(exercise_text)
            if type(exercise) == list:
                for ex in exercise:
                    exercise_list.append({
                    'section': section_name,
                    'name': ex['name'],
                    'reps': ex['reps'],
                    'rest': section_rest,
                    'weight': ex['weight'],
                    'time': ex['time']
                })
            else:
                exercise_list.append({
                    'section': section_name,
                    'name': exercise['name'],
                    'reps': exercise['reps'],
                    'rest': section_rest,
                    'weight': exercise['weight'],
                    'time': exercise['time']
                })
        return exercise_list

    def _extract_exercises(self, text: str):
        logging.debug(f"Received text: {text}")
        if type(text) != str:
            raise ValueError(f"Got {type(text)} expected 'str'")
        exercises = []
        exercise = {'name': None, 'reps': [], 'weight': 0, 'time': 0}

        name, info = text.split(':')
        logging.debug(f"Name: {name} - Info: {info}")
        if 'rest' in name.lower():
            logging.debug(f"Extracting rest string: {info}")
            exercise['rest'] = self._parse_rest_string(info)
        exercise['name'] = name.split('(')[0].strip()
        exercise_type = None
        if 'x' in info:
            logging.debug(f"Reps type exercise")
            reps = self._parse_reps_exercise(info)
            exercise['reps'] = reps
            try:
                weight = [self._extract_weight_from_name(name)]
            except ValueError as e:
                logging.debug(f"No weight to parse: {str(e)}")
            else:
                exercise['weight'] = weight
            exercises.append(exercise)

            neg_exercise = self._generate_negative(name, info)
            if neg_exercise is not None:
                exercises.append(neg_exercise)

        else:
            exercise_type = 'time'
            weight = self._extract_weight_from_name(name)
            time = self._extract_time(info)
            logging.debug(time)
            exercise['weight'] = weight
            exercise['time'] = time
            exercises.append(exercise)
        logging.debug(f"Returning exercises: {exercises}")
        return exercises

    def _extract_time(self, text):
        logging.debug(f"Extracting time from: '{text}'")
        p = re.compile(self.patterns['exercise']['exercise_time'])
        matches = p.match(text.strip())
        logging.debug(f"Time matches: {matches}")
        mins = int(matches.group(1))
        return mins * 60

    def _parse_reps_exercise(self, text: str):
        p = re.compile(self.patterns['exercise']['exercise_reps_only'])
        matches = p.findall(text)
        logging.debug(f"Reps matches: {matches}")
        if not matches:
            raise ValueError(f"No match for {text}")
        reps = [int(_set) for _set in matches]
        logging.debug(reps)
        return reps

    def _generate_negative(self, name: str, reps: str) -> Dict[str, Union[str, List[int]]]:
        logging.debug(f"Reps: {reps}")
        p = re.compile(self.patterns['exercise']['negative_reps'])
        matches = p.findall(reps)
        neg_reps = [int(neg) for neg in matches]
        if not neg_reps:
            return None
        return {
            "name": name + ' negatives',
            "reps": neg_reps,
            "weight": 0,
            "time": 0,
        }

    def _extract_weight_from_name(self, name):
        """Given a string with the name and weight of the exercise:
        'Barbell Squat (50kg+bar)' extract the weight value:
        50
        """
        p = re.compile(self.patterns['exercise']['exercise_weight'])
        matches = p.match(name)
        if not matches:
            raise ValueError(f"No match for {name}")
        return int(matches.group(1))



if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG, format="[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s")
    with open('data/20220912.txt') as f:
        data = f.read()
    result = WorkoutParser(data).parse()
    logging.debug(f"Result: {result}")