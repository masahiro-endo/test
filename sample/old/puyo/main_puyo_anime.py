
import pyxel
import random

# Game constants
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 120
PUYO_SIZE = 8
GRAVITY = 0.5
BOUNCE_DAMPING = 0.3
NUM_PUYOS = 5

class Puyo:
    def __init__(self):
        self.reset()

    def reset(self):
        # Random color (Pyxel palette index 2–15)
        self.color = random.randint(2, 15)
        self.x = random.randint(0, SCREEN_WIDTH - PUYO_SIZE)
        self.y = -PUYO_SIZE
        self.vy = 0

    def update(self):
        self.vy += GRAVITY
        self.y += self.vy

        # Bounce on floor
        if self.y + PUYO_SIZE >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - PUYO_SIZE
            self.vy = -self.vy * BOUNCE_DAMPING

            # If bounce is too small, reset puyo
            if abs(self.vy) < 0.5:
                self.reset()

    def draw(self):
        pyxel.circ(self.x + PUYO_SIZE // 2, self.y + PUYO_SIZE // 2, PUYO_SIZE // 2, self.color)


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Puyo Puyo Animation")
        pyxel.cls(0)
        self.puyos = [Puyo() for _ in range(NUM_PUYOS)]
        pyxel.run(self.update, self.draw)

    def update(self):
        for puyo in self.puyos:
            puyo.update()

    def draw(self):
        pyxel.cls(0)
        for puyo in self.puyos:
            puyo.draw()


if __name__ == "__main__":
    App()

