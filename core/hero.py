import os
from pygame import image, Rect
from pygame.sprite import Sprite


class HeroManager(object):
    def __init__(self, screen=None, movement_manager=None, frame_rate=60):
        self.hero = None
        self.screen = screen
        self.frame_rate = frame_rate
        self.down = False
        self.mm = movement_manager


    def _handle_idling(self):
        self.hero.idle_time += 1
        self.hero.is_idle = self.hero.idle_time > self.frame_rate * 5

    def _handle_movement(self):
        if self.mm.moving_right:
            self.hero.idle_time = 0

        if self.mm.moving_left:
            self.hero.idle_time = 0

        if self.hero.animating and not self.hero.is_idle:
            self.hero.idle_time = 0
            self.hero.animate()

    def start_animating_blink(self):
        self.hero.animating = True

    def add_hero(self, hero=None):
        if not hero:
            raise Exception("You can't have a story without a hero...")

        self.hero = hero

    def draw(self, screen=None):
        self._handle_idling()
        self._handle_movement()
        self.hero.draw(screen or self.screen)


class Hero(Sprite):
    def __init__(self, app, file='', layer=0, screen_height=0, screen_width=0):
        asset_location = os.path.join(os.path.dirname(__file__), '../{}/assets/images/{}'.format(app, file))
        super(Hero, self).__init__()
        self.image = image.load(asset_location).convert_alpha()
        self._sprite_sheet_width = self.image.get_rect().width
        self._layer = layer
        self.frame_width = 200
        self.frame_height = 400
        self.frame_pos_x = 0
        self.frame_pos_y = - (screen_height - self.image.get_rect().height)
        self.middle = screen_width / 2 - self.frame_width / 2
        self.rect = self._get_rect()
        self.animating = False
        self.running_animations = []
        self.idle_time = 0
        self._hero_is_idle = False
        self.counter = 0

    @property
    def is_idle(self):
        return self._hero_is_idle

    @is_idle.setter
    def is_idle(self, value):
        if not value:
            return

        if self._animate_blink not in self.running_animations:
            self.running_animations.append(self._animate_blink)
            self.animating = True
            self.animate()

    def _get_rect(self):
        return Rect(self.frame_pos_x, self.frame_pos_y, self.frame_width, self.frame_height)

    def _animate_blink(self):
        if self.counter % 4 != 0:
            self.counter += 1
            return

        if self.frame_pos_x < self._sprite_sheet_width - self.frame_width:
            self.frame_pos_x += self.frame_width
            self.rect = self._get_rect()
            self.counter += 1
        else:
            self.frame_pos_x = 0
            self.animating = False
            self.rect = self._get_rect()
            self.counter = 0
            self.idle_time = 0
            self.is_idle = False
            self.running_animations.remove(self._animate_blink)

    def animate(self):
        for animation in self.running_animations:
            animation()

    def draw(self, screen):
        screen.blit(self.image, (self.middle, 0), self.rect)
