import pyxel
import heapq
import random

# キャラクタークラス
class Character:
    def __init__(self, name, hp, speed, is_player):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.speed = speed
        self.is_player = is_player

    def __lt__(self, other):
        return self.speed < other.speed

    def is_alive(self):
        return self.hp > 0

# 戦闘管理クラス
class Battle:
    def __init__(self):
        # 味方パーティ
        self.players = [
            Character("Hero", 30, 5, True),
            Character("Mage", 20, 4, True),
            Character("Cleric", 25, 3, True)
        ]
        # 敵パーティ
        self.enemies = [
            Character("SlimeA", 15, 2, False),
            Character("SlimeB", 18, 3, False),
            Character("SlimeC", 20, 4, False)
        ]

        self.log = []
        self.turn_queue = []
        self.state = "TURN_START"  # TURN_START, PLAYER_CMD, ENEMY_ACT, END
        self.selected_cmd = 0
        self.selected_target = 0
        self.current_actor = None
        self.fill_turn_queue()

    def fill_turn_queue(self):
        """行動順キューをスピード順で作成"""
        self.turn_queue.clear()
        for char in self.players + self.enemies:
            if char.is_alive():
                heapq.heappush(self.turn_queue, (-char.speed, char))

    def next_turn(self):
        """次の行動者を決定"""
        if not self.turn_queue:
            self.fill_turn_queue()
        _, self.current_actor = heapq.heappop(self.turn_queue)

        if not self.current_actor.is_alive():
            self.next_turn()
            return

        if self.current_actor.is_player:
            self.state = "PLAYER_CMD"
            self.selected_cmd = 0
            self.selected_target = 0
        else:
            self.state = "ENEMY_ACT"

    def player_action(self):
        """プレイヤーの行動実行"""
        if self.selected_cmd == 0:  # 攻撃
            target = self.get_alive_enemies()[self.selected_target]
            dmg = random.randint(4, 8)
            target.hp -= dmg
            self.log.append(f"{self.current_actor.name} attacks {target.name}! {dmg} dmg!")
        elif self.selected_cmd == 1:  # 回復
            heal = random.randint(5, 10)
            self.current_actor.hp = min(self.current_actor.max_hp, self.current_actor.hp + heal)
            self.log.append(f"{self.current_actor.name} heals {heal} HP!")

        self.end_action()

    def enemy_action(self):
        """敵の行動実行"""
        target = random.choice(self.get_alive_players())
        dmg = random.randint(2, 5)
        target.hp -= dmg
        self.log.append(f"{self.current_actor.name} bites {target.name}! {dmg} dmg!")
        self.end_action()

    def end_action(self):
        """行動終了処理"""
        if self.current_actor.is_alive():
            heapq.heappush(self.turn_queue, (-self.current_actor.speed, self.current_actor))
        if self.is_battle_over():
            self.state = "END"
        else:
            self.state = "TURN_START"

    def is_battle_over(self):
        return not self.get_alive_players() or not self.get_alive_enemies()

    def get_alive_players(self):
        return [p for p in self.players if p.is_alive()]

    def get_alive_enemies(self):
        return [e for e in self.enemies if e.is_alive()]

# Pyxelアプリ
class App:
    def __init__(self):
        pyxel.init(200, 150, title="Pyxel Party Battle")
        self.battle = Battle()
        self.frame_count = 0
        self.battle.next_turn()
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.battle.state == "TURN_START":
            self.battle.next_turn()

        elif self.battle.state == "PLAYER_CMD":
            if pyxel.btnp(pyxel.KEY_UP):
                self.battle.selected_cmd = (self.battle.selected_cmd - 1) % 2
            if pyxel.btnp(pyxel.KEY_DOWN):
                self.battle.selected_cmd = (self.battle.selected_cmd + 1) % 2
            if self.battle.selected_cmd == 0:  # 攻撃時はターゲット選択
                if pyxel.btnp(pyxel.KEY_LEFT):
                    self.battle.selected_target = (self.battle.selected_target - 1) % len(self.battle.get_alive_enemies())
                if pyxel.btnp(pyxel.KEY_RIGHT):
                    self.battle.selected_target = (self.battle.selected_target + 1) % len(self.battle.get_alive_enemies())
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.battle.player_action()

        elif self.battle.state == "ENEMY_ACT":
            if self.frame_count % 30 == 0:
                self.battle.enemy_action()

        self.frame_count += 1

    def draw(self):
        pyxel.cls(0)
        # 味方表示
        for i, p in enumerate(self.battle.players):
            color = 7 if p.is_alive() else 5
            pyxel.text(5, 5 + i * 10, f"{p.name} HP:{p.hp}/{p.max_hp}", color)

        # 敵表示
        for i, e in enumerate(self.battle.enemies):
            color = 8 if e.is_alive() else 5
            pyxel.text(120, 5 + i * 10, f"{e.name} HP:{e.hp}/{e.max_hp}", color)

        # ログ表示
        for i, log in enumerate(self.battle.log[-5:]):
            pyxel.text(5, 80 + i * 10, log, 7)

        # コマンド選択
        if self.battle.state == "PLAYER_CMD":
            cmds = ["Attack", "Heal"]
            for i, cmd in enumerate(cmds):
                color = 10 if i == self.battle.selected_cmd else 7
                pyxel.text(5, 120 + i * 10, cmd, color)

            # 攻撃時のターゲット表示
            if self.battle.selected_cmd == 0:
                alive_enemies = self.battle.get_alive_enemies()
                for i, e in enumerate(alive_enemies):
                    pass



App()