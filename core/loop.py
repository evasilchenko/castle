import pygame

from core.background import BackgroundManager
from core.enemy import EnemyManager
from core.event_handler import EventHandler
from core.hero import HeroManager
from core.info import Information
from core.movement import MovementManager


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
        self._setup_movement_manager()
        self._setup_background_manager()
        self._setup_hero_manager()
        self._setup_enemy_manager()
        self._setup_event_handler()

    def _fill_screen(self, color=(255, 255, 255)):
        self.screen.fill(color)

    def _deal_with_events(self):
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                self._quit()
            self.event_handler.route_event(event)

    def _setup_event_handler(self):
        self.event_handler = EventHandler(self)

    def _setup_background(self):
        raise NotImplementedError

    def _setup_hero(self):
        raise NotImplementedError

    def _setup_movement_manager(self):
        self.movement_manager = MovementManager()

    def _setup_background_manager(self):
        self.background_manager = BackgroundManager(self.screen, self.movement_manager)
        self._setup_background()

    def _setup_hero_manager(self):
        self.hero_manager = HeroManager(self.screen, movement_manager=self.movement_manager, frame_rate=self.frame_rate)
        self._setup_hero()

    def _setup_enemy_manager(self):
        self.enemy_manager = EnemyManager(self.screen, frame_rate=self.frame_rate)
        self._setup_enemies()

    def _handle_movement(self):
        self.movement_manager._handle_movement()

    def _draw_background(self):
        self.background_manager.draw()

    def _draw_hero(self):
        self.hero_manager.draw()

    def toggle_fullscreen(self):
        if self.full_screen:
            self.screen = self.pygame.display.set_mode((self.window_res_w, self.window_res_h), self.pygame.RESIZABLE)
        else:
            self.screen = self.pygame.display.set_mode((self.display_res_w, self.display_res_h), self.pygame.RESIZABLE)

        self.background_manager.resize_layers_to_resolution(self.full_screen)
        self.full_screen = not self.full_screen

    def _quit(self):
        self.pygame.quit()

    def start_game(self):
        while True:
            self._deal_with_events()
            self._fill_screen()
            self._handle_movement()
            self._draw_background()
            self._draw_hero()
            self._draw_enemies()
            self.info.show_fps(self.clock, self.screen)
            self.pygame.display.flip()
            self.clock.tick(self.frame_rate)
