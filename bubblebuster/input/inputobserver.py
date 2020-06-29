from bubblebuster.link import Link

class InputObserver(Link):
    def notify(self, screen, xcurs, ycurs):
        raise NotImplementedError('this is an abstract method')

