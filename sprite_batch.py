import enum

class SpriteBatchNames(enum.Enum):
    MOUSE = 1


class SpriteBatch(Link):
    def __init__(self, name):
        self.name = name



class SpriteBatchMan(LinkMan):
    instance = None

    @staticmethod
    def create():
        if not SpriteBatchMan.instance:
            SpriteBatchMan.instance = SpriteBatchMan.__new__(SpriteBatchMan)
            SpriteBatchMan.instance.head = None

    @staticmethod
    def _get_instance():
        if not SpriteBatchMan.instance:
            SpriteBatchMan.instance = SpriteBatchMan.create()
        return SpriteBatchMan.instance

    @staticmethod
    def add(name, path):
        instance = SpriteBatchMan._get_instance()
        head = instance.head
        link = SpriteBatch(name, path)
        if not instance.head:
            instance.head = link
            return
        link.prev = None
        link.next = instance.head
        instance.head.prev = link
        instance.head = link

    @staticmethod
    def remove(link):
        instance = SpriteBatchMan._get_instance()
        head = instance.head
        while head:
            if head == link:
                if head.next and not head.prev:
                    head = head.next
                    head.prev = None
                    instance.head = head
                elif head.next and head.prev:
                    head.next.prev = head.prev
                    head.prev.next = head.next
                else:
                    if not head.prev: # only one on list
                        instance.head = None
                    else:
                        head.prev.next = None
                return
            head = head.next

    @staticmethod
    def find(link):
        head = SpriteBatchMan._get_instance().head
        while head:
            if head.name == link:
                return head
            head = head.next

    @staticmethod
    def print():
        head = SpriteBatchMan._get_instance().head
        while head:
            head.print()
            head = head.next

    @staticmethod
    def draw(screen):
        head = SpriteBatchMan._get_instance().head
        while head:
            head.draw(screen)
            head = head.next

