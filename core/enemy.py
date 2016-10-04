from pygame.sprite import LayeredUpdates

from core.character import Character, CharacterManager


class EnemyManager(CharacterManager):
    def __init__(self, *args, **kwargs):
        super(EnemyManager, self).__init__(*args, **kwargs)
        self.enemies = []
        self.active_enemies = LayeredUpdates()

    def _spawn(self):
        self.active_enemies.add(self.enemies[0].copy)

    def add_enemies(self, enemies):
        self.enemies.append(enemies)


class Enemy(Character):
    def __init__(self, *args, **kwargs):
        super(Enemy, self).__init__(*args, **kwargs)
        self.is_boss = kwargs.pop('boss', False)

    def _die(self):
        self.kill()

    def take_damage(self, damage=1):
        self.health -= damage

        if self.health <= 0:
            self._die()

    def attack(self):
        pass
