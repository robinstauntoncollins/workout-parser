
class Exercise():

    @classmethod
    def from_dict(self, input_dict: dict):
        self.name = input_dict['name']
        self.reps = input_dict.get('reps') or []
        self.weight = input_dict.get('weight') or 0
        self.time = input_dict.get('time') or 0

    @classmethod
    def to_dict(self):
        return {
            'name': self.name,
            'reps': self.reps,
            'weight': self.weight,
            'time': self.time,
        }