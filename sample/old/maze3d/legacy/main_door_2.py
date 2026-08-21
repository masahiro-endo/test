
import pyxel
import math

# Constants
SCREEN_W = 160
SCREEN_H = 120
DOOR_W = 32
DOOR_H = 64

class App:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="3D Maze Door (No Raycast)")
        # pyxel.load("")  # No external resource file

        # Door state
        self.door_open_progress = 0.0  # 0 = closed, 1 = fully open
        self.door_speed = 0.02
        self.door_opening = True

        # Maze wall colors
        self.wall_color = 8
        self.floor_color = 3
        self.ceiling_color = 1

        pyxel.run(self.update, self.draw)

    def update(self):
        # Toggle door animation with SPACE
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.door_opening = not self.door_opening

        # Animate door
        if self.door_opening:
            self.door_open_progress = min(1.0, self.door_open_progress + self.door_speed)
        else:
            self.door_open_progress = max(0.0, self.door_open_progress - self.door_speed)

    def draw(self):
        pyxel.cls(0)

        # Draw ceiling
        pyxel.rect(0, 0, SCREEN_W, SCREEN_H // 2, self.ceiling_color)
        # Draw floor
        pyxel.rect(0, SCREEN_H // 2, SCREEN_W, SCREEN_H // 2, self.floor_color)

        # Draw maze walls (simple perspective lines)
        self.draw_maze_walls()

        # Draw door sprite (scaled rectangle)
        self.draw_door()

        # Instructions
        pyxel.text(5, 5, "SPACE: Toggle Door", 7)

    def draw_maze_walls(self):
        # Fake perspective lines
        for i in range(5):
            depth = i + 1
            scale = 1 / depth
            wall_w = SCREEN_W * scale
            wall_h = SCREEN_H * scale
            x = (SCREEN_W - wall_w) / 2
            y = (SCREEN_H - wall_h) / 2
            pyxel.rectb(int(x), int(y), int(wall_w), int(wall_h), self.wall_color)

    def draw_door(self):
        # Door position and scaling based on open progress
        scale = 1.0 - self.door_open_progress
        door_w = DOOR_W * (1.5 - scale)  # Slight zoom as it opens
        door_h = DOOR_H * (1.5 - scale)
        x = SCREEN_W / 2 - door_w / 2
        y = SCREEN_H / 2 - door_h / 2

        # Draw left and right panels moving apart
        gap = self.door_open_progress * 20
        pyxel.rect(int(x - gap), int(y), int(door_w / 2), int(door_h), 9)  # Left panel
        pyxel.rect(int(x + door_w / 2 + gap), int(y), int(door_w / 2), int(door_h), 9)  # Right panel


if __name__ == "__main__":
    App()
