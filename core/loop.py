import pygame

from core.event_handler import EventHandler
from core.info import Information


class GameLoop(object):

    def __init__(self, frame_rate=60, res_w=800, res_h=600):
        self.pygame = pygame
        self.pygame.init()
        self.screen = pygame.display.set_mode([res_w, res_h])
        self.frame_rate = frame_rate
        self.clock = pygame.time.Clock()
        self.info = Information(self.pygame)

    def _fill_screen(self, color=(255, 255, 255)):
        self.screen.fill(color)

    def _deal_with_events(self):
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                self._quit()

            self.event_handler.route_event(event)
        return True # Game Loop is still alive

    def _draw_background(self):
        raise NotImplementedError

    def _quit(self):
        self.pygame.quit()

    def start_game(self):
        while True:
            self._deal_with_events()
            self._fill_screen()
            self._draw_background()
            self.info.show_fps(self.clock, self.screen)
            self.pygame.display.flip()
            self.clock.tick(self.frame_rate)
