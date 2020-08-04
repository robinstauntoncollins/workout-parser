from datetime import datetime

from workout.parse import parse_date

def parse(raw: str) -> dict:
    lines = raw.split('\n\n')
    date = parse_date(lines[0])


if __name__ == '__main__':
    with open('data/20200803.txt') as f:
        raw = f.read()
    result = parse(raw)