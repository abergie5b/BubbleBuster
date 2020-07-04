from bubblebuster.link import Link
from bubblebuster.timer import TimerMan

from enum import Enum

class TimeEventNames(Enum):
    CLICKEXPLODE = 1
    FADEOUTTOAST = 2
    DESTROYSPRITE = 3
    MINICLICKEXPLODE = 4
    REMOVEFONT = 5
    SWITCHSCENE = 6
    SECONDCHANCE = 7
    COLORCHANGEBUBBLE = 8
    ADDTOCIRCLEGROUP = 9


class TimeEvent(Link):
    def __init__(self, command, delta_time):
        super().__init__()
        self.command = command
        self.delta_time = delta_time
        self.trigger_time = TimerMan.instance.current_time + delta_time

    def process(self):
        self.command.execute(self.delta_time)

