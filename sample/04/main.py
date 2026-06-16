import pyxel as px
import json
import copy
from UI import *
from actor import *
import appconfig as gbl
from scenestate import *



IS_WEB = True

try:
    from js import window
except:
    IS_WEB = False





# Pyxel
class App:
    def __init__(self):
        # global BDF
        config = gbl.get_settings()

        px.init(
            128, 128, title="Pyxel Tiny DRPG", quit_key=px.KEY_NONE, display_scale=2
        )
        px.load("assets.pyxres")
        config.BDF = px.Font("k8x12S.bdf")  # フォントファイル
        config.party = Party()

        config.screen = SceneStates()
        self.screen = gbl.get_screen()
        self.screen.Main()

        self.cur = None
        self.wait = False
        self.bgm = None
        # self.welcome_show()
        self.scene = ""
        px.run(self.update, self.draw)

    # pyxel updateメイン
    def update(self):
        # ゲーム時間カウント
        # if self.scene != "welcome":
        #     self.frames += 1
        self.screen.update()
        btn = get_btn_state()

        # 十字キー押しっぱなし防止
        if self.wait and (btn["u"] or btn["d"] or btn["r"] or btn["l"]):
            return
        self.wait = False
        # カーソルがある場合カーソル処理を優先
        if self.cur:
            cur = self.cur
            ret = cur.update(btn)
            # ショップの場合は左右キーを押したときにウィンドウを再表示
            if btn["r"] or btn["l"]:
                if cur.key == "spells":
                    self.menu_spells()
                elif cur.key == "shop":
                    self.shop_show()
                elif cur.key == "bt_spells":
                    self.battle_spells()
            # ABボタンを押してなければ終了
            if ret is None:
                return
            # 起動画面の選択肢
            if cur.key == "welcome":
                # self.cur = None
                # # ret == 1（Continue)の場合、すでにセーブデータをロードしているので何もしない
                # if ret == 0:  # New
                #     self.new_game()
                # elif ret == 2:  # Exit
                #     px.quit()
                # self.field_start()
                pass
            # メニューの選択肢
            elif cur.key == "menu":
                # self.cur = None
                # if ret == 0:  # セーブ
                #     self.save_data()
                # elif ret == 1:  # じゅもん
                #     self.menu_spells()
                #     return
                # elif ret == 2:
                #     Window.close()
                #     self.welcome_show()
                #     return
                # self.field_start()
                # if ret == 0:
                #     self.message(["セーブしました"])
                pass
            # メニュー呪文の選択肢
            elif cur.key == "spells":
                # if ret >= 0:
                #     spl_id = self.available_spells()[ret]
                #     spl = self.spells[spl_id]
                #     mp = spl.get_mp(self.pl)
                #     if mp and mp <= self.pl.mp and spl.on_menu:
                #         self.pl.mp -= mp
                #         if spl_id == SPELL_RETURN:
                #             Window.close()
                #             self.cur = None
                #             self.go_start_location()
                #             px.play(3, 36)
                #             return
                #         elif spl_id == SPELL_HEAL:
                #             self.use_heal(mp)
                #             self.menu_spells()
                # else:
                #     Window.close()
                #     self.menu_show()
                #     self.cur.pos = 1
                pass
            # ショップの選択肢
            elif cur.key == "shop":
                # if ret < 0:
                #     Window.close()
                #     self.cur = None
                # else:
                #     _, _, cost = self.shop_get_item(ret)
                #     if cost == 0 or self.gold < cost:
                #         return
                #     self.gold -= cost
                #     if ret == 0:
                #         self.pl.mhp += 5
                #         self.pl.hp = self.pl.mhp
                #     elif ret == 1:
                #         self.pl.mmp += 2
                #         self.pl.mp = self.pl.mmp
                #     elif ret == 2:
                #         self.pl.atk += 2
                #     elif ret == 3:
                #         self.pl.spd += 2
                #     px.play(3, 32)
                #     self.shop_show()
                pass
            # イベント（ボス戦1）の選択肢
            elif cur.key == "boss1":
                self.cur = None
                Window.close()
                if ret == 0:
                    self.battle_start(5, "boss1")
            # イベント（ボス戦2）の選択肢
            elif cur.key == "boss2":
                self.cur = None
                Window.close()
                if ret == 0:
                    self.battle_start(6, "boss2")
            # イベント（ボス戦3）の選択肢
            elif cur.key == "boss3":
                self.cur = None
                Window.close()
                if ret == 0:
                    self.battle_start(7, "boss3")
            # バトルのコマンド選択
            elif cur.key == "bt_command":
                self.cur = None
                if ret == 0:
                    self.battle_attack()
                elif ret == 1:
                    self.battle_spells()
                elif ret == 2:
                    self.battle_run()
            # バトル呪文の選択肢
            elif cur.key == "bt_spells":
                if ret >= 0:
                    spl_id = self.available_spells(True)[ret]
                    spl = self.spells[spl_id]
                    mp = spl.get_mp(self.pl)
                    if mp and mp <= self.pl.mp:
                        self.pl.mp -= mp
                        self.cur = None
                        self.bt_msg = [f"{self.pl.name}は {spl.name}をとなえた"]
                        if spl_id == SPELL_FIRE:
                            dmg = 0 if self.ms.resist else px.rndi(24, 30)
                            self.battle_damage(self.ms, dmg)
                        elif spl_id == SPELL_HEAL:
                            ret = self.use_heal(mp)
                            self.bt_msg += [f"{ret}HP かいふくした"]
                        elif spl_id == SPELL_BURST:
                            dmg = 0
                            for _ in range(mp):
                                dmg += px.rndi(8, 12)
                            self.battle_damage(self.ms, dmg)
                        self.battle_show()
                else:
                    self.battle_command()
                    self.cur.pos = 1
        # フィールド用update処理
        elif self.scene == "field":
            # 操作受付
            # if not self.moving:
            #     self.dy = btn["d"] - btn["u"]
            #     self.dx = btn["r"] - btn["l"] if not self.dy else 0
            #     if self.dy or self.dx:
            #         self.move_start()
            #     elif btn["a"]:
            #         Window.close()
            #     elif btn["b"]:  # メニュー呼び出し
            #         self.menu_show()
            #         self.scene = "menu"
            # # 移動実処理
            # else:
            #     self.dy += self.spd * ((self.dy > 0) - (self.dy < 0))
            #     self.dx += self.spd * ((self.dx > 0) - (self.dx < 0))
            #     # 移動終了
            #     if (self.dy % 16, self.dx % 16) == (0, 0):
            #         self.move_end()
            pass
        # バトル用update処理（ターン送り）
        elif self.scene == "battle":
            if btn["a"] or btn["b"]:
                # どちらかが倒れた
                if self.pl.hp <= 0:
                    self.game_over()
                elif self.ms.hp <= 0:
                    self.battle_win()
                # 攻守が入れ替わる
                elif self.bt_my_turn:
                    self.battle_monster_action()
                else:
                    self.battle_command()
        # ゲームオーバー
        elif self.scene == "gameover":
            if btn["a"] or btn["b"]:
                self.gold = self.gold // 2
                self.go_start_location()
                self.pl.hp = 1
                self.field_start()

    # pyxel drawメイン
    def draw(self):
        px.cls(0)
        self.screen.draw()

        # 起動画面用draw処理
        if self.scene == "welcome":
            pass
            # draw_text(3, 2, "Pyxel Tiny")
            # draw_text(6, 4, "DRPG")
        # フィールド用draw処理
        elif self.scene == "field":
            # # マップ
            # x, y = (self.x * 16 + self.dx, self.y * 16 + self.dy)
            # px.bltm(8, 0, self.z, x - 48, y - 48, 112, 112)
            # # 障害物（NPC含む）
            # for key in self.obstacles:
            #     if not key in self.flags:
            #         ob = self.obstacles[key]
            #         ob.draw(x, y, self.z)
            # # マスク
            # px.blt(0, -8, 0, 64, 0, 64, 64, 1)
            # px.blt(64, -8, 0, 64, 0, -64, 64, 1)
            # px.blt(0, 56, 0, 64, 0, 64, -64, 1)
            # px.blt(64, 56, 0, 64, 0, -64, -64, 1)
            # # 主人公
            # (u, v) = ((px.frame_count % 30) // 15 * 16, 2 * 16)
            # px.blt(56, 48, 0, u, v, 16, 16, 1)
            # # ステータス表示
            # px.rect(0, 112, 128, 16, 0)
            # t = f"HP{pad(self.pl.hp,3)} MP{pad(self.pl.mp,2)} {pad(self.gold,4)}G"
            # draw_text(0, 14, t)
            pass
        # バトル用draw処理（モンスターグラフィック表示）
        elif self.scene == "battle":
            u = self.ms.img % 4 * 64
            v = self.ms.img // 4 * 64 + 64
            px.blt(0, 0, 0, u, v, 64, 64)
        # ウィンドウ
        # for key in Window.all:
        #     Window.all[key].draw()
        # カーソル
        # if self.cur:
        #     self.cur.draw()

    ### システム関連 ###




    # # ニューゲーム
    # def new_game(self):
    #     self.pl = Actor("あなた", 30, 6, 12, 12)
    #     self.go_start_location()
    #     self.gold = 0
    #     self.keys = 0  # カギの数
    #     self.flags = []  # フラグ（宝箱、扉などの判定用）
    #     self.enc = 0  # エンカウント
    #     self.frames = 0


    ### 汎用関数 ####

    # ゲームオーバー
    def game_over(self):
        Window.close()
        self.message([f"{self.pl.name}は", "いしきを うしなった"])
        self.scene = "gameover"

    # スタート位置にもどる
    # def go_start_location(self):
    #     self.scene = "field"
    #     (self.x, self.y, self.z) = (8, 21, 0)
    #     self.play_bgm(2)

    # お金入手
    def add_gold(self, gold):
        self.gold = min(self.gold + gold, 9999)

    # ヒール発動
    def use_heal(self, mp):
        hp = min(self.pl.hp + mp * 5, self.pl.mhp)
        ret = hp - self.pl.hp
        self.pl.hp += ret
        return ret

    # # 現在使える呪文
    # def available_spells(self, on_battle=False):
    #     ret = [SPELL_FIRE]  # ファイアは最初から
    #     if not on_battle and "sp1" in self.flags:
    #         ret.append(SPELL_RETURN)
    #     if "sp2" in self.flags:
    #         ret.append(SPELL_HEAL)
    #     if "sp3" in self.flags:
    #         ret.append(SPELL_BURST)
    #     return ret

    ### フィールド関連 ###

    # 移動先のイベントorタイル状態取得
    # @property
    # def event(self):
    #     x = self.x + self.dx
    #     y = self.y + self.dy
    #     tm = px.tilemaps[self.z].pget(x * 2, y * 2)
    #     if tm == (0, 2):
    #         return "-"  # 壁
    #     elif tm == (2, 2):
    #         return "@"  # 泉
    #     elif tm == (4, 0):
    #         return "<"  # 上り階段
    #     elif tm == (6, 0):
    #         return ">"  # 下り階段
    #     for key in self.obstacles:
    #         ob = self.obstacles[key]
    #         if not key in self.flags and (ob.x, ob.y, ob.z) == (x, y, self.z):
    #             return key
    #     return ""

    # フィールド処理開始
    # def field_start(self):
    #     Window.close()
    #     self.scene = "field"
    #     # self.field_bgm()
    #     self.moving = False
    #     (self.dx, self.dy, self.spd) = (0, 0, 4)

    # フィールドBGM
    # def field_bgm(self):
    #    self.play_bgm(1 if self.z > 0 else 2)


    # ショップ用ウィンドウ生成
    def shop_show(self):
        t1, t2, cost = self.shop_get_item(self.cur.pos)
        if cost:
            t3 = f"{cost}Gで パワーアップ"
        else:
            t3 = "もう パワーアップできない"
        t4 = "# おかねが たりません" if cost > self.gold else ""
        t = [f"{t1} → {t2}", t3, t4, f"  (げんざい {pad(self.gold,4)}G)"]
        Window.open("shop", 0, 0, 16, 10, t)

    # ショップ用購入項目情報取得
    def shop_get_item(self, kind):
        pl = self.pl
        cost = 0
        t2 = "---"
        if kind == 0:
            t1 = f"HP {pad(pl.mhp,3)}"
            if pl.mhp < 255:
                t2 = pad(pl.mhp + 5, 3)
                cost = pl.mhp * 2
        elif kind == 1:
            t1 = f"MP  {pad(pl.mmp,2)}"
            if pl.mmp < 98:
                t2 = pad(pl.mmp + 2, 3)
                cost = pl.mmp * 5
        elif kind == 2:
            t1 = f"ちから {pad(pl.atk,2)}"
            if pl.atk < 98:
                t2 = pad(pl.atk + 2, 3)
                cost = pl.atk * 5
        elif kind == 3:
            t1 = f"はやさ {pad(pl.spd,2)}"
            if pl.spd < 98:
                t2 = pad(pl.spd + 2, 3)
                cost = pl.spd * 5
        return t1, t2, cost

    ### メニュー関連 ###

    # # メニュー用ウィンドウ生成
    # def menu_show(self):
    #     pl = self.pl
    #     t = [
    #         f"HP {pad(pl.hp,3)}/{pad(pl.mhp,3)}",
    #         f"MP  {pad(pl.mp,2)}/ {pad(pl.mmp,2)}",
    #         f"ちから {pad(pl.atk,2)}  はやさ {pad(pl.spd,2)}",
    #         f" {pad(self.gold,4)}G  カギ {pad(self.keys,2)}こ",
    #     ]
    #     Window.open("menu_stat", 0, 0, 16, 10, t)
    #     Window.message([f"いま ちか{self.z+1}かいに います", " セーブ じゅもん リセット"])
    #     self.cur = Cursor("menu", [1, 5, 10], 14, -1)

    # # メニュー用呪文リスト
    # def menu_spells(self):
    #     spells = self.available_spells()
    #     pos = self.cur.pos if self.cur else 0
    #     spl = self.spells[spells[pos]]
    #     t1 = f"げんざいのMP {self.pl.mp}" if spl.on_menu else "ここでは つかえない"
    #     mp = spl.get_mp(self.pl)
    #     t2 = [f"{spacing(spl.name,4)}    MP {pad(mp,2)}", spl.desc[0], spl.desc[1], t1]
    #     Window.open("menu_spells", 0, 0, 16, 10, t2)
    #     t3 = " "
    #     list_x = []
    #     for spl_id in spells:
    #         list_x.append(len(t3))
    #         # 文字数省略のため最初の２文字だけ表示
    #         t3 += self.spells[spl_id].name[0:2] + " "
    #     self.message(["なにを つかいますか？", t3])
    #     if not self.cur:
    #         self.cur = Cursor("spells", list_x, 14, -1)

    ### バトル関連 ###

    # バトル開始
    def battle_start(self, ms_id, evt=None):
        data = self.monsters[ms_id]
        self.scene = "battle"
        self.ms = Actor(*data)
        self.bt_evt = evt
        self.bt_my_turn = True
        msg_pre = [f"{self.ms.name}が あらわれた"]
        # 先行判定
        if self.pl.spd * px.rndf(1.0, 2.0) >= self.ms.spd * px.rndf(1.0, 2.0):
            self.battle_command(msg_pre)
        else:
            self.bt_msg = msg_pre + ["てきに せんてをとられた"]
            self.battle_show()
        self.wait = True
        self.play_bgm(0)

    # バトル用ウィンドウ生成
    def battle_show(self):
        pl = self.pl
        t = [pl.name, f"HP {pad(pl.hp,3)}", f"MP  {pad(pl.mp,2)}"]
        Window.open("bt_stat", 8, 0, 16, 8, t)
        Window.open("bt_msg", 0, 8, 16, 16, self.bt_msg)

    # コマンド選択
    def battle_command(self, msg_pre=[]):
        self.bt_my_turn = True
        self.bt_msg = msg_pre + ["どうする？", " たたかう じゅもん にげる"]
        y = 8 + len(self.bt_msg) * 2
        self.cur = Cursor("bt_command", [1, 6, 11], y)
        self.battle_show()

    # バトル用呪文リスト
    def battle_spells(self):
        spells = self.available_spells(True)
        pos = self.cur.pos if self.cur else 0
        mp = self.spells[spells[pos]].get_mp(self.pl)
        t1 = " "
        list_x = []
        for spl_id in spells:
            list_x.append(len(t1))
            t1 += self.spells[spl_id].name + " "
        self.bt_msg = ["なにを つかいますか？", t1, f" MP {pad(mp,2)}"]
        if not self.cur:
            self.cur = Cursor("bt_spells", list_x, 12, -1)
        self.battle_show()

    # 攻撃
    def battle_attack(self, msg_pre=[]):
        # 攻撃する人、される人を設定
        if self.bt_my_turn:
            attacker = self.pl
            target = self.ms
        else:
            attacker = self.ms
            target = self.pl
        self.bt_msg = msg_pre + [f"{attacker.name}の こうげき"]
        hit_rate = max(min(attacker.spd / target.spd, 1.5), 0.25)
        hit_rate = min(hit_rate - px.rndf(0.0, 1.0), 1.0)
        if hit_rate > 0.0:
            dmg = int(attacker.atk * (1 + hit_rate) / 2 + 0.99)
            self.battle_damage(target, dmg)
        else:  # 回避された
            self.bt_msg += [f"{target.name}は みをかわした"]
        self.battle_show()

    # ダメージ処理
    def battle_damage(self, target, dmg):
        self.bt_msg += [f"{target.name}に {dmg}ダメージ"]
        target.hp = max(target.hp - dmg, 0)
        if self.bt_my_turn and target.hp <= 0:
            self.bt_msg += [f"{target.name}を たおした"]

    # 逃げる
    def battle_run(self):
        rate = 1.0 + self.pl.spd / self.ms.spd
        if rate > px.rndf(0.0, 2.0):
            self.field_start()
            self.message(["にげのびた..."])
        else:
            self.bt_msg = ["にげられなかった"]
            self.battle_show()

    # 敵の行動
    def battle_monster_action(self, msg_pre=[]):
        self.bt_my_turn = False
        # MPがある敵はファイアを使う
        spl = self.spells[SPELL_FIRE]
        if self.ms.mp >= spl.mp and px.rndi(0, 1) == 0:
            self.ms.mp -= spl.mp
            self.bt_msg = [f"{self.ms.name}は{spl.name}をとなえた"]
            dmg = px.rndi(12, 18)  # 敵のファイアは少し弱め
            self.battle_damage(self.pl, dmg)
            self.battle_show()
        else:
            self.battle_attack(msg_pre)

    # 勝利
    def battle_win(self):
        self.field_start()
        t = ["たたかいに かった"]
        if self.bt_evt == "boss1":
            t += [f"「{self.spells[SPELL_HEAL].name}」を おぼえた"]
            self.flags.append("sp2")
        elif self.bt_evt == "boss2":
            t += [f"「{self.spells[SPELL_BURST].name}」を おぼえた"]
            self.flags.append("sp3")
        elif self.bt_evt == "boss3":
            self.flags.append("4-3")
            t = ["ひほうを てにいれた！"]
        else:
            gold = int(self.ms.gold * px.rndf(0.7, 1.0) + 0.99)
            self.add_gold(gold)
            t += [f"{gold}G てにいれた"]
        self.message(t)


App()
