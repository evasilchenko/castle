import os
from pygame import image
from pygame.sprite import Sprite, LayeredUpdates

class BackgroundManager(object):
    def __init__(self, screen=None):
        self.layers = LayeredUpdates()
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.screen = screen
        self.y_position = 0
        self.drop_speed = 1

    def _get_all_sprites(self):
        for layer in self.layers.layers():
            yield self.layers.get_sprites_from_layer(layer)

    def _handle_movement(self):
        move_speed = 1
        if self.moving_right:
            for layer_sprites in self._get_all_sprites():
                self._move_right(layer_sprites, move_speed)
                move_speed *= 2

        if self.moving_left:
            for layer_sprites in self._get_all_sprites():
                self._move_left(layer_sprites, move_speed)
                move_speed *= 2

        if self.moving_up and self.y_position < 150:
            move_speed *= 4
            for layer_sprites in self._get_all_sprites():
                self._move_up(layer_sprites, move_speed)
        elif self.y_position >= 150:
            self.moving_up = False
            self.moving_down = True

        if self.moving_down and self.y_position > 0:
            self.drop_speed *= 2
            for layer_sprites in self._get_all_sprites():
                self._move_down(layer_sprites, self.drop_speed)
        elif self.y_position <= 0:
            self.moving_down = False
            self.drop_speed = 1

    def _set_tile_position(self, background):
        sprites = self.layers.get_sprites_from_layer(background._layer)
        last_sprite = sprites[len(sprites) - 1] if self.layers.get_sprites_from_layer(background._layer) else None
        background.rect.x = (last_sprite.rect.x + last_sprite.rect.width) if last_sprite else 0

    def draw(self, screen=None):
        self._handle_movement()
        self.layers.draw(screen or self.screen)

    def add(self, backgrounds, repeat_tiles=True):
        for background in backgrounds:
            self._set_tile_position(background)
            self.layers.add(background)

    def _move_right(self, sprites, amount=1):
        for sprite in sprites:
            sprite.rect.x -= amount

    def _move_left(self, sprites, amount=1):
        for sprite in sprites:
            sprite.rect.x += amount

    def _move_up(self, sprites, amount=1):
        for sprite in sprites:
            sprite.rect.y += amount
            self.y_position = sprite.rect.y

    def _move_down(self, sprites, amount=1):
        for sprite in sprites:
            sprite.rect.y = (sprite.rect.y - amount) if (sprite.rect.y - amount) >= 0 else 0
            self.y_position = sprite.rect.y

    def stop_moving_left(self):
        self.moving_left = False

    def start_moving_left(self):
        self.moving_right = False
        self.moving_left = True

    def stop_moving_right(self):
        self.moving_right = False

    def start_moving_right(self):
        self.moving_right = True
        self.moving_left = False

    def stop_moving_up(self):
        self.drop_speed = 1
        self.moving_up = False
        self.moving_down = True

    def start_moving_up(self):
        if not self.moving_down:
            self.moving_up = True


class Background(Sprite):
    def __init__(self, app, file, layer=0):
        asset_location = os.path.join(os.path.dirname(__file__), '../{}/assets/images/{}'.format(app, file))
        super(Background, self).__init__()
        self.image = image.load(asset_location).convert()
        self.rect = self.image.get_rect()
        self._layer = layer
