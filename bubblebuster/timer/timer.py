from bubblebuster.link import LinkMan
import bubblebuster.timer as timer

class TimerMan(LinkMan):
    instance = None
    def __init__(self):
        super().__init__()
        self.head = None
        self.current_time = 0
        TimerMan.instance = self

    def add(self, command, delta_time):
        event = timer.TimeEvent(command, delta_time)
        self.base_add(event)

    def compare(self, a, b):
        return a.command.name == b

    def find(self, command):
        return self.base_find(command)

    def remove(self, command):
        self.base_remove(command)

    def update(self, game, time):
        self.current_time = time
        head = self.head
        while head:
            next_ = head.next
            if self.current_time >= head.trigger_time:
                head.process()
                self.base_remove(head)
            head = next_

    @staticmethod
    def set_active(manager):
        TimerMan.instance = manager

