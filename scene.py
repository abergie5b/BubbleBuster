

class Scene(Link):
    def __init__(self):
        super().__init__()


class SceneMan(LinkMan):
    instance = None

    @staticmethod
    def create():
        if not SceneMan.instance:
            SceneMan.instance = SceneMan.__new__(SceneMan)
            SceneMan.instance.head = None
        return SceneMan.instance

    def add(self, scene):
        self.base_add(scene)

    def remove(self, scene):
        self.base_remove(scene)


