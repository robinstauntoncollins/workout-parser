from typing import List
from pprint import pprint
from datetime import datetime


def get_sections(input: str):
    sections = input.split('\n\n')
    pprint(f"Lines: {sections}")
    sections = [section.split('\n') for section in sections if section]
    return sections
    
def extract_line(line: str):
    name = line.split(' ')[0]
    weight = line.split('(')[0].split(')')
    reps = line.split(':')[1]
    return (name, weight, reps)

def parse_section(section: List[str]):
    """
        exercise name
        number of sets and their weights
        length of rest
        (notes)
    """
    exercises = {}
    for line in section:
        print(f"Extracting line: {line}")
        name, weight, reps = extract_line(line)
        if not exercises.get(name):
            exercises[name] = []
        exercises[name].append({
            'weight': weight,
            'reps': reps
        })

    return exercises

def is_date(text: str) -> bool:
    try:
        datetime.strptime(text, '%d %B %Y')
    except Exception:
        return False
    return True


if __name__ == '__main__':
    with open('data/20220912.txt', 'r') as f:
        data = f.read()
    sections = get_sections(data)
    pprint(f"Sections: {sections}")
    for section in sections[1::]:
        print(f"Parsing section: {section}")
        exercises = parse_section(section)
        pprint(f"Parsed section: {exercises}")
        print()