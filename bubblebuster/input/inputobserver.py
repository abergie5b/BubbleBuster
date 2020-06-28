from bubblebuster.link import Link

class InputObserver(Link):
    def __init__(self):
        pass

    def notify(self, screen, xcurs, ycurs):
        raise NotImplementedError('this is an abstract method')

