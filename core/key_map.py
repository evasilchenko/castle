from core.info import Information

class KeyMap(object):
    def __init__(self, pygame, *args, **kwargs):
        self.pygame = pygame
        self.info = Information(self.pygame)
        self.key_map = {
            self.pygame.K_UP: self.info.toggle_fps
        }

    def map_key_to_action(self, key):
        return self.key_map[key]