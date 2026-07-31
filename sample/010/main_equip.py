
import pyxel as px

# 装備データ
EQUIP_ITEMS = {
    "sword": {"name": "鉄の剣", "atk": 5, "def": 0},
    "shield": {"name": "木の盾", "atk": 0, "def": 3},
    "armor": {"name": "革の鎧", "atk": 0, "def": 2},
    "axe": {"name": "戦斧", "atk": 8, "def": -1},
}

# 装備スロットの順序
EQUIP_SLOTS = ["weapon", "shield", "armor"]

class Player:
    def __init__(self):
        self.name = "勇者"
        self.x = 40
        self.y = 40
        self.base_atk = 10
        self.base_def = 5
        self.equipment = {"weapon": "sword", "shield": "shield", "armor": None}

    def equip(self, slot, item_key):
        if slot in self.equipment and (item_key is None or item_key in EQUIP_ITEMS):
            self.equipment[slot] = item_key

    def total_atk(self):
        atk = self.base_atk
        for item_key in self.equipment.values():
            if item_key:
                atk += EQUIP_ITEMS[item_key]["atk"]
        return atk

    def total_def(self):
        defense = self.base_def
        for item_key in self.equipment.values():
            if item_key:
                defense += EQUIP_ITEMS[item_key]["def"]
        return defense


class App:
    def __init__(self):
        px.init(160, 120, title="px RPG 装備メニュー付き")
        self.player = Player()
        self.mode = "field"  # "field" or "menu"
        self.menu_index = 0  # 装備スロット選択位置
        self.item_index = 0  # 装備候補選択位置
        self.item_list = list(EQUIP_ITEMS.keys()) + [None]  # Noneは装備解除

        px.run(self.update, self.draw)

    def update(self):
        if self.mode == "field":
            self.update_field()
        elif self.mode == "menu":
            self.update_menu()

    def update_field(self):
        # 移動
        if px.btn(px.KEY_LEFT):
            self.player.x -= 1
        if px.btn(px.KEY_RIGHT):
            self.player.x += 1
        if px.btn(px.KEY_UP):
            self.player.y -= 1
        if px.btn(px.KEY_DOWN):
            self.player.y += 1

        # メニューを開く
        if px.btnp(px.KEY_E):
            self.mode = "menu"
            self.menu_index = 0
            self.item_index = 0

    def update_menu(self):
        # スロット選択
        if px.btnp(px.KEY_UP):
            self.menu_index = (self.menu_index - 1) % len(EQUIP_SLOTS)
        if px.btnp(px.KEY_DOWN):
            self.menu_index = (self.menu_index + 1) % len(EQUIP_SLOTS)

        # 装備候補選択
        if px.btnp(px.KEY_LEFT):
            self.item_index = (self.item_index - 1) % len(self.item_list)
        if px.btnp(px.KEY_RIGHT):
            self.item_index = (self.item_index + 1) % len(self.item_list)

        # 装備変更
        if px.btnp(px.KEY_RETURN) or px.btnp(px.KEY_SPACE):
            slot = EQUIP_SLOTS[self.menu_index]
            self.player.equip(slot, self.item_list[self.item_index])

        # メニューを閉じる
        if px.btnp(px.KEY_E):
            self.mode = "field"

    def draw(self):
        px.cls(0)
        if self.mode == "field":
            self.draw_field()
        elif self.mode == "menu":
            self.draw_menu()

    def draw_field(self):
        # 簡易マップ背景
        px.rect(0, 0, 160, 120, 3)
        # プレイヤー
        px.rect(self.player.x, self.player.y, 8, 8, 7)
        # ステータス表示
        px.text(5, 5, f"ATK:{self.player.total_atk()} DEF:{self.player.total_def()}", 7)
        px.text(5, 15, "[E] 装備メニュー", 6)

    def draw_menu(self):
        px.cls(1)
        px.text(5, 5, f"== 装備メニュー ==", 7)
        y = 20
        for i, slot in enumerate(EQUIP_SLOTS):
            prefix = ">" if i == self.menu_index else " "
            item_key = self.player.equipment[slot]
            item_name = EQUIP_ITEMS[item_key]["name"] if item_key else "なし"
            px.text(5, y, f"{prefix} {slot}: {item_name}", 7)
            y += 10

        # 候補表示
        px.text(5, 60, "候補:", 10)
        for i, key in enumerate(self.item_list):
            name = EQUIP_ITEMS[key]["name"] if key else "なし"
            color = 11 if i == self.item_index else 7
            px.text(5 + i * 40, 75, name, color)

        px.text(5, 100, "[↑↓]スロット [←→]候補 [Enter]装備 [E]戻る", 6)


if __name__ == "__main__":
    App()

