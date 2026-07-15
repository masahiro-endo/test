import pyxel
import random

class Character:
    def __init__(self, name, hp, speed, is_enemy=False):
        self.name = name
        self.hp = hp
        self.speed = speed
        self.is_enemy = is_enemy
        self.action = None

    def is_alive(self):
        return self.hp > 0

class Game:
    def __init__(self):
        pyxel.init(200, 160, title="Pyxel RPG Battle")
        self.phase = "input"  # input / target / execute / end
        self.all_chars = [
            Character("Hero", 30, 12, is_enemy=False),
            Character("Mage", 20, 8, is_enemy=False),
            Character("Warrior", 40, 10, is_enemy=False),
            Character("Goblin", 15, 9, is_enemy=True),
            Character("Orc", 25, 7, is_enemy=True)
        ]
        self.current_index = 0
        self.action_queue = []
        self.message = ""
        self.timer = 0

        # ターゲット選択用
        self.target_list = []
        self.target_index = 0
        self.pending_action_type = None
        self.pending_value = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.phase == "input":
            self.handle_input_phase()
        elif self.phase == "target":
            self.handle_target_phase()
        elif self.phase == "execute":
            self.handle_execute_phase()

    def handle_input_phase(self):
        current_char = self.all_chars[self.current_index]

        if not current_char.is_alive():
            self.next_character()
            return

        if current_char.is_enemy:
            # 敵AI: ランダム攻撃
            target = self.choose_random_target(is_enemy=False)
            if target:
                current_char.action = ("attack", target, 5)
            self.next_character()
        else:
            # プレイヤー入力
            if pyxel.btnp(pyxel.KEY_A):
                self.pending_action_type = "attack"
                self.pending_value = 5
                self.target_list = [c for c in self.all_chars if c.is_enemy and c.is_alive()]
                self.target_index = 0
                self.phase = "target"
            elif pyxel.btnp(pyxel.KEY_H):
                self.pending_action_type = "heal"
                self.pending_value = 3
                self.target_list = [c for c in self.all_chars if not c.is_enemy and c.is_alive()]
                self.target_index = 0
                self.phase = "target"

    def handle_target_phase(self):
        # カーソル移動
        if pyxel.btnp(pyxel.KEY_UP):
            self.target_index = (self.target_index - 1) % len(self.target_list)
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.target_index = (self.target_index + 1) % len(self.target_list)

        # 決定
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            current_char = self.all_chars[self.current_index]
            target = self.target_list[self.target_index]
            current_char.action = (self.pending_action_type, target, self.pending_value)
            self.phase = "input"
            self.next_character()

    def choose_random_target(self, is_enemy):
        candidates = [c for c in self.all_chars if c.is_enemy == is_enemy and c.is_alive()]
        return random.choice(candidates) if candidates else None

    def next_character(self):
        self.current_index += 1
        if self.current_index >= len(self.all_chars):
            # 行動順決定（素早さ降順）
            alive_chars = [c for c in self.all_chars if c.is_alive()]
            sorted_chars = sorted(alive_chars, key=lambda c: c.speed, reverse=True)
            self.action_queue = [(c, c.action) for c in sorted_chars]
            self.current_index = 0
            self.phase = "execute"
            self.timer = 0

    def handle_execute_phase(self):
        self.timer += 1
        if self.timer < 30:
            return
        self.timer = 0

        if self.action_queue:
            char, action = self.action_queue.pop(0)
            if not char.is_alive() or action is None:
                return

            act_type, target, value = action
            if act_type == "attack" and target and target.is_alive():
                target.hp -= value
                self.message = f"{char.name} attacks {target.name} for {value}!"
                if target.hp <= 0:
                    self.message += f" {target.name} is defeated!"
            elif act_type == "heal" and target and target.is_alive():
                target.hp += value
                self.message = f"{char.name} heals {target.name} for {value} HP!"
        else:
            # 勝敗判定
            if not any(c.is_alive() and not c.is_enemy for c in self.all_chars):
                self.message = "Enemies win!"
                self.phase = "end"
            elif not any(c.is_alive() and c.is_enemy for c in self.all_chars):
                self.message = "Players win!"
                self.phase = "end"
            else:
                self.phase = "input"
                self.message = ""

    def draw(self):
        pyxel.cls(0)
        pyxel.text(5, 5, f"Phase: {self.phase}", 7)

        # 味方表示
        pyxel.text(5, 20, "Allies:", 10)
        y = 35
        for c in [ch for ch in self.all_chars if not ch.is_enemy]:
            pyxel.text(5, y, f"{c.name} HP:{c.hp} SPD:{c.speed}", 7)
            y += 10

        # 敵表示
        pyxel.text(120, 20, "Enemies:", 8)
        y = 35
        for c in [ch for ch in self.all_chars if c.is_enemy]:
            pyxel.text(120, y, f"{c.name} HP:{c.hp} SPD:{c.speed}", 7)
            y += 10

        # 入力フェーズの表示
        if self.phase == "input":
            char = self.all_chars[self.current_index]
            if not char.is_enemy:
                pyxel.text(5, 130, f"{char.name}'s turn", 11)
                pyxel.text(5, 145, "[A] Attack  [H] Heal", 7)

        # ターゲット選択フェーズ
        if self.phase == "target":
            pyxel.text(5, 130, "Select Target:", 14)
            y = 145
            for i, t in enumerate(self
