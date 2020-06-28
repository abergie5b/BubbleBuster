from bubblebuster.input import InputObserver

class KeyPressObserver(InputObserver):
    def __init__(self, command, delta_time):
        self.command = command
        self.delta_time = delta_time

    def notify(self, screen, xcurs, ycurs):
        self.command.execute(self.delta_time)

