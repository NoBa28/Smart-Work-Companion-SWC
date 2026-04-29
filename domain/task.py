class Task:

    def __init__(self, id: str, title: str, priority: str, done: bool = False):
        self.id = id
        self.title = title
        self.priority = priority
        self.done = done

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Task(**data)
