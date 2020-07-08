from bubblebuster.link import *

class Subject(Link):
    def __init__(self):
        super().__init__()

    def attach(self, observer):
        observer.subject = self
        head = self.head
        if not self.head:
            observer.next = None
            observer.prev = None
            self.head = observer
        else:
            observer.next = head
            observer.prev = None
            self.head.prev = observer
            self.head = observer
        return observer

    def remove(self, observer):
        self.base_remove(observer)

    def base_remove_single(self, head):
        if head.next and not head.prev:
            head = head.next
            head.prev = None
            self.head = head
        elif head.next and head.prev:
            head.next.prev = head.prev
            head.prev.next = head.next
        else:
            if not head.prev: # only one on list
                self.head = None
            else:
                head.prev.next = None

    def base_remove(self, link):
        head = self.head
        while head:
            if head == link:
                head.observer = None
                self.base_remove_single(head)
                return
            head = head.next

class CollisionSubject(Subject):
    def __init__(self):
        self.objA = None
        self.objB = None
        self.head = None

    def notify(self):
        head = self.head
        while head:
            head.notify()
            head = head.next
