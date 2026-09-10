
import math
import random
import uuid

from constant import * 







class BaseEnemy():
    def __init__(self, size):
        self.size = size
        self.score = 100
        self._hp = 1
        self.id = uuid.uuid4()
        self.item = None

    @property
    def hp(self):
        return self._hp
    @hp.setter
    def hp(self, new_value):
        if new_value != self._hp:
            self._hp = new_value

    def hit(self, bullet):
        if self.is_owner(bullet):
            return False
        return math.hypot(self.x - bullet.x, self.y - bullet.y) < self.size - 1

    def is_owner(self, bullet):
        return self.id == bullet.owner_id

    def is_offscreen(self):
        if (self.x < -self.size or self.x > WIDTH  + self.size or
            self.y < -self.size or self.y > HEIGHT + self.size):
            return True
        return False

    def is_dead(self):
        return self._hp <= 0

    def sudden_death(self):
        self._hp = 0
        del self

