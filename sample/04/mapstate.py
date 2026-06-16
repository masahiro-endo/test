import pyxel
from enum import Enum, auto
from basestate import *
from UI import *
from actor import *
import appconfig as gbl





class MapStates():
    def __init__(self, parent):
        self.parent = parent
        self.table = {
            STATE.Field: MapState_Field(self),
            STATE.Shop: MapState_Shop(self),
            STATE.Menu: MapState_Menu(self),
            STATE.Spell: MapState_Spell(self),
        }
        self._stack = []
        self.pushstate(STATE.Field)

    def update(self):
        curr = self.current()
        if curr: 
            curr.update()

    def draw(self):
        curr = self.current()
        if curr: 
            curr.draw()

    def Field(self):
        for map in reversed(self._stack):
            self.popstate()
        self.pushstate(STATE.Field)

    def Menu(self):
        self.pushstate(STATE.Menu)

    def Spell(self):
        self.pushstate(STATE.Spell)

    def Shop(self):
        self.pushstate(STATE.Shop)

    def pushstate(self, state):
        tbl = self.table[state]
        curr = self.current()
        if curr: 
            curr.exit()

        self._stack.append(tbl)
        curr = self.current()
        if curr: 
            curr.enter()

    @overload
    def popstate(self):
        curr = self.current()
        if curr: 
            curr.exit()

        self._stack.pop()
        curr = self.current()
        if curr: 
            curr.enter()

    @overload
    def popstate(self, state):
        curr = self.current()
        if curr: 
            curr.exit()

        for map in reversed(self._stack):
            if state == map.state:
                self._stack.remove(map)

        curr = self.current()
        if curr: 
            curr.enter()

    def current(self):
        if not self._stack:
            return None
        return self._stack[-1]



class STATE(Enum):
    Field = auto()
    Shop = auto()
    Menu = auto()
    Spell = auto()




class MapState_Field(BaseState):
    def __init__(self, parent):
        self.state = STATE.Field
        self.map = parent

    def update(self):
        gbl.get_party().update()

    def draw(self):
        pt = gbl.get_party()

        x, y = (pt.x * 16 + pt.dx, pt.y * 16 + pt.dy)
        px.bltm(8, 0, pt.z, x - 48, y - 48, 112, 112)
        # 障害物（NPC含む）
        for key in get_resource().obstacles:
            if not key in pt.flags:
                ob = get_resource().obstacles[key]
                ob.draw(x, y, pt.z)
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



class MapState_Menu(BaseState):
    def __init__(self, parent):
        self.state = STATE.Menu
        self.map = parent

    # メニュー用ウィンドウ生成
    def showmenu(self):
        pt = gbl.get_party()
        Window.open(WINDOW_KEY.MENU, 0, 0, 16, 10, pt.status())
        Window.message([f"いま ちか{pt.z+1}かいに います", " セーブ じゅもん とじる"])
        self.cur = Cursor("menu", [1, 5, 10], 14, -1)


    def enter(self):
        self.showmenu()

    def update(self):
        ret = self.cur.update()

        if ret == MENU_SEL.Save:
            # self.save_data()
            Window.message(["セーブしました"])
        elif ret == MENU_SEL.Spells:
            self.map.Spell()
        elif ret == MENU_SEL.Close:
            self.map.Field()

    def draw(self):
        for key in Window.all:
            Window.all[key].draw()
        self.cur.draw()



class MapState_Spell(BaseState):
    def __init__(self, parent):
        self.state = STATE.Spell
        self.map = parent
        self.cur = None

    # メニュー用呪文リスト
    def menu_spells(self):
        pt = gbl.get_party()

        spells = pt.available_spells()
        pos = self.cur.pos if self.cur else 0
        spl = get_resource().spells[spells[pos]]
        t1 = f"げんざいのMP {pt.pl.mp}" if spl.on_menu else "ここでは つかえない"
        mp = spl.get_mp(pt.pl)
        t2 = [f"{spacing(spl.name,4)}    MP {pad(mp,2)}", spl.desc[0], spl.desc[1], t1]
        Window.open(WINDOW_KEY.MENU_SPELLS, 0, 0, 16, 10, t2)
        t3 = " "
        list_x = []
        for spl_id in spells:
            list_x.append(len(t3))
            # 文字数省略のため最初の２文字だけ表示
            t3 += get_resource().spells[spl_id].name[0:2] + " "
        Window.message(["なにを つかいますか？", t3])
        self.cur = Cursor("spells", list_x, 14, -1)

    def enter(self):
        self.menu_spells()

    def update(self):
        ret = self.cur.update()

        if ret is None:
            return
        if ret >= 0:
            pt = gbl.get_party()
            spl_id = pt.available_spells()[ret]
            spl = get_resource().spells[spl_id]
            mp = spl.get_mp(pt.pl)
            if mp and mp <= pt.pl.mp and spl.on_menu:
                pt.pl.mp -= mp
                if spl_id == SPELL.CLOSE:
                    Window.close()
                    # self.cur = None
                    # self.go_start_location()
                    # px.play(3, 36)
                    return
                elif spl_id == SPELL.HEAL:
                    pt.use_heal(mp)
                    self.menu_spells()
        else:
            Window.pop(WINDOW_KEY.MENU_SPELLS)
            self.map.popstate()
        

    def draw(self):

        for key in Window.all:
            Window.all[key].draw()

        self.cur.draw()



class MapState_Shop(BaseState):
    def __init__(self, parent):
        self.state = STATE.Shop
        self.map = parent

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
        pt = gbl.get_party()

        cost = 0
        t2 = "---"
        if kind == 0:
            t1 = f"HP {pad(pt.pl.mhp,3)}"
            if pt.pl.mhp < 255:
                t2 = pad(pt.pl.mhp + 5, 3)
                cost = pt.pl.mhp * 2
        elif kind == 1:
            t1 = f"MP  {pad(pt.pl.mmp,2)}"
            if pt.pl.mmp < 98:
                t2 = pad(pt.pl.mmp + 2, 3)
                cost = pt.pl.mmp * 5
        elif kind == 2:
            t1 = f"ちから {pad(pt.pl.atk,2)}"
            if pt.pl.atk < 98:
                t2 = pad(pt.pl.atk + 2, 3)
                cost = pt.pl.atk * 5
        elif kind == 3:
            t1 = f"はやさ {pad(pt.pl.spd,2)}"
            if pt.pl.spd < 98:
                t2 = pad(pt.pl.spd + 2, 3)
                cost = pt.pl.spd * 5
        return t1, t2, cost

    def update(self):
        ret = self.cur.update()

        if ret < 0:
            Window.close()
        else:
            pt = gbl.get_party()
            _, _, cost = self.shop_get_item(ret)
            if cost == 0 or pt.gold < cost:
                return
            pt.gold -= cost
            if ret == 0:
                pt.pl.mhp += 5
                pt.pl.hp = pt.pl.mhp
            elif ret == 1:
                pt.pl.mmp += 2
                pt.pl.mp = self.pl.mmp
            elif ret == 2:
                pt.pl.atk += 2
            elif ret == 3:
                pt.pl.spd += 2
            # px.play(3, 32)
            self.shop_show()

    def draw(self):
        pyxel.text(75, 0, "now playing...", 14)




