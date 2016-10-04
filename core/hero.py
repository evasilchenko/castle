from core.character import Character, CharacterManager


class HeroManager(CharacterManager):
    def __init__(self, *args, **kwargs):
        super(HeroManager, self).__init__(*args, **kwargs)

        events = [
            ('start_moving_right', self.handle_start_moving_right),
            ('stop_moving_right', self.handle_stop_moving_right)
        ]
        self.mm.subscribe_to_events(events)
        self.hero = None

    def _handle_idling(self):
        self.hero.idle_time += 1
        self.hero.is_idle = self.hero.idle_time > self.frame_rate * 5

    def _handle_movement(self):
        if self.mm.moving or self.hero.animating:
            self.hero.idle_time = 0
            self.hero.animate()

    def handle_stop_moving_right(self):
        if not self.mm.moving_right:
            self.hero.animate_moving_right_stop()

    def handle_start_moving_right(self):
        if self.mm.moving_right:
            self.hero.animate_moving_right_start()

    def start_animating_blink(self):
        self.hero.animating = True

    def add_hero(self, hero=None):
        if not hero:
            raise Exception("You can't have a story without a hero...")

        self.hero = hero

    def draw(self, screen=None):
        self._handle_idling()
        self._handle_movement()
        self.hero.draw(screen or self.screen)


class Hero(Character):

    def __init__(self, *args, **kwargs):
        super(Hero, self).__init__(*args, **kwargs)
        self.idle_time = 0
        self._hero_is_idle = False

    @property
    def is_idle(self):
        return self._hero_is_idle

    @is_idle.setter
    def is_idle(self, value):
        if not value:
            return

        self._set_new_image(self.image_idle)
        self.add_animation(self._animate_blink)

    def _animate_blink(self):
        if self.counter % 4 != 0:
            self.counter += 1
            return

        self._animate_image(self._animate_blink, None, loop=False)

    def animate_moving_right_start(self):
        self.frame_pos_x = 0
        self._set_new_image(self.image_moving_right_start)
        self._animate_image(self._animate_moving_right_start, None, loop=False)

    def _animate_moving_right_start(self):
        if self.counter % 5 != 0:
            self.counter += 1
            return

        self._animate_image(self._animate_moving_right_start, None, loop=False)
        if not self.animating:
            self._set_new_image(self.image_moving_right_middle)
            self._animate_image(self._animate_moving_right_middle, None)

    def _animate_moving_right_middle(self):
        if self.counter % 10 != 0:
            self.counter += 1
            return

        self._set_new_image(self.image_moving_right_middle)
        self._animate_image(self._animate_moving_right_middle, None)

    def animate_moving_right_stop(self):
        self.frame_pos_x = 0
        self._set_new_image(self.image_moving_right_stop)
        self._animate_image(self._animate_moving_right_stop, self._animate_moving_right_middle, loop=False)

    def _animate_moving_right_stop(self):
        if self.counter % 5 != 0:
            self.counter += 1
            return

        self._animate_image(self._animate_moving_right_stop, None, loop=False)
        if not self.animating:
            self._set_new_image(self.image_idle)

    def draw(self, screen):
        screen.blit(self.image, (self.middle, 0), self.rect)
