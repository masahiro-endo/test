
import pyxel
import math
import random

WIDTH = 160
HEIGHT = 120

class Star:
    """背景の星"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, WIDTH - 1)
        self.y = random.randint(0, HEIGHT - 1)
        self.speed = random.choice([0.5, 1, 1.5])
        self.color = random.choice([5, 6, 7])

    def update(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = WIDTH
            self.y = random.randint(0, HEIGHT - 1)
            self.speed = random.choice([0.5, 1, 1.5])
            self.color = random.choice([5, 6, 7])

    def draw(self):
        pyxel.pset(int(self.x), int(self.y), self.color)


class Terrain:
    """上下の壁や障害物をスクロールさせる"""
    def __init__(self):
        self.segments = []
        self.generate_initial()

    def generate_initial(self):
        # 初期地形を生成
        for x in range(WIDTH // 8 + 2):
            self.segments.append(self.random_segment())

    def random_segment(self):
        # 上下の壁の高さをランダム生成
        top_height = random.randint(0, 20)
        bottom_height = random.randint(0, 20)
        return (top_height, bottom_height)

    def update(self):
        # 左にスクロール
        if pyxel.frame_count % 8 == 0:  # スクロール速度
            self.segments.pop(0)
            self.segments.append(self.random_segment())

    def draw(self):
        for i, (top, bottom) in enumerate(self.segments):
            x = i * 8
            if top > 0:
                pyxel.rect(x, 0, 8, top, 3)  # 上の壁
            if bottom > 0:
                pyxel.rect(x, HEIGHT - bottom, 8, bottom, 3)  # 下の壁

    def check_collision(self, px, py, pw, ph):
        """プレイヤーと地形の衝突判定"""
        for i, (top, bottom) in enumerate(self.segments):
            x = i * 8
            if x < px + pw and x + 8 > px:
                if py < top or py + ph > HEIGHT - bottom:
                    return True
        return False


class Enemy:
    def __init__(self, x, y, speed, amplitude, frequency, phase=0):
        self.x = x
        self.y = y
        self.base_y = y
        self.speed = speed
        self.amplitude = amplitude
        self.frequency = frequency
        self.t = phase

    def update(self):
        self.x -= self.speed
        self.t += 1
        self.y = self.base_y + math.sin(self.t * self.frequency) * self.amplitude

    def draw(self):
        pyxel.rect(self.x, self.y, 8, 8, 8)

    def is_offscreen(self):
        return self.x < -8


class Player:
    def __init__(self):
        self.x = 20
        self.y = HEIGHT // 2
        self.speed = 2
        self.bullets = []
        self.alive = True

    def update(self):
        if not self.alive:
            return
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= self.speed
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.speed
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.bullets.append([self.x + 8, self.y + 3])

        for b in self.bullets:
            b[0] += 3
        self.bullets = [b for b in self.bullets if b[0] < WIDTH]

    def draw(self):
        if self.alive:
            pyxel.rect(self.x, self.y, 8, 8, 11)
        for b in self.bullets:
            pyxel.rect(b[0], b[1], 2, 2, 7)


class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="Gradius-like Stage with Terrain")
        self.player = Player()
        self.enemies = []
        self.stars = [Star() for _ in range(40)]
        self.terrain = Terrain()
        self.score = 0
        pyxel.run(self.update, self.draw)

    def spawn_enemy_wave(self):
        base_y = random.randint(20, HEIGHT - 40)
        amp = random.randint(5, 15)
        freq = random.uniform(0.05, 0.12)
        spacing = 16
        for i in range(5):
            e = Enemy(
                WIDTH + i * spacing,
                base_y,
                1.5,
                amp,
                freq,
                phase=i * 10
            )
            self.enemies.append(e)

    def update(self):
        for s in self.stars:
            s.update()

        self.terrain.update()
        self.player.update()

        if pyxel.frame_count % 300 == 0:
            self.spawn_enemy_wave()

        for e in self.enemies:
            e.update()

        # 弾と敵の衝突
        for b in self.player.bullets[:]:
            for e in self.enemies[:]:
                if (e.x < b[0] < e.x + 8) and (e.y < b[1] < e.y + 8):
                    self.score += 100
                    self.enemies.remove(e)
                    self.player.bullets.remove(b)
                    break

        self.enemies = [e for e in self.enemies if not e.is_offscreen()]

        # 地形との衝突
        if self.terrain.check_collision(self.player.x, self.player.y, 8, 8):
            self.player.alive = False

    def draw(self):
        pyxel.cls(0)
        for s in self.stars:
            s.draw()
        self.terrain.draw()
        self.player.draw()
        for e in self.enemies:
            e.draw()
        pyxel.text(5, 5, f"SCORE: {self.score}", 7)
        if not self.player.alive:
            pyxel.text(WIDTH // 2 - 20, HEIGHT // 2, "GAME OVER", 8)


if __name__ == "__main__":
    App()



    