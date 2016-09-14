from core.loop import GameLoop
from core.background import Background, BackgroundManager
from core.event_handler import EventHandler


class CastleGameLoop(GameLoop):
    def __init__(self):
        super(CastleGameLoop, self).__init__()
        app = 'castle'
        clouds1 = Background(app, 'clouds1.png')
        empty_sky = Background(app, 'empty_sky.png')
        clouds2 = Background(app, 'clouds1.png')
        empty_sky2 = Background(app, 'empty_sky.png')
        self.background_manager = BackgroundManager(self.screen)
        self.background_manager.add([clouds1, empty_sky, clouds2, empty_sky2])
        self.event_handler = EventHandler(self)

    def _fill_screen(self, **kwargs):
        color = (15, 122, 155) # Sky Blue
        self.screen.fill(color)

    def _draw_background(self):
        self.background_manager.draw()
