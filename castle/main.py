from core.loop import GameLoop
from core.background import Background
from core.hero import Hero


class CastleGameLoop(GameLoop):
    def __init__(self):
        self.screen_width = 1300
        self.screen_height = 600
        self.app = 'castle'
        super(CastleGameLoop, self).__init__(res_w=self.screen_width, res_h=self.screen_height)

    def _setup_background(self):
        empty_sky = Background(self.app, 'empty_sky.png', screen_height=self.screen.get_height())
        clouds = Background(self.app, 'clouds.png', layer=1, screen_height=self.screen.get_height(), skip_every=2)
        bg_clouds = Background(self.app, 'clouds1.png', screen_height=self.screen.get_height())
        self.background_manager.add([empty_sky, bg_clouds])
        self.background_manager.add([clouds])

    def _setup_hero(self):
        hero_files = {
            'idle': 'hero.png',
            'moving_right': {
                'start':'hero_moving_right_start.png',
                'middle': 'hero_moving_right_middle.png',
                'stop': 'hero_moving_right_stop.png'
            }
        }
        hero = Hero(self.app, hero_files, screen_height=self.screen_height, screen_width=self.screen_width)
        self.hero_manager.add_hero(hero)

    def _fill_screen(self, **kwargs):
        color = (15, 122, 155) # Sky Blue
        self.screen.fill(color)

    def _draw_background(self):
        self.background_manager.draw()
