import pyxel

# Game constants
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
PLAYER_SPEED = 2
SCROLL_SPEED = 1

class Game:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel Scroll Action")
        pyxel.load("")  # No external resource file; using draw functions

        # Player position
        self.player_x = 20
        self.player_y = SCREEN_HEIGHT // 2
        self.player_w = 8
        self.player_h = 8

        # World scroll offset
        self.scroll_x = 0

        # Obstacles (world coordinates)
        self.obstacles = [
            {"x": 100, "y": 80, "w": 8, "h": 8},
            {"x": 180, "y": 60, "w": 8, "h": 8},
            {"x": 260, "y": 90, "w": 8, "h": 8},
        ]

        pyxel.run(self.update, self.draw)

    def update(self):
        # Player movement
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y = max(0, self.player_y - PLAYER_SPEED)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_y = min(SCREEN_HEIGHT - self.player_h, self.player_y + PLAYER_SPEED)

        # Scroll world
        self.scroll_x += SCROLL_SPEED

        # Collision detection
        for obs in self.obstacles:
            obs_screen_x = obs["x"] - self.scroll_x
            if (self.player_x < obs_screen_x + obs["w"] and
                self.player_x + self.player_w > obs_screen_x and
                self.player_y < obs["y"] + obs["h"] and
                self.player_y + self.player_h > obs["y"]):
                print("Collision!")
                pyxel.quit()

    def draw(self):
        pyxel.cls(0)

        # Draw player
        pyxel.rect(self.player_x, self.player_y, self.player_w, self.player_h, 11)

        # Draw obstacles (adjusted for scroll)
        for obs in self.obstacles:
            obs_screen_x = obs["x"] - self.scroll_x
            if -obs["w"] < obs_screen_x < SCREEN_WIDTH:
                pyxel.rect(obs_screen_x, obs["y"], obs["w"], obs["h"], 8)

        # Draw ground
        pyxel.line(0, SCREEN_HEIGHT - 1, SCREEN_WIDTH, SCREEN_HEIGHT - 1, 3)

        # HUD
        pyxel.text(5, 5, f"Scroll: {self.scroll_x}", 7)


if __name__ == "__main__":
    Game()


    