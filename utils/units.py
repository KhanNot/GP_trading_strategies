class Volume:
    def __init__(self, value: float):
        self.value = value
    def __reduce__(self):
        return (self.__class__, (self.name, self.age))

class Dollar:
    def __init__(self, value: float):
        self.value = value
    def __reduce__(self):
        return (self.__class__, (self.name, self.age))