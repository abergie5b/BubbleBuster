from bubblebuster.timer import TimerMan

from enum import Enum
import pygame

class SimulationNames(Enum):
    REALTIME = 1
    FIXEDSTEP = 2
    SINGLESTEP = 3
    PAUSE = 4


class Simulation:
    instance = None
    SINGLE_TIME_STEP = 0.0166667
    def __init__(self):
        '''
           --------- Simulation controls ------------
           S - single step
           D - repeat step while holding
           G - start simulation fixed step
           H - start simulation realtime stepping
       '''
        super().__init__()
        self.state = SimulationNames.REALTIME
        self.tic = 0
        self.toc = 0
        self.total_watch = 0
        self.time_step = 0
        self.keyprev = 0
        Simulation.instance = self

    def update(self, current_time):
        self._process()

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

        #print('simulation state: %s total watch: %d time step: %d' % (
        #      self.state, self.total_watch, self.time_step)
        #)
        self.total_watch += self.time_step

    def _process(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_g]:
            self.state = SimulationNames.FIXEDSTEP

        elif keys[pygame.K_h]:
            self.state = SimulationNames.REALTIME

        elif keys[pygame.K_s] and self.keyprev == False:
            self.state = SimulationNames.SINGLESTEP

        elif keys[pygame.K_d]:
            self.state = SimulationNames.SINGLESTEP

        self.keyprev = (keys[pygame.K_s])

