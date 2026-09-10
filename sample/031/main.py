
import pyxel
import random

# Board settings
BOARD_SIZE = 10  # 10 squares per side (total 40 squares)
TILE_SIZE = 16   # pixels per square
WINDOW_SIZE = BOARD_SIZE * TILE_SIZE

class MonopolyGame:
    def __init__(self):
        pyxel.init(WINDOW_SIZE, WINDOW_SIZE, title="Pyxel Monopoly Demo")
        self.player_pos = 0  # position index (0-39)
        self.dice_roll = 0
        self.is_moving = False
        self.steps_remaining = 0
        self.turn_message = "Press SPACE to roll dice"
        pyxel.run(self.update, self.draw)

    def roll_dice(self):
        # Roll two dice (1-6 each)
        return random.randint(1, 6) + random.randint(1, 6)

    def update(self):
        # Roll dice when SPACE is pressed and not moving
        if not self.is_moving and pyxel.btnp(pyxel.KEY_SPACE):
            self.dice_roll = self.roll_dice()
            self.steps_remaining = self.dice_roll
            self.is_moving = True
            self.turn_message = f"Rolled {self.dice_roll}!"

        # Move player step-by-step
        if self.is_moving:
            if self.steps_remaining > 0:
                self.player_pos = (self.player_pos + 1) % 40
                self.steps_remaining -= 1
            else:
                self.is_moving = False
                self.turn_message = "Press SPACE to roll dice"

    def draw(self):
        pyxel.cls(0)
        self.draw_board()
        self.draw_player()
        pyxel.text(5, 5, self.turn_message, 7)

    def draw_board(self):
        # Draw a simple square loop
        for i in range(40):
            x, y = self.get_tile_coords(i)
            pyxel.rectb(x, y, TILE_SIZE, TILE_SIZE, 7)

    def draw_player(self):
        x, y = self.get_tile_coords(self.player_pos)
        pyxel.circ(x + TILE_SIZE // 2, y + TILE_SIZE // 2, 4, 8)

    def get_tile_coords(self, index):
        # Convert board index (0-39) to x,y coordinates
        if index < 10:  # top row
            return index * TILE_SIZE, 0
        elif index < 20:  # right column
            return (BOARD_SIZE - 1) * TILE_SIZE, (index - 10) * TILE_SIZE
        elif index < 30:  # bottom row
            return (BOARD_SIZE - 1 - (index - 20)) * TILE_SIZE, (BOARD_SIZE - 1) * TILE_SIZE
        else:  # left column
            return 0, (BOARD_SIZE - 1 - (index - 30)) * TILE_SIZE

if __name__ == "__main__":
    MonopolyGame()


    