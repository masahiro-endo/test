import pyxel as px
from actor import *



class Map_Field():
    def __init__(self):
        (self.x, self.y, self.z) = (8, 21, 0)

    def update(self):
        gbl.get_party().update()

    def draw(self):
            pt = gbl.get_party()

            x, y = (self.x * 16 + pt.dx, self.y * 16 + pt.dy)
            px.bltm(8, 0, self.z, x - 48, y - 48, 112, 112)
            # 障害物（NPC含む）
            for key in get_resource().obstacles:
                if not key in pt.flags:
                    ob = get_resource().obstacles[key]
                    ob.draw(x, y, self.z)
            # マスク
            px.blt(0, -8, 0, 64, 0, 64, 64, 1)
            px.blt(64, -8, 0, 64, 0, -64, 64, 1)
            px.blt(0, 56, 0, 64, 0, 64, -64, 1)
            px.blt(64, 56, 0, 64, 0, -64, -64, 1)
            # 主人公
            (u, v) = ((px.frame_count % 30) // 15 * 16, 2 * 16)
            px.blt(56, 48, 0, u, v, 16, 16, 1)
            # ステータス表示
            px.rect(0, 112, 128, 16, 0)
            t = f"HP{pad(pt.pl.hp,3)} MP{pad(pt.pl.mp,2)} {pad(pt.gold,4)}G"
            draw_text(0, 14, t)

    @property
    def event(self):
        pt = gbl.get_party()
        
        x = self.x + pt.dx
        y = self.y + pt.dy
        tm = px.tilemaps[self.z].pget(x * 2, y * 2)
        if tm == (0, 2):
            return "-"  # 壁
        elif tm == (2, 2):
            return "@"  # 泉
        elif tm == (4, 0):
            return "<"  # 上り階段
        elif tm == (6, 0):
            return ">"  # 下り階段
        for key in get_resource().obstacles:
            ob = get_resource().obstacles[key]
            if not key in pt.flags and (ob.x, ob.y, ob.z) == (x, y, self.z):
                return key
        return ""


    # 移動（１ステップ）開始
    def move_start(self):
        # 移動先のイベントを取得
        evt = self.event
        pt = gbl.get_party()

        if not evt or evt in (">", "<"):  # 階段
            pt.dx *= pt.spd
            pt.dy *= pt.spd
            pt.moving = True
            Window.close()  # ウィンドウが表示されていれば閉じる
            return
        pt.dx, pt.dy = (0, 0)
        if evt == "@":  # 泉
            px.play(3, 32)
            self.message(["かいふくの いずみだ", "HP MP かいふく！"])
            pt.pl.hp = pt.pl.mhp
            pt.pl.mp = pt.pl.mmp
        if evt in get_resource().obstacles:
            ob = get_resource().obstacles[evt]
            # 扉
            if ob.kind == 0:
                if self.keys:
                    px.play(3, 33)
                    self.message(["カギを あけた"])
                    pt.flags.append(evt)
                    pt.keys -= 1
                    self.wait = True
                else:
                    self.message(["カギを もっていない"])
            # 宝箱
            elif ob.kind == 1:
                t = ["たからばこだ！"]
                if ob.val:
                    t.append(f"{ob.val}G てにいれた")
                    self.add_gold(ob.val)
                else:
                    t.append(f"カギを てにいれた")
                    self.keys += 1
                self.message(t)
                pt.flags.append(evt)
                px.play(3, 35)
            # NPC
            if evt == "0-1" and "4-3" in pt.flags:
                self.message(["ぜひ Pyxelを", "マスターしてくれ"])
            elif evt == "0-3":
                self.message(["パワーアップするかい？", " HP MP ちから はやさ"])
                self.cur = Cursor("shop", [1, 4, 7, 11], 14, -1)
                self.shop_show()
            elif evt == "1-2" and not "sp1" in self.flags:
                self.message(["リターンの じゅもんを", "さずけよう"])
                self.flags.append("sp1")
            elif evt == "2-5" and not "sp2" in self.flags:
                self.message(["じゅんびは よいか？", " はい  いいえ"])
                self.cur = Cursor("boss1", [1, 5], 14, 1)
            elif evt == "3-1" and not "sp3" in self.flags:
                self.message(["おれと たたかうのか？", " はい  いいえ"])
                self.cur = Cursor("boss2", [1, 5], 14, 1)
            elif evt == "4-3":
                self.message(["この ひほうが ほしいか？", " はい  いいえ"])
                self.cur = Cursor("boss3", [1, 5], 14, 1)
            # 会話のみ
            elif evt in get_resource().talks:
                Window.message(get_resource().talks[evt])

    # 移動（１ステップ）終了
    def move_end(self):
        pt = gbl.get_party()

        self.y += pt.dy // 16
        self.x += pt.dx // 16
        pt.dy = 0
        pt.dx = 0
        pt.moving = False
        if self.event in ("<", ">"):  # 階段
            self.z += 1 if self.event == ">" else -1
            # エンディング判定
            if self.z == 0 and "4-3" in pt.flags and not "end" in pt.flags:
                s = self.frames // 30
                m = s // 60
                s %= 60
                self.message(["ゲームクリア！", f"タイム：{m}ふん{s}びょう"])
                pt.flags.append("end")
            else:
                self.message([f"ちか{self.z+1}かい"])
            # self.field_bgm()
            # px.play(3, 34)
            self.wait = True
            return
        if (self.x + self.y) % 2 == 0:
            pt.pl.hp = min(pt.pl.hp + 1, pt.pl.mhp)
        # 地下1階、ひほう取得〜エンディングは敵がでない
        if self.z == 0 or ("4-3" in pt.flags and not "end" in pt.flags):
            return
        self.enc += 1
        if self.enc > 12 and px.rndi(0, 7) == 0:
            self.enc = 0
            ms_id = self.z - (1 if px.rndi(0, 3) < 3 else 0)
            self.battle_start(ms_id)

