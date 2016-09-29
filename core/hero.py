import os
from pygame import image, Rect
from pygame.sprite import Sprite


class HeroManager(object):
    def __init__(self, screen=None, movement_manager=None, frame_rate=60):
        self.hero = None
        self.screen = screen
        self.frame_rate = frame_rate
        self.down = False

        events = [
            ('start_moving_right', self.handle_start_moving_right),
            ('stop_moving_right', self.handle_stop_moving_right)
        ]
        self.mm = movement_manager
        self.mm.subscribe_to_events(events)

    def _handle_idling(self):
        self.hero.idle_time += 1
        self.hero.is_idle = self.hero.idle_time > self.frame_rate * 5

    def _handle_movement(self):
        if self.mm.moving or self.hero.animating:
            self.hero.idle_time = 0
            self.hero.animate()

    def handle_stop_moving_right(self):
        if not self.mm.moving_right:
            self.hero.animate_moving_right_stop()

    def handle_start_moving_right(self):
        if self.mm.moving_right:
            self.hero.animate_moving_right_start()

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
    def __init__(self, app, files, layer=0, screen_height=0, screen_width=0):
        super(Hero, self).__init__()
        for key, file in files.iteritems():
            if isinstance(file, dict):
                for k, f in file.iteritems():
                    self._add_image(app, "{}_{}".format(key, k), f)
            else:
                self._add_image(app, key, file)

        self.image = self.image_idle #Always start rendering the hero in an idle state
        self._sprite_sheet_width = self.image.get_rect().width
        self._layer = layer
        self.frame_width = 200
        self.frame_height = 600
        self.frame_pos_x = 0
        self.frame_pos_y = - (screen_height - self.image.get_rect().height)
        self.middle = screen_width / 2 - self.frame_width / 2
        self.rect = self._get_rect()
        self.animating = False
        self.running_animations = []
        self.idle_time = 0
        self._hero_is_idle = False
        self.counter = 0

    def _add_image(self, app, key, file):
        asset_location = os.path.join(os.path.dirname(__file__), '../{}/assets/images/{}'.format(app, file))
        self.__setattr__('image_{}'.format(key), image.load(asset_location).convert_alpha())

    @property
    def is_idle(self):
        return self._hero_is_idle

    @is_idle.setter
    def is_idle(self, value):
        if not value:
            return

        self._set_new_image(self.image_idle)
        self.add_animation(self._animate_blink)

    def add_animation(self, animation):
        if animation not in self.running_animations:
            self.running_animations.append(animation)
            self.animating = True

    def _set_new_image(self, new_image):
        self.image = new_image
        self._sprite_sheet_width = self.image.get_rect().width

    def _get_rect(self):
        return Rect(self.frame_pos_x, self.frame_pos_y, self.frame_width, self.frame_height)

    def _animate_blink(self):
        if self.counter % 4 != 0:
            self.counter += 1
            return

        self._animate_image(self._animate_blink, None, loop=False)

    def animate_moving_right_start(self):
        self.frame_pos_x = 0
        self._set_new_image(self.image_moving_right_start)
        self._animate_image(self._animate_moving_right_start, None, loop=False)

    def _animate_moving_right_start(self):
        if self.counter % 5 != 0:
            self.counter += 1
            return

        self._animate_image(self._animate_moving_right_start, None, loop=False)
        if not self.animating:
            self._set_new_image(self.image_moving_right_middle)
            self._animate_image(self._animate_moving_right_middle, None)

    def _animate_moving_right_middle(self):
        if self.counter % 10 != 0:
            self.counter += 1
            return

        self._set_new_image(self.image_moving_right_middle)
        self._animate_image(self._animate_moving_right_middle, None)

    def animate_moving_right_stop(self):
        self.frame_pos_x = 0
        self._set_new_image(self.image_moving_right_stop)
        self._animate_image(self._animate_moving_right_stop, self._animate_moving_right_middle, loop=False)

    def _animate_moving_right_stop(self):
        if self.counter % 5 != 0:
            self.counter += 1
            return

        self._animate_image(self._animate_moving_right_stop, None, loop=False)
        if not self.animating:
            self._set_new_image(self.image_idle)

    def _animate_image(self, animation, previous_animation, loop=True):
        self.add_animation(animation)

        if previous_animation and previous_animation in self.running_animations:
            self.running_animations.remove(previous_animation)

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
            if not loop:
                self.running_animations.remove(animation)

    def animate(self):
        for animation in self.running_animations:
            animation()

    def draw(self, screen):
        screen.blit(self.image, (self.middle, 0), self.rect)
