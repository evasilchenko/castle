

class KeyMap(object):
    def __init__(self, game_loop, *args, **kwargs):
        self.pygame = game_loop.pygame
        self.info = game_loop.info
        self.background_manager = game_loop.background_manager
        self.hero_manager = game_loop.hero_manager
        self.movement_manager = game_loop.movement_manager
        self.key_map_up = {
            self.pygame.K_F1: game_loop.toggle_fullscreen,
            self.pygame.K_F2: self.info.toggle_fps,
            self.pygame.K_RIGHT: self.movement_manager.stop_moving_right,
            self.pygame.K_LEFT: self.movement_manager.stop_moving_left,
            self.pygame.K_UP: self.movement_manager.stop_moving_up,
            self.pygame.K_DOWN: self.hero_manager.start_animating_blink
        }
        self.key_map_down = {
            self.pygame.K_RIGHT: self.movement_manager.start_moving_right,
            self.pygame.K_LEFT: self.movement_manager.start_moving_left,
            self.pygame.K_UP: self.movement_manager.start_moving_up
        }

    def get_key_up_action(self, key):
        return self.key_map_up.get(key)

    def get_key_down_action(self, key):
        return self.key_map_down.get(key)