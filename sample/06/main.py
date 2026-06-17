import heapq
import random
from prettytable import PrettyTable
from colorama import Fore, Style, init



# Windowsでも色が出るように初期化
init(autoreset=True)

class Character:
    def __init__(self, name, hp, attack, speed):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.speed = speed
        self.status = {"stun": 0, "poison": 0}

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        self.hp = max(self.hp - dmg, 0)

    def apply_status_effects(self):
        """ターン開始時に状態異常を処理"""
        log = []
        if self.status["poison"] > 0:
            poison_dmg = 3
            self.take_damage(poison_dmg)
            log.append(Fore.MAGENTA + f"{self.name} は毒で {poison_dmg} ダメージ！")
            self.status["poison"] -= 1

        if self.status["stun"] > 0:
            self.status["stun"] -= 1
            log.append(Fore.MAGENTA + f"{self.name} はスタンで行動不能！")
            return True, log
        return False, log

    def status_str(self):
        """状態異常を文字列化"""
        effects = []
        if self.status["stun"] > 0:
            effects.append(f"スタン({self.status['stun']})")
        if self.status["poison"] > 0:
            effects.append(f"毒({self.status['poison']})")
        return ", ".join(effects) if effects else "-"

    def __repr__(self):
        return f"{self.name}(HP:{self.hp}, SPD:{self.speed})"


def print_battle_status(turn, characters):
    """現在の戦闘状況を表形式で表示"""
    table = PrettyTable()
    table.field_names = ["キャラ", "HP", "SPD", "状態異常"]
    for c in characters:
        table.add_row([c.name, c.hp, c.speed, c.status_str()])
    print(Fore.CYAN + f"\n=== ターン {turn} 状況 ===")
    print(table)


def battle_with_colors(characters):
    queue = []
    for c in characters:
        heapq.heappush(queue, (0, c))

    turn_count = 1

    while True:
        # 勝敗判定
        if not any(c.is_alive() for c in characters if c.name != "Enemy"):
            print(Fore.YELLOW + "\n=== 敵の勝利！ ===")
            break
        if not any(c.is_alive() for c in characters if c.name == "Enemy"):
            print(Fore.YELLOW + "\n=== プレイヤーの勝利！ ===")
            break

        # 状況表示
        print_battle_status(turn_count, characters)

        # 次に行動するキャラ
        turn_time, actor = heapq.heappop(queue)
        if not actor.is_alive():
            continue

        print(Fore.WHITE + f"[{turn_time:03}] {actor.name} のターン")

        # 状態異常処理
        stunned, status_logs = actor.apply_status_effects()
        for log in status_logs:
            print("  >>", log)

        if stunned:
            next_turn_time = turn_time + max(1, 10 - actor.speed)
            heapq.heappush(queue, (next_turn_time, actor))
            turn_count += 1
            continue

        # 行動選択
        action_type = random.choice(["attack", "slow", "haste", "stun", "poison"])
        targets = [c for c in characters if c.is_alive() and c != actor]
        if not targets:
            continue
        target = random.choice(targets)

        if action_type == "attack":
            dmg = random.randint(actor.attack - 2, actor.attack + 2)
            target.take_damage(dmg)
            print(Fore.RED + f"  >> {actor.name} が {target.name} に {dmg} ダメージ！")

        elif action_type == "slow":
            delay = 5
            print(Fore.MAGENTA + f"  >> {actor.name} が {target.name} にスロー！ 行動遅延 +{delay}")
            heapq.heappush(queue, (turn_time + delay, target))

        elif action_type == "haste":
            accel = -3
            print(Fore.GREEN + f"  >> {actor.name} が {target.name} にヘイスト！ 行動加速 {accel}")
            heapq.heappush(queue, (max(0, turn_time + accel), target))

        elif action_type == "stun":
            stun_turns = 1
            target.status["stun"] = stun_turns
            print(Fore.MAGENTA + f"  >> {actor.name} が {target.name} をスタン！ {stun_turns}ターン行動不能")

        elif action_type == "poison":
            poison_turns = 3
            target.status["poison"] = poison_turns
            print(Fore.MAGENTA + f"  >> {actor.name} が {target.name} に毒！ {poison_turns}ターン継続ダメージ")

        # 次の行動時間
        next_turn_time = turn_time + max(1, 10 - actor.speed)
        heapq.heappush(queue, (next_turn_time, actor))
        turn_count += 1


# キャラクター作成
player1 = Character("Hero", 30, 8, 7)
player2 = Character("Mage", 20, 10, 5)
enemy = Character("Enemy", 40, 6, 6)

# 戦闘開始
battle_with_colors([player1, player2, enemy])

