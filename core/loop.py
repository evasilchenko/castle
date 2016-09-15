import pygame

from core.event_handler import EventHandler
from core.info import Information


class GameLoop(object):

    def __init__(self, frame_rate=60, res_w=800, res_h=600):
        self.pygame = pygame
        self.pygame.init()
        display_info = self.pygame.display.Info()
        self.display_res_w = display_info.current_w
        self.display_res_h = display_info.current_h
        self.window_res_w = res_w
        self.window_res_h = res_h
        self.screen = pygame.display.set_mode([res_w, res_h])
        self.frame_rate = frame_rate
        self.clock = pygame.time.Clock()
        self.info = Information(self.pygame)
        self.full_screen = False

    def _fill_screen(self, color=(255, 255, 255)):
        self.screen.fill(color)

    def _deal_with_events(self):
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                self._quit()
            self.event_handler.route_event(event)

    def _setup_event_handler(self):
        raise NotImplementedError

    def _setup_background_manager(self):
        raise NotImplementedError

    def _draw_background(self):
        raise NotImplementedError

    def toggle_fullscreen(self):
        if self.full_screen:
            self.screen = self.pygame.display.set_mode((self.window_res_w, self.window_res_h), self.pygame.RESIZABLE)
        else:
            self.screen = self.pygame.display.set_mode((self.display_res_w, self.display_res_h), self.pygame.FULLSCREEN)

        self.full_screen = not self.full_screen
        self._setup_background_manager()
        self._setup_event_handler()


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
