from datetime import datetime

def parse_date(raw: str) -> str:
    date = datetime.strptime(raw, '%d %B %Y')
    return date.isoformat()