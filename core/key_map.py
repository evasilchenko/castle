

class KeyMap(object):
    def __init__(self, game_loop, *args, **kwargs):
        self.pygame = game_loop.pygame
        self.info = game_loop.info
        self.background_manager = game_loop.background_manager
        self.key_map_up = {
            self.pygame.K_F1: game_loop.toggle_fullscreen,
            self.pygame.K_F2: self.info.toggle_fps,
            self.pygame.K_RIGHT: self.background_manager.stop_moving_right,
            self.pygame.K_LEFT: self.background_manager.stop_moving_left,
            self.pygame.K_UP: self.background_manager.stop_moving_up
        }
        self.key_map_down = {
            self.pygame.K_RIGHT: self.background_manager.start_moving_right,
            self.pygame.K_LEFT: self.background_manager.start_moving_left,
            self.pygame.K_UP: self.background_manager.start_moving_up
        }

    def map_key_up_to_action(self, key):
        return self.key_map_up.get(key)

    def map_key_down_to_action(self, key):
        return self.key_map_down.get(key)