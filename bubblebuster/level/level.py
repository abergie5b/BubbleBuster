

class Level(Link):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings


class LevelMan(LinkMan):
    def compare(self, a, b):
        return a.name == b

    def add(self, name, data):
        image = Level(name, data)
        self.base_add(image)

    def find(self, image):
        return self.base_find(image)

    @staticmethod
    def set_active(manager):
        LevelMan.instance = manager

