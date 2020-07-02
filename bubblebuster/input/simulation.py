from bubblebuster.timer import TimerMan

from enum import Enum
import pygame

class SimulationNames(Enum):
    REALTIME = 1
    FIXEDSTEP = 2
    SINGLESTEP = 3
    PAUSE = 4


# --- Simulation controls ------------
#   S - single step
#   D - repeat step while holding
#   G - start simulation fixed step
#   H - start simulation realtime stepping
class Simulation:
    instance = None
    SINGLE_TIME_STEP = 0.016666
    def __init__(self):
        super().__init__()
        self.state = SimulationNames.SINGLESTEP
        self.tic = 0
        self.toc = 0
        self.total_watch = 0
        self.time_step = 0
        self.keyprev = 0
        Simulation.instance = self

    def update(self, event):
        self._process(event)

        current_time = TimerMan.instance.current_time
        self.toc = current_time - self.tic
        self.tic = current_time

        if self.state == SimulationNames.FIXEDSTEP:
            self.time_step = Simulation.SINGLE_TIME_STEP
        elif self.state == SimulationNames.REALTIME:
            self.time_step = self.toc
        elif self.state == SimulationNames.SINGLESTEP:
            self.time_step = Simulation.SINGLE_TIME_STEP
            self.state = SimulationNames.PAUSE
        elif self.state == SimulationNames.PAUSE:
            self.time_step = 0
        else:
            raise AttributeError('invalid simulation state: %s' % self.state)

        self.total_watch += self.time_step

    def _process(self, event):
        key = event.key
        if key == pygame.K_g:
            self.state = SimulationNames.FIXEDSTEP
        elif key == pygame.K_h:
            self.state = SimulationNames.REALTIME
        elif key == pygame.K_s and self.keyprev == False:
            self.state = SimulationNames.SINGLESTEP
        elif key == pygame.K_d:
            self.state = SimulationNames.SINGLESTEP
        self.keyprev = key == pygame.K_s
    