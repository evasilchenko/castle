from core.loop import GameLoop
from core.background import Background, BackgroundManager
from core.event_handler import EventHandler


class CastleGameLoop(GameLoop):
    def __init__(self):
        self.screen_width = 1300
        self.screen_height = 600
        super(CastleGameLoop, self).__init__(res_w=self.screen_width, res_h=self.screen_height)
        app = 'castle'
        empty_sky = Background(app, 'empty_sky.png')
        clouds = Background(app, 'clouds.png', layer=1)
        self.background_manager = BackgroundManager(self.screen)
        self.background_manager.add([empty_sky])
        self.background_manager.add([clouds], skip_every=1)
        self.event_handler = EventHandler(self)

    def _fill_screen(self, **kwargs):
        color = (15, 122, 155) # Sky Blue
        self.screen.fill(color)

    def _draw_background(self):
        self.background_manager.draw()
