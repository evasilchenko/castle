import os
from pygame import image, Rect

from core.sprite_helper import SpriteHelper


class CharacterManager(object):
    def __init__(self, screen=None, movement_manager=None, frame_rate=60):
        self.screen = screen
        self.frame_rate = frame_rate
        self.down = False
        self.mm = movement_manager


class Character(SpriteHelper):
    def __init__(self, *args, **kwargs):
        super(Character, self).__init__(*args, **kwargs)
        for key, file in files.iteritems():
            if isinstance(file, dict):
                for k, f in file.iteritems():
                    self._add_image(self.app, "{}_{}".format(key, k), f)
            else:
                self._add_image(self.app, key, file)

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
        self.counter = 0
        self.health = health

    def _add_image(self, app, key, file):
        asset_location = os.path.join(os.path.dirname(__file__), '../{}/assets/images/{}'.format(app, file))
        self.__setattr__('image_{}'.format(key), image.load(asset_location).convert_alpha())

    def add_animation(self, animation):
        if animation not in self.running_animations:
            self.running_animations.append(animation)
            self.animating = True

    def _set_new_image(self, new_image):
        self.image = new_image
        self._sprite_sheet_width = self.image.get_rect().width

    def _get_rect(self):
        return Rect(self.frame_pos_x, self.frame_pos_y, self.frame_width, self.frame_height)

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