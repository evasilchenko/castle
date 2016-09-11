from core.key_map import KeyMap


class EventHandler(object):

    def __init__(self, pygame):
        self.pygame = pygame
        self.key_map = KeyMap(self.pygame)
        self.PYGAME_EVENT_TYPES = {
            self.pygame.KEYUP: self._handle_key_up,
            self.pygame.KEYDOWN: self._handle_key_down
        }

    def _handle_key_up(self, key):
        action = self.key_map.map_key_to_action(key)
        action()

    def _handle_key_down(self, key):
        pass

    def route_event(self, event):
        handler = self.PYGAME_EVENT_TYPES.get(event.type, None)
        if handler and event.key:
            handler(event.key)





