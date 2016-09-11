

class Information(object):
    def __init__(self, pygame):
        self.pygame = pygame
        self.display_fps = False

    def _show_fps(self, clock, screen):
        font = self.pygame.font.SysFont('Calibri', 25, True, False)
        text = font.render("fps: {0:.2f}".format(clock.get_fps()), True, (0, 0, 0))
        screen.blit(text, [0, 0])

    def show_fps(self, clock, screen):
        if self.display_fps:
            self._show_fps(clock, screen)

    def toggle_fps(self):
        self.display_fps = not self.display_fps
