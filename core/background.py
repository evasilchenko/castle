import os
from pygame import image
from pygame import transform
from pygame.sprite import LayeredUpdates

from core.sprite_helper import SpriteHelper

class BackgroundManager(object):
    def __init__(self, screen=None, movement_manager=None):
        self.layers = LayeredUpdates()
        self.layers_copy = None
        self.screen = screen
        self.mm = movement_manager

    def resize_layers_to_resolution(self, scale_up):
        height = self.screen.get_height()
        for sprite in self.layers.sprites():
            sprite.scale_to_resolution(height, scale_up)

    def _get_all_sprites(self):
        for layer in self.layers.layers():
            yield self.layers.get_sprites_from_layer(layer)

    def _move_to_end(self, first, last):
        first.rect.x = last.rect.right + (last.rect.width * last.skip_every + 1 if last.skip_every else 0)
        self.layers.remove(first)
        self.layers.add(first)

    def _move_to_start(self, sprites):
        self.layers.remove(sprites)
        last = sprites.pop(len(sprites) - 1)
        last.rect.x = sprites[0].rect.x - (sprites[0].rect.width * (sprites[0].skip_every + 1) if sprites[0].skip_every else last.rect.width)
        sprites.insert(0, last)
        self.layers.add(sprites)

    def _handle_movement(self):
        move_speed = 1
        if self.mm.moving_right:
            for layer_sprites in self._get_all_sprites():
                self._move_right(layer_sprites, move_speed)
                move_speed *= 2
                if self._check_left_bounds(layer_sprites[0]):
                    self._move_to_end(layer_sprites[0], layer_sprites[len(layer_sprites) - 1])

        if self.mm.moving_left:
            for layer_sprites in self._get_all_sprites():
                self._move_left(layer_sprites, move_speed)
                move_speed *= 2
                if self._check_right_bounds(layer_sprites[len(layer_sprites) - 1]):
                    self._move_to_start(layer_sprites)

        if self.mm.moving_up:
            move_speed *= 2
            for layer_sprites in self._get_all_sprites():
                self._move_up(layer_sprites, move_speed)
                move_speed *= 3

        if self.mm.moving_down:
            self.mm.drop_speed *= 2
            for layer_sprites in self._get_all_sprites():
                self._move_down(layer_sprites, self.mm.drop_speed)

    def _check_left_bounds(self, first_sprite):
        return first_sprite.rect.right <= 0

    def _check_right_bounds(self, last_sprite):
        return last_sprite.rect.x >= self.screen.get_width()

    def _get_last_sprite_in_layer(self, layer):
        sprites = self.layers.get_sprites_from_layer(layer)
        last_sprite = sprites[len(sprites) - 1] if self.layers.get_sprites_from_layer(layer) else None
        return last_sprite

    def _create_tiles(self, backgrounds, fill, x_position=None):
        last_sprite = self._get_last_sprite_in_layer(backgrounds[0]._layer)
        x_pos = x_position or last_sprite.rect.right if last_sprite else 0
        tile_position = None
        for background in backgrounds:
            background.height = self.screen.get_height()
            background.rect.x = x_pos
            x_pos = background.rect.right
            self.layers.add(background)
        tile_position = background.rect.right + ((background.rect.width * background.skip_every + 1) if background.skip_every else 0)
        continue_tiling = fill and (tile_position < self.screen.get_width() + background.rect.width)
        if continue_tiling:
            self._create_tiles([Background(copy_from=background, screen_height=self.screen.get_height()) for background in backgrounds], fill, x_position=tile_position)

    def draw(self, screen=None):
        self._handle_movement()
        self.layers.draw(screen or self.screen)

    def add(self, backgrounds, repeat_pattern=True):
        self._create_tiles(backgrounds, repeat_pattern)

    def _move_right(self, sprites, amount=1):
        for sprite in sprites:
            sprite.rect.x -= amount

    def _move_left(self, sprites, amount=1):
        for sprite in sprites:
            sprite.rect.x += amount

    def _move_up(self, sprites, amount=1):
        for sprite in sprites:
            sprite.rect.y += amount

    def _move_down(self, sprites, amount=1):
        for sprite in sprites:
            sprite.rect.y = (sprite.rect.y - amount) if (sprite.rect.y - amount) >= 0 else 0

class Background(SpriteHelper):
    def __init__(self, *args, **kwargs):
        super(Background, self).__init__(*args, **kwargs)
