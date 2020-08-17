import re

class WorkoutParser():
    
    def __init__(self, raw):
        self.raw = raw

    def parse(self):
        date = self._extract_date()
        return date

    def _extract_date(self):
        pattern = r"[\d]{1,2}(?:[trns]\w*)? [ADFJMNOS]\w* [\d]{4}"
        p = re.compile(pattern)
        return p.search(self.raw).group()
    