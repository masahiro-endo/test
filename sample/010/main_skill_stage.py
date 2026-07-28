import pyxel

# ===== スキルデータ =====
skills = [
    {"name": "Sword Slash", "category": "physical", "subcategory": "slash", "power": 15, "mp_cost": 0},
    {"name": "Piercing Thrust", "category": "physical", "subcategory": "pierce", "power": 18, "mp_cost": 0},
    {"name": "Fireball", "category": "spell", "subcategory": "fire", "power": 25, "mp_cost": 5},
    {"name": "Ice Lance", "category": "spell", "subcategory": "ice", "power": 20, "mp_cost": 4},
    {"name": "Heal", "category": "spell", "subcategory": "heal", "power": -20, "mp_cost": 6},
]

# 大分類と小分類の定義
categories = ["physical", "spell"]
subcategories = {
    "physical": ["slash", "pierce"],
    "spell": ["fire", "ice", "heal"]
}

# ===== ゲームクラス =====
class Game:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel RPG Battle Demo")
        self.state = "category"  # category → subcategory → skill → result
        self.selected_category = 0
        self.selected_subcategory = 0
        self.selected_skill = 0
        self.message = ""
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.state == "category":
            self.handle_menu(categories, "subcategory", "selected_category")

        elif self.state == "subcategory":
            current_cat = categories[self.selected_category]
            self.handle_menu(subcategories[current_cat], "skill", "selected_subcategory")

        elif self.state == "skill":
            current_cat = categories[self.selected_category]
            current_subcat = subcategories[current_cat][self.selected_subcategory]
            skill_list = [s for s in skills if s["subcategory"] == current_subcat]
            self.handle_menu(skill_list, "result", "selected_skill")

        elif self.state == "result":
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
                self.state = "category"
                self.message = ""

    def handle_menu(self, items, next_state, attr_name):
        # 上下キーで選択
        if pyxel.btnp(pyxel.KEY_DOWN):
            setattr(self, attr_name, (getattr(self, attr_name) + 1) % len(items))
        elif pyxel.btnp(pyxel.KEY_UP):
            setattr(self, attr_name, (getattr(self, attr_name) - 1) % len(items))

        # 決定キー
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            if next_state == "result":
                # 攻撃結果を作成
                current_cat = categories[self.selected_category]
                current_subcat = subcategories[current_cat][self.selected_subcategory]
                skill_list = [s for s in skills if s["subcategory"] == current_subcat]
                chosen_skill = skill_list[self.selected_skill]
                self.message = f"{chosen_skill['name']} を使った！ Power={chosen_skill['power']}"
            self.state = next_state

    def draw(self):
        pyxel.cls(0)
        pyxel.text(5, 5, "Pyxel RPG Battle Demo", 7)

        if self.state == "category":
            self.draw_menu(categories, self.selected_category, "大分類を選択")
        elif self.state == "subcategory":
            current_cat = categories[self.selected_category]
            self.draw_menu(subcategories[current_cat], self.selected_subcategory, "小分類を選択")
        elif self.state == "skill":
            current_cat = categories[self.selected_category]
            current_subcat = subcategories[current_cat][self.selected_subcategory]
            skill_list = [s["name"] for s in skills if s["subcategory"] == current_subcat]
            self.draw_menu(skill_list, self.selected_skill, "スキルを選択")
        elif self.state == "result":
            pyxel.text(10, 50, self.message, 10)
            pyxel.text(10, 70, "Enterで戻る", 8)

    def draw_menu(self, items, selected_index, title):
        pyxel.text(5, 20, title, 11)
        for i, item in enumerate(items):
            color = 10 if i == selected_index else 7
            pyxel.text(10, 40 + i * 10, f"> {item}", color)

# ===== 実行 =====
if __name__ == "__main__":
    Game()

    