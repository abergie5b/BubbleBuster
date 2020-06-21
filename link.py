
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

    def create(self):
        raise NotImplementedError('this is an abstract method')

    def compare(self, a, b):
        raise NotImplementedError('this is an abstract method')

    def wash(self):
        raise NotImplementedError('this is an abstract method')

    def _get_instance(self):
        raise NotImplementedError('this is an abstract method')

    def base_add(self, link):
        head = self.instance.head
        if not self.instance.head:
            self.instance.head = link
            return
        link.prev = None
        link.next = self.instance.head
        self.instance.head.prev = link
        self.instance.head = link

    def base_remove(self, link):
        head = self.instance.head
        while head:
            if head == link:
                if head.next and not head.prev:
                    head = head.next
                    head.prev = None
                    self.instance.head = head
                elif head.next and head.prev:
                    head.next.prev = head.prev
                    head.prev.next = head.next
                else:
                    if not head.prev: # only one on list
                        self.instance.head = None
                    else:
                        head.prev.next = None
                return
            head = head.next

    def base_find(self, link):
        head = self.instance.head
        while head:
            if self.instance.compare(head, link):
                return head
            head = head.next

    def print(self):
        head = self.instance.head
        while head:
            head.print()
            head = head.next

