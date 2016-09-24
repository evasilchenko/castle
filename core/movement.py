


class MovementManager(object):
    def __init__(self):
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.y_position = 0
        self.x_position = 0
        self.drop_speed = 1

    def _move_right(self):
        self.x_position += 1

    def _move_left(self):
        if self.x_position > 0:
            self.x_position -= 1

    def _move_up(self):
        if self.y_position < 150:
            self.y_position += 1
        else:
            self.moving_up = False
            self.moving_down = True

    def _move_down(self):
        if self.y_position > 0:
            self.y_position -= 1
        else:
            self.moving_down = False
            self.drop_speed = 1

    def _handle_movement(self):
        if self.moving_right:
            self._move_right()

        if self.moving_left:
            self._move_left()

        if self.moving_up:
            self._move_up()

        if self.moving_down:
            self._move_down()

    def stop_moving_left(self):
        self.moving_left = False

    def start_moving_left(self):
        self.moving_right = False
        self.moving_left = True

    def stop_moving_right(self):
        self.moving_right = False

    def start_moving_right(self):
        self.moving_right = True
        self.moving_left = False

    def stop_moving_up(self):
        self.drop_speed = 1
        self.moving_up = False
        self.moving_down = True

    def start_moving_up(self):
        if not self.moving_down:
            self.moving_up = True