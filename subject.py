
class Subject:
    def __init__(self):
        raise NotImplementedError('this is a base class')

    def attach(self, observer):
        observer.subject = self
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

