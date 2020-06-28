import bubblebuster.input.subject as subject

class InputSubject(subject.Subject):
    def __init__(self):
        self.objA = None
        self.objB = None
        self.head = None

    def notify(self, screen, xcurs, ycurs):
        observer = self.head
        while observer:
            observer.notify(screen, xcurs, ycurs)
            observer = observer.next

