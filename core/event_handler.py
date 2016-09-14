from core.key_map import KeyMap


class EventHandler(object):

    def __init__(self, game_loop):
        self.pygame = game_loop.pygame
        self.key_map = KeyMap(game_loop)
        self.PYGAME_EVENT_TYPES = {
            self.pygame.KEYUP: self._handle_key_up,
            self.pygame.KEYDOWN: self._handle_key_down
        }

    def _handle_key_up(self, key):
        action = self.key_map.map_key_up_to_action(key)
        if callable(action):
            action()

    def _handle_key_down(self, key):
        action = self.key_map.map_key_down_to_action(key)
        if callable(action):
            action()

    def route_event(self, event):
        handler = self.PYGAME_EVENT_TYPES.get(event.type, None)
        if callable(handler) and event.key:
            handler(event.key)





