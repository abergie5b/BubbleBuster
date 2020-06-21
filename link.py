
class Link:
    def __init__(self):
        self.next = None
        self.prev = None

    def wash(self):
        self.next = None
        self.prev = None

    def print(self):
        raise NotImplementedError('this method is abstract')


class LinkMan:
    instance = None 

    def __init__(self):
        raise NotImplementedError('this is a singleton class')

    @staticmethod
    def create():
        if not __class__.instance:
            __class__.instance = __class__.__new__(__class__)
            __class__.instance.head = None

    @staticmethod
    def _get_instance():
        if not __class__.instance:
            __class__.instance = __class__.create()
        return __class__.instance

    @staticmethod
    def add(link):
        instance = __class__._get_instance()
        head = instance.head
        if not instance.head:
            instance.head = link
            return
        link.prev = None
        link.next = instance.head
        instance.head.prev = link
        instance.head = link

    @staticmethod
    def remove(link):
        instance = __class__._get_instance()
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
        instance = __class__._get_instance()
        head = instance.head
        print(__class__.__name__)
        while head:
            if head.name == link:
                return instance.compare(link)
            head = head.next

    @staticmethod
    def print():
        head = __class__._get_instance().head
        while head:
            head.print()
            head = head.next

    @staticmethod
    def draw(screen):
        head = __class__._get_instance().head
        while head:
            head.draw(screen)
            head = head.next

