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

    def remove(self, observer):
        observer.subject = None
        if observer.next and observer.prev: # middle
            observer.next.prev = observer.prev
            observer.prev.next = observer.next
        elif not observer.prev: # first
            if observer.next:
                observer.next.prev = None
            else:
                self.head = observer = None
        elif not observer.next: # first
            observer.prev.next = None


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
