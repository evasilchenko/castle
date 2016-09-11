import pygame

from core.event_handler import EventHandler


class GameLoop(object):

    def __init__(self, frame_rate=60, res_w=800, res_h=600):
        self.pygame = pygame
        self.pygame.init()
        self.screen = pygame.display.set_mode([res_w, res_h])
        self.frame_rate = frame_rate
        self.clock = pygame.time.Clock()
        self.event_handler = EventHandler(self.pygame)
        self.info = self.event_handler.key_map.info

    def _fill_screen(self, color=(255, 255, 255)):
        self.screen.fill(color)

    def _deal_with_events(self):
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                return False

            self.event_handler.route_event(event)
        return True # Game Loop is still alive

    def _quit(self):
        self.pygame.quit()

    def start_game(self):
        while self._deal_with_events():
            self._fill_screen()
            self.info.show_fps(self.clock, self.screen)
            self.pygame.display.flip()
            self.clock.tick(self.frame_rate)
        self._quit()
