import pyxel
import random





# 味方キャラ
party = [
    {"name": "Hero", "hp": 30, "atk": 8, "def": 3},
    {"name": "Mage", "hp": 20, "atk": 10, "def": 2},
    {"name": "Warrior", "hp": 40, "atk": 6, "def": 5},
]

# 敵キャラ
enemies = [
    {"name": "Slime", "hp": 15, "atk": 4, "def": 1},
    {"name": "Goblin", "hp": 20, "atk": 5, "def": 2},
]

ACTIONS = ["Attack", "Defend", "Heal"]






class App:
    def __init__(self):
        pyxel.init(200, 150, title="Pyxel RPG Battle")
        self.reset_battle()
        pyxel.run(self.update, self.draw)

    def reset_battle(self):
        self.turn_index = 0
        self.selected_action = 0
        self.actions_dict = {}  # {キャラ名: {"action": str, "target": dict}}
        self.phase = "input"
        self.log = []
        self.exec_index = 0
        self.battle_over = False

    def update(self):
        if self.battle_over:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.reset_battle()
            return

        if self.phase == "input":
            self.update_input_phase()
        elif self.phase == "enemy_ai":
            self.enemy_ai_phase()
        elif self.phase == "execute":
            self.update_execute_phase()

    def update_input_phase(self):
        # 上下キーで行動選択
        if pyxel.btnp(pyxel.KEY_UP):
            self.selected_action = (self.selected_action - 1) % len(ACTIONS)
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.selected_action = (self.selected_action + 1) % len(ACTIONS)

        # Enterキーで決定
        if pyxel.btnp(pyxel.KEY_RETURN):
            char = party[self.turn_index]
            target = None
            if ACTIONS[self.selected_action] == "Attack":
                target = random.choice([e for e in enemies if e["hp"] > 0])
            elif ACTIONS[self.selected_action] == "Heal":
                target = char  # 自分を回復

            self.actions_dict[char["name"]] = {
                "action": ACTIONS[self.selected_action],
                "target": target
            }
            self.turn_index += 1
            self.selected_action = 0

            # 全員分入力が終わったら敵AIへ
            if self.turn_index >= len(party):
                self.phase = "enemy_ai"

    def enemy_ai_phase(self):
        # 敵の行動を決定
        for enemy in enemies:
            if enemy["hp"] <= 0:
                continue
            action = "Attack"
            target = random.choice([p for p in party if p["hp"] > 0])
            self.actions_dict[enemy["name"]] = {
                "action": action,
                "target": target
            }
        self.phase = "execute"
        self.exec_index = 0

    def update_execute_phase(self):
        all_chars = party + enemies
        if self.exec_index < len(all_chars):
            char = all_chars[self.exec_index]
            if char["hp"] > 0:
                act = self.actions_dict.get(char["name"])
                if act:
                    self.perform_action(char, act)
            self.exec_index += 1
        else:
            # 戦闘終了判定
            if all(e["hp"] <= 0 for e in enemies):
                self.log.append("You win!")
                self.battle_over = True
            elif all(p["hp"] <= 0 for p in party):
                self.log.append("You lose...")
                self.battle_over = True
            else:
                self.reset_battle()

    def perform_action(self, actor, act):
        action = act["action"]
        target = act["target"]

        if action == "Attack" and target and target["hp"] > 0:
            dmg = max(1, actor["atk"] - target["def"] + random.randint(-1, 2))
            target["hp"] = max(0, target["hp"] - dmg)
            self.log.append(f"{actor['name']} attacks {target['name']} for {dmg} dmg!")
        elif action == "Defend":
            self.log.append(f"{actor['name']} defends!")
        elif action == "Heal" and target:
            heal = random.randint(5, 10)
            target["hp"] += heal
            self.log.append(f"{actor['name']} heals {target['name']} for {heal} HP!")

    def draw(self):
        pyxel.cls(0)
        # 味方表示
        pyxel.text(5, 5, "Party:", 11)
        for i, p in enumerate(party):
            pyxel.text(10, 15 + i * 10, f"{p['name']} HP:{p['hp']}", 7)

        # 敵表示
        pyxel.text(120, 5, "Enemies:", 8)
        for i, e in enumerate(enemies):
            pyxel.text(125, 15 + i * 10, f"{e['name']} HP:{e['hp']}", 7)

        # ログ表示
        for i, line in enumerate(self.log[-6:]):
            pyxel.text(5, 80 + i * 10, line, 7)

        if self.battle_over:
            pyxel.text(60, 130, "Press Enter to restart", 10)
            return

        if self.phase == "input":
            char_name = party[self.turn_index]["name"]
            pyxel.text(5, 60, f"{char_name}'s turn", 14)
            for i, action in enumerate(ACTIONS):
                color = 10 if i == self.selected_action else 7
                pyxel.text(10, 95 + i * 10, action, color)
        elif self.phase == "execute":
            pyxel.text(5, 60, "Executing actions...", 14)

# 実行
App()


