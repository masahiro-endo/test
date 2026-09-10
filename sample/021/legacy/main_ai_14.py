
import pyxel as px
import random



WIDTH = 120
HEIGHT = 160







class Star2:
    def __init__(self):
        self.reset()

    def reset(self):
        # 星の初期位置（画面外左）
        self.x = random.uniform(-20, 0)
        self.y = random.uniform(0, px.height)
        # 初速（1.5〜3.0）
        self.vx = random.uniform(1.5, 3.0)
        self.target_speed = self.vx * 0.5  # 最終速度（50%）
        self.change_rate = random.uniform(0.01, 0.03)  # 減速率
        self.size = random.randint(1, 2)  # 星の大きさ
        self.color = random.choice([7, 10, 11])  # 白・黄・水色

    def update(self):
        # 徐々に減速
        if self.vx > self.target_speed:
            self.vx -= (self.vx - self.target_speed) * self.change_rate

        # 位置更新
        self.x += self.vx

        # 画面外に出たら再生成
        if self.x > px.width + 5:
            self.reset()

    def draw(self):
        px.circ(self.x, self.y, self.size, self.color)




class Star:
    SIZE = 1
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, WIDTH - Star.SIZE)
        self.y = random.randint(0, HEIGHT - Star.SIZE)
        self.speed = random.choice([0.5, 1, 1.5]) # 初速
        self.color = random.choice([5, 6, 7])

        self.vy = self.speed
        self.target_rate = 1   # 最終速度 現在速度に対する率
        self.target_vy = 0
        self.change_speed(self.target_rate)
        self.df_rate = 0.03 # 最終速度に至るまでの変化率

    def update(self):
        if px.frame_count % 200 == 0:
            self.change_speed(0 if self.target_rate == 1 else 1)

        df = (max(self.vy, self.target_vy) - min(self.vy, self.target_vy)) * self.df_rate
        self.vy += df if self.vy < self.target_vy else -df

        # 位置更新
        self.y += self.vy

        if self.is_offscreen():
            self.x = random.randint(0, WIDTH - Star.SIZE)
            self.y = -Star.SIZE

    def draw(self):
        px.pset(int(self.x), int(self.y), self.color)

    def is_offscreen(self):
        if (self.x < -Star.SIZE or self.x > WIDTH  + Star.SIZE or 
            self.y < -Star.SIZE or self.y > HEIGHT + Star.SIZE):
            return True
        return False

    def change_speed(self, rate):
        self.target_rate = rate
        self.target_vy = self.speed * (self.target_rate)



class App:
    def __init__(self):
        px.init(160, 120, title="Multiple Shooting Stars")
        self.stars = [Star() for _ in range(20)]  # 星20個
        px.run(self.update, self.draw)

    def update(self):
        for star in self.stars:
            star.update()

    def draw(self):
        px.cls(0)  # 背景黒
        for star in self.stars:
            star.draw()
        px.text(10, 10, str(self.stars[0].target_rate), px.COLOR_WHITE)


App()




