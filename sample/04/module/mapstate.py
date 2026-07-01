import pyxel
from enum import Enum, auto
from basestate import *
from UI import *
from actor import *
import appconfig as gbl
from resource.mapevent import *



pt = gbl.player_party



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
        sz = TileEvents.TILE_SIZE
        # 主人公
        (u, v) = ((px.frame_count % 30) // 15 * sz, 2 * sz)
        # blt(x, y, imgbank, u, v, w, h, [colkey])
        px.blt(56, 48, 0, u, v, sz, sz, 1)
        # ステータス表示
        px.rect(0, 112, 128, 16, 0)
        t = f"HP{Meth.pad(pt[0].hp,3)} MP{Meth.pad(pt[0].mp,2)} {Meth.pad(pt.gold,4)}G"
        Meth.draw_text(0, 14, t)



class MapState_FieldMenu(BaseState):
    def __init__(self, parent):
        self.state = STATE.FieldMenu
        self.map = parent
        self.cursor = None

    def enter(self):
        self.pt = gbl.player_party()
        self.showmenu()

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

    # メニュー用ウィンドウ生成
    def showmenu(self):
        pt = self.pt
        Window.open(WINDOW_KEY.MENU, 0, 0, 16, 10, pt.status())
        Window.message([f"いま ちか{pt.z+1}かいに います", " セーブ じゅもん とじる"])
        self.cursor = Cursor(CURSOR_KEY.MENU, [1, 5, 10], 14, MENU_SEL.Cancel)




class MapState_FieldSpell(BaseState):
    def __init__(self, parent):
        self.state = STATE.FieldSpell
        self.map = parent
        self.cursor = None

    # メニュー用呪文リスト
    def menu_spells(self):
        pt = gbl.get_party()

        spells = pt.available_spells()
        pos = self.cursor.pos if self.cursor else 0
        spl = gbl.resource().spells[spells[pos]]
        t1 = f"げんざいのMP {pt.pl.mp}" if spl.on_menu else "ここでは つかえない"
        mp = spl.get_mp(pt.pl)
        t2 = [f"{Meth.spacing(spl.name,4)}    MP {Meth.pad(mp,2)}", spl.desc[0], spl.desc[1], t1]
        Window.open(WINDOW_KEY.MENU_SPELLS, 0, 0, 16, 10, t2)
        t3 = " "
        list_x = []
        for spl_id in spells:
            list_x.append(len(t3))
            # 文字数省略のため最初の２文字だけ表示
            t3 += gbl.resource().spells[spl_id].name[0:2] + " "
        Window.message(["なにを つかいますか？", t3])
        self.cursor = Cursor(CURSOR_KEY.SPELLS, list_x, 14, SPELL_SEL.Cancel)

    def enter(self):
        self.menu_spells()

    def update(self):
        if self.cursor is None:
            return

        ret = self.cursor.update()
        if ret is None:
            return

        if ret == SPELL_SEL.Cancel:
            Window.close()
            self.map.Field()
        else:
            pt = gbl.get_party()
            spl_id = pt.available_spells()[ret]
            spl = gbl.resource().spells[spl_id]
            mp = spl.get_mp(pt.pl)
            if mp and mp <= pt.pl.mp and spl.on_menu:
                pt.pl.mp -= mp
                if spl_id == SPELL.RETURN:
                    Window.close(self.cursor)
                    self.map.Field()
                    pt.use_return()
                    return
                elif spl_id == SPELL.HEAL:
                    pt.use_heal(mp)
                    self.menu_spells()        

    def draw(self):
        pass


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
        self.cursor = Cursor(CURSOR_KEY.SHOP, [1, 4, 7, 11], 14, SHOP_SEL.Cancel)

        pt = gbl.get_party()
        t1, t2, cost = self.shop_get_item(self.cursor.pos)
        if cost:
            t3 = f"{cost}Gで レベルアップ"
        else:
            t3 = "もう レベルアップできない"
        t4 = "# おかねが たりません" if cost > pt.gold else ""
        t = [f"{t1} → {t2}", t3, t4, f"  (げんざい {Meth.pad(pt.gold,4)}G)"]
        Window.open(WINDOW_KEY.SHOP, 0, 0, 16, 10, t)


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


