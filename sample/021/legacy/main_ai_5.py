
import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Enemy Path Array Movement")
        
        # 経路（敵が通る座標のリスト）
        self.path = [
            (20, 20),
            (140, 20),
            (140, 100),
            (20, 100),
            (20, 20)  # 最初に戻る
        ]
        
        self.enemy_x, self.enemy_y = self.path[0]
        self.target_index = 1  # 次の目的地インデックス
        self.speed = 1.0       # 移動速度（px/frame）
        
        pyxel.run(self.update, self.draw)

    def update(self):
        target_x, target_y = self.path[self.target_index]
        
        # X方向移動
        if abs(self.enemy_x - target_x) > self.speed:
            self.enemy_x += self.speed if target_x > self.enemy_x else -self.speed
        else:
            self.enemy_x = target_x
        
        # Y方向移動
        if abs(self.enemy_y - target_y) > self.speed:
            self.enemy_y += self.speed if target_y > self.enemy_y else -self.speed
        else:
            self.enemy_y = target_y
        
        # 目的地に到達したら次のポイントへ
        if (self.enemy_x, self.enemy_y) == (target_x, target_y):
            self.target_index = (self.target_index + 1) % len(self.path)

    def draw(self):
        pyxel.cls(0)
        
        # 経路表示（デバッグ用）
        for px, py in self.path:
            pyxel.circ(px, py, 2, 5)
        
        # 敵キャラ
        pyxel.circ(self.enemy_x, self.enemy_y, 4, 8)
        
        pyxel.text(5, 5, "Path Array Movement", 7)

if __name__ == "__main__":
    App()


