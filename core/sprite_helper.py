import os
from pygame import image, transform
from pygame.sprite import Sprite


class SpriteHelper(Sprite):
    def __init__(self, app='', file='', layer=0, copy_from=None, screen_height=0, skip_every=None):
        super(SpriteHelper, self).__init__()
        asset_location = os.path.join(os.path.dirname(__file__), '../{}/assets/images/{}'.format(app, file))
        self.image = getattr(copy_from, 'image') if copy_from else image.load(asset_location).convert_alpha()
        self._layer = getattr(copy_from, '_layer') if copy_from else layer
        self.skip_every = getattr(copy_from, 'skip_every') if copy_from else skip_every
        self._scale_to_resolution(screen_height, None)
        self.rect = self.image.get_rect()

    def _scale_to_resolution(self, screen_height, scale_up):
        scale_up = int(1 if scale_up else -1) if scale_up is not None else 0
        ratio = self.image.get_height() * 1.0 / self.image.get_width()
        self.image = transform.smoothscale(self.image, (int(screen_height / ratio) + scale_up, screen_height))
        self.image = self.image.convert_alpha()

    def scale_to_resolution(self, screen_height, scale_up):
        self._scale_to_resolution(screen_height, scale_up)