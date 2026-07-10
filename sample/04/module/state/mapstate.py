
from enum import Enum, auto

import appconfig as gbl
from module.UI import *
from module.actor import *
from module.state.basestate import *
from module.state.optionstate import *
from resource.mapevent import *







class MapStates(BaseContext):
    def __init__(self, parent):
        self.parent = parent
        self.table = {
            STATE.Field: MapState_Field(self),
            STATE.Shop: MapState_Shop(self),
            STATE.FieldMenu: MapState_FieldMenu(self),
            STATE.FieldSpell: MapState_FieldSpell(self),
        }
        self.changeState(STATE.Field)

    def update(self):
        self.currentState.update()
    def draw(self):
        self.currentState.draw()

    def Field(self):
        self.changeState(STATE.Field)
    def FieldMenu(self):
        self.changeState(STATE.FieldMenu)
    def FieldSpell(self):
        self.changeState(STATE.FieldSpell)
    def Shop(self):
        self.changeState(STATE.Shop)




class STATE(Enum):
    Field = auto()
    Shop = auto()
    FieldMenu = auto()
    FieldSpell = auto()




class MapState_Field(BaseState):
    def __init__(self, parent):
        self.state = STATE.Field
        self.map = parent
        self.cursor = None

    def enter(self):
        self.pt = gbl.player_party()

    def update(self):
        self.pt.update()

    def draw(self):
        pt = self.pt

        x, y = (pt.x * 16 + pt.dx, pt.y * 16 + pt.dy)
        # bltm(x, y, tilemap, u, v, w, h, [colkey])
        px.bltm(8, 0, pt.z, x - 48, y - 48, 112, 112)
        # 障害物（NPC含む）
        for key in gbl.map_resource().obstacles:
            # 扉開放や宝箱取得時点でフラグを保持し、
            # 以降は描画しない
            if not key in pt.flags:
                ob = gbl.map_resource().obstacles[key]
                ob.draw(x, y, pt.z)
        
        # イメージバンクimg(0-2) の (u, v) からサイズ (w, h) の領域を (x, y) にコピーする。
        # w、hそれぞれに負の値を設定すると水平、垂直方向に反転する。
        # colkeyに色を指定すると透明色として扱われる
        # マスク
        (u, v) = (64, 0)
        px.blt(0 , -8, 0, u, v,  64,  64, 1)
        px.blt(64, -8, 0, u, v, -64,  64, 1)
        px.blt(0 , 56, 0, u, v,  64, -64, 1)
        px.blt(64, 56, 0, u, v, -64, -64, 1)
        sz = TILE_SIZE
        # 主人公
        (u, v) = ((px.frame_count % 30) // 15 * sz, 2 * sz)
        # blt(x, y, imgbank, u, v, w, h, [colkey])
        px.blt(56, 48, 0, u, v, sz, sz, 1)
        # ステータス表示
        px.rect(0, 112, 128, 16, 0)
        t = f"HP{Meth.pad(pt[0].hp,3)} MP{Meth.pad(pt[0].mp,2)} {Meth.pad(pt.gold,4)}G"
        Meth.draw_text(0, 14, t)


# 選択肢機能を持つクラスは「親」が異なる
class MapState_FieldMenu(OptionState):
    def __init__(self, parent):
        self.state = STATE.FieldMenu
        self.map = parent
        self.cursor = None

    def enter(self):
        COMMAND_TREE = {
            'セーブ'  : [self.cmd_Save],
            'じゅもん': [self.map.FieldSpell],
            'とじる'  : [self.cmd_Close],
        }
        # sub_tree = self.update_sub_tree()
        # COMMAND_TREE["じゅもん"] = sub_tree
        super().__init__(COMMAND_TREE)

        self.show_menu()
        gbl.current_cursor = self

    def update(self):
        super().update()

    def draw(self):
        super().draw()


    def cmd_Save(self):
        Window.message(["セーブしました"])

    def cmd_Close(self):
        Window.close()
        self.map.Field()

    def show_menu(self):
        pt = gbl.player_party()
        Window.open(WIN.MENU, 0, 0, 16, 10, pt.field_status())
        Window.message([f"いま ちか{pt.z+1}かいに います"])



# 選択肢機能を持つクラスは「親」が異なる
class MapState_FieldSpell(OptionState):
    def __init__(self, parent):
        self.state = STATE.FieldSpell
        self.map = parent

    def enter(self):
        COMMAND_TREE = {
            'とじる'  : [self.cmd_Close],
        }
        sub_tree = self.update_spell_tree()
        sub_tree.update(**COMMAND_TREE)
        super().__init__(sub_tree)

        self.sub_tree = sub_tree
        self.show_menu()
        gbl.current_cursor = self

    def update(self):
        super().update()


    def draw(self):
        super().draw()

    def update_spell_tree(self):
        resr = SkillResources().spells
        sub_tree = {}
        for i, data in enumerate(resr):
            name, mp, place, desc = data
            if SKL.FLD in place:
                spl = Spell(*data)

                sub_tree[name] = [self.cmd_action, {'spl': spl }] 
        return sub_tree

    def cmd_Close(self):
        Window.close()
        self.map.Field()

    def cmd_action(self, *args, **kwargs):
        spl = kwargs['spl']

        if mp and mp <= pt.pl.mp and spl.on_menu:
            pt.pl.mp -= mp
            if spl_id == SPELL.RETURN:
                Window.close(self.cursor)
                self.map.Field()
                pt.use_return()
                return
            elif spl_id == SPELL.HEAL:
                pt.use_heal(mp)
                self.MENU_SPL()        


    def show_menu(self):
        pt = gbl.player_party()
        for key, data in self.sub_tree.items():
            func, kmarg = data
            spl = kmarg['spl']
            break

        t1 = f"げんざいのMP {pt[0].mp}" if SKL.FLD in spl.usable_place else "ここでは つかえない"
        t2 = [f"{Meth.spacing(spl.name,4)}    MP {Meth.pad(spl.cost, 2)}", spl.desc[0], spl.desc[1], t1]
        Window.open(WIN.MENU_SPL, 0, 0, 16, 10, t2)

        Window.message(["なにを つかいますか？"])





class MapState_Shop(BaseState):
    def __init__(self, parent):
        self.state = STATE.Shop
        self.map = parent
        self.cursor = None

    def enter(self):
        self.shop_show()

    def update(self):
        if self.cursor is None:
            return

        ret = self.cursor.update()
        if ret is None:
            return

        if ret == SHOP_SEL.Cancel:
            Window.close()
            self.map.Field()
        else:
            pt = gbl.player_party()
            _, _, cost = self.shop_get_item(ret)
            if cost == 0 or pt.gold < cost:
                return
            pt.gold -= cost
            if ret == SHOP_SEL.HP:
                pt.pl.mhp += 5
                pt.pl.hp = pt.pl.mhp
            elif ret == SHOP_SEL.MP:
                pt.pl.mmp += 2
                pt.pl.mp = self.pl.mmp
            elif ret == SHOP_SEL.STR:
                pt.pl.atk += 2
            elif ret == SHOP_SEL.AGI:
                pt.pl.spd += 2
            # px.play(3, 32)
            self.shop_show()

    def draw(self):
        pass


    # ショップ用ウィンドウ生成
    def shop_show(self):
        Window.message(["レベルアップするかい？", " HP MP ちから はやさ"])
        self.cursor = Cursor(CSR.SHOP, [1, 4, 7, 11], 14, SHOP_SEL.Cancel)

        pt = gbl.player_party()
        t1, t2, cost = self.shop_get_item(self.cursor.pos)
        if cost:
            t3 = f"{cost}Gで レベルアップ"
        else:
            t3 = "もう レベルアップできない"
        t4 = "# おかねが たりません" if cost > pt.gold else ""
        t = [f"{t1} → {t2}", t3, t4, f"  (げんざい {Meth.pad(pt.gold,4)}G)"]
        Window.open(WIN.SHOP, 0, 0, 16, 10, t)


    # ショップ用購入項目情報取得
    def shop_get_item(self, kind):
        pt = gbl.get_party()

        cost = 0
        t2 = "---"
        if kind == SHOP_SEL.HP:
            t1 = f"HP {Meth.pad(pt.pl.mhp,3)}"
            if pt.pl.mhp < 255:
                t2 = Meth.pad(pt.pl.mhp + 5, 3)
                cost = pt.pl.mhp * 2
        elif kind == SHOP_SEL.MP:
            t1 = f"MP  {Meth.pad(pt.pl.mmp,2)}"
            if pt.pl.mmp < 98:
                t2 = Meth.pad(pt.pl.mmp + 2, 3)
                cost = pt.pl.mmp * 5
        elif kind == SHOP_SEL.STR:
            t1 = f"ちから {Meth.pad(pt.pl.atk,2)}"
            if pt.pl.atk < 98:
                t2 = pad(pt.pl.atk + 2, 3)
                cost = pt.pl.atk * 5
        elif kind == SHOP_SEL.AGI:
            t1 = f"はやさ {Meth.pad(pt.pl.spd,2)}"
            if pt.pl.spd < 98:
                t2 = Meth.pad(pt.pl.spd + 2, 3)
                cost = pt.pl.spd * 5
        return t1, t2, cost



class MapState_FieldTalk(BaseState):
    def __init__(self, parent):
        self.state = STATE.FieldMenu
        self.map = parent
        self.cursor = None

    def enter(self):
        self.pt = gbl.player_party()
        self.showmsg()

    def update(self):
        ret = self.cursor.update()

        if ret == MENU_SEL.Save:
            # self.save_data()
            Window.message(["セーブしました"])
        elif ret == MENU_SEL.Spells:
            self.map.Spell()
        elif ret == MENU_SEL.Close:
            Window.close()
            self.map.Field()

    def draw(self):
        pass

    def showmsg(self):
        pt = self.pt
        Window.open(WIN.MENU, 0, 0, 16, 10, pt.status())
        Window.message([f"いま ちか{pt.z+1}かいに います", " セーブ じゅもん とじる"])
        self.cursor = Cursor(CSR.MENU, [1, 5, 10], 14, MENU_SEL.Cancel)