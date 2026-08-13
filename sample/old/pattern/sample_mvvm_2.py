import pyxel
import random

# -------------------------
# Model: ゲーム状態
# -------------------------
class GameModel:
    def __init__(self, enemy_count=3):
        self.player_x = 60
        self.player_y = 100
        self.coin_x = random.randint(0, 120)
        self.coin_y = random.randint(0, 100)
        self.enemies = [
            {"x": random.randint(0, 120), "y": random.randint(0, 100)}
            for _ in range(enemy_count)
        ]
        self.enemy_speed = 1
        self.score = 0
        self.game_over = False
        self.frame_count = 0  # 難易度上昇用カウンタ

    def move_player(self, dx, dy):
        self.player_x = max(0, min(120, self.player_x + dx))
        self.player_y = max(0, min(120, self.player_y + dy))

    def move_enemies_towards_player(self):
        for enemy in self.enemies:
            if enemy["x"] < self.player_x:
                enemy["x"] += self.enemy_speed
            elif enemy["x"] > self.player_x:
                enemy["x"] -= self.enemy_speed

            if enemy["y"] < self.player_y:
                enemy["y"] += self.enemy_speed
            elif enemy["y"] > self.player_y:
                enemy["y"] -= self.enemy_speed

    def check_coin_collision(self):
        if abs(self.player_x - self.coin_x) < 8 and abs(self.player_y - self.coin_y) < 8:
            self.score += 1
            self.coin_x = random.randint(0, 120)
            self.coin_y = random.randint(0, 100)

    def check_enemy_collision(self):
        for enemy in self.enemies:
            if abs(self.player_x - enemy["x"]) < 8 and abs(self.player_y - enemy["y"]) < 8:
                self.score -= 1
                if self.score < 0:
                    self.game_over = True
                else:
                    # 敵をランダム位置にリスポーン
                    enemy["x"] = random.randint(0, 120)
                    enemy["y"] = random.randint(0, 100)

    def increase_difficulty(self):
        self.frame_count += 1
        # 10秒ごとに敵の速度を上げる（Pyxelは1秒=30フレーム）
        if self.frame_count % (30 * 10) == 0:
            self.enemy_speed += 0.5


# -------------------------
# ViewModel: ロジック制御
# -------------------------
class GameViewModel:
    def __init__(self, model: GameModel):
        self.model = model

    def update(self):
        if self.model.game_over:
            return

        # 入力処理
        if pyxel.btn(pyxel.KEY_LEFT):
            self.model.move_player(-2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.model.move_player(2, 0)
        if pyxel.btn(pyxel.KEY_UP):
            self.model.move_player(0, -2)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.model.move_player(0, 2)

        # AI処理
        self.model.move_enemies_towards_player()

        # 衝突判定
        self.model.check_coin_collision()
        self.model.check_enemy_collision()

        # 難易度上昇
        self.model.increase_difficulty()

    # View 用データ取得
    def get_player_pos(self):
        return self.model.player_x, self.model.player_y

    def get_coin_pos(self):
        return self.model.coin_x, self.model.coin_y

    def get_enemies(self):
        return self.model.enemies

    def get_score(self):
        return self.model.score

    def is_game_over(self):
        return self.model.game_over


# -------------------------
# View: 描画とイベントループ
# -------------------------
class GameView:
    def __init__(self, view_model: GameViewModel):
        self.vm = view_model
        pyxel.init(128, 128, title="Pyxel MVVM + Multiple Enemies + Difficulty")
        pyxel.run(self.update, self.draw)

    def update(self):
        self.vm.update()

    def draw(self):
        pyxel.cls(0)

        if self.vm.is_game_over():
            pyxel.text(40, 60, "GAME OVER", 8)
            pyxel.text(35, 75, f"Final Score: {self.vm.get_score()}", 7)
            return

        # プレイヤー
        px, py = self.vm.get_player_pos()
        pyxel.rect(px, py, 8, 8, 11)  # 青

        # コイン
        cx, cy = self.vm.get_coin_pos()
        pyxel.circ(cx, cy, 3, 10)  # 黄

        # 敵
        for enemy in self.vm.get_enemies():
            pyxel.rect(enemy["x"], enemy["y"], 8, 8, 8)  # 赤

        # スコア表示
        pyxel.text(5, 5, f"Score: {self.vm.get_score()}", 7)


# -------------------------
# 実行
# -------------------------
if __name__ == "__main__":
    model = GameModel(enemy_count=5)  # 敵5体
    vm = GameViewModel(model)
    GameView(vm)
