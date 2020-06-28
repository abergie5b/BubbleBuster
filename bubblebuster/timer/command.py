from bubblebuster.link import Link

class Command(Link):
    def __init__(self):
        raise NotImplementedError('this is a singleton class')

    def execute(self, delta_time, *args):
        raise NotImplementedError('this is an abstract method')
