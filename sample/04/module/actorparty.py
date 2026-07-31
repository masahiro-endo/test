
from module.UI import *
from module.actor import *
from module.actorvm import *
from module.state.actorstate import *









class BaseParty():
    def __init__(self):
        self._member = []

    def __len__(self):
        return len(self._member)
    
    def __getitem__(self, index):
        return self._member[index]
    
    def __setitem__(self, index, value):
        self._member[index] = value
    #「in」
    def __contains__(self, item):
        return item in self._member
    
    def __iter__(self):
        return iter(self._member)

    #「+」 演算子
    def __add__(self, other):
        return self._member + other._member
    
    def __getattr__(self, name):
        if name == 'type':
            return self._member
        raise AttributeError


    def add_member(self, chr):
        self._member.append(chr)

    def remove_member(self, idx):
        try:
            del self._member[idx]
        except:
            raise Exception("the specified member doesn't exist.：" + str(idx))

    def clear_member(self):
        self._member.clear()
        
    def get_alive_actors(self):
        return [p for p in self._member if p.is_alive()]





class PlayerParty(BaseParty):

    def __init__(self):
        super().__init__()
        mem = Player(self, "あなた", 30,  6, 12, 12, JOB.WARRIOR)
        mem.skills = [("攻撃", SkillMeth.normal_attack, SKLTYP.ATTK), ("呪文", None, SKLTYP.NODE), ("逃走", SkillMeth.escape, SKLTYP.SPEC)]
        mem.spells = [("全体", SkillMeth.aoe, SKLTYP.ATTK), ("回復", SkillMeth.heal, SKLTYP.SUPP)]
        self.add_member(mem)
 
        mem = Player(self, "そうりょ", 15, 50, 5, 10, JOB.PRIEST)
        mem.skills = [("攻撃", SkillMeth.poison_attack, SKLTYP.ATTK), ("呪文", None, SKLTYP.NODE)]
        mem.spells = [("全体", SkillMeth.aoe, SKLTYP.ATTK), ("回復", SkillMeth.heal, SKLTYP.SUPP)]
        self.add_member(mem)
 
        # mem = Player(self, "にんじゃ", 20, 5, 8, 15, JOB.NINJA)
        # mem.skills = [("麻痺攻撃", SkillMeth.paralyze_attack), ("全体攻撃", SkillMeth.aoe)]
        # self.add_member(mem)

        self.gold = 0
        self.keys = 0    # カギの数
        self.flags = []  # フラグ（宝箱、扉などの判定用）
        self.enc = 0     # エンカウント
        self.frames = 0
        self.action = ActorStates(self)

        self.get_start_location()
        (self.dx, self.dy, self.spd) = (0, 0, 4)


    def update(self):
        self.action.update()

    def draw(self):
        self.action.draw()

    def get_current_floor(self):
        return self.z

    def use_return(self):
        if gbl.scene_state(): gbl.scene_state().Main()
        (self.x, self.y, self.z) = (8, 21, 0)
        # self.play_bgm(2)

    def get_start_location(self):
        self.use_return()

    def add_gold(self, gold):
        self.gold = min(self.gold + gold, 9999)

    def pos_try_move(self):
        x = self.x + self.dx
        y = self.y + self.dy
        return (x, y)

    def pos_3d(self):
        (x, y) = self.pos_try_move()
        z = self.get_current_floor()
        return (x, y, z)


    def try_move_forward(self):
        # Tileの定義位置は、イメージバンクが関わるため、
        # 座標にはz軸も必要
        pos = self.pos_3d()
        evt = MapMeth.get_obs_key(pos)
        obj = MapTiles.is_defined(pos) and not MapTiles.is_walkable(pos)

        # 扉開放や宝箱取得時点でフラグを保持し、
        # 以降は通過を許す
        if obj or (evt and not evt in self.flags): 
            self.fire_event_in_front()
        else:
            self.move_step()

    # 移動（１マス）開始
    def move_step(self):
        self.dx *= self.spd
        self.dy *= self.spd
        self.moving = True
        Window.close()

    def fire_event_in_front(self):
        pos = self.pos_3d() # 踏み出し直後の座標を保持
        self.dx, self.dy = (0, 0)
            
        # 進行先タイルに紐づくイベント処理 泉
        MapTiles.sensor_spring(**{'pos': pos, 'pt': self})

        evt = MapMeth.get_obs_key(pos)
        if evt and not evt in self.flags:
            ob = gbl.map_resource().obstacles[evt]
            ob.response(**{'evt': evt, 'pos': pos, 'pt': self, 'ob': ob })


    # 移動（１ステップ）終了
    def move_end(self):
        self.y += self.dy // 16 
        self.x += self.dx // 16
        self.dy = 0
        self.dx = 0
        self.moving = False

        # 移動後のタイルに紐づくイベント処理 階段
        pos = self.pos_3d()
        MapTiles.sensor_stairs(**{'pos': pos, 'pt': self})

        self.recover_health_gradually()
        self.roll_encount()

    def recover_health_gradually(self):
        if (self.x + self.y) % 2 == 0:
            self[0].hp = min(self[0].hp + 1, self[0].mhp)

    def roll_encount(self):
        # 地下1階、ひほう取得〜エンディングは敵がでない
        if self.z == 0 or ("4-3" in self.flags and not "end" in self.flags):
            return
        self.enc += 1

        if self.enc > 12 and px.rndi(0, 7) == 0:
            self.enc = 0
            # ms_id = self.get_enemy_race()
            # self.battle_start(ms_id)
            gbl.current_scene().Battle()

    def get_enemy_random(self):
            return self.get_current_floor() + (0 if px.rndi(0, 3) < 3 else 1)


    def field_status(self):
        return [
            f"HP {Meth.pad(self[0].hp,3)}/{Meth.pad(self[0].mhp,3)}",
            f"MP  {Meth.pad(self[0].mp,2)}/ {Meth.pad(self[0].mmp,2)}",
            f"ちから {Meth.pad(self[0].atk,2)}  はやさ {Meth.pad(self[0].spd,2)}",
            f" {Meth.pad(self.gold,4)}G  カギ {Meth.pad(self.keys,2)}こ",
        ]



class EnemyParty(BaseParty):
    
    opt = ['A','B','C','D','E','F']

    def __init__(self, race):
        super().__init__()
        self.race = race

    def add_member(self, chr):
        self._member.append(chr)
        # 複数体の場合は、甲乙丙を付与
        # 異種族混在は不可。Party を分けるか？
        for i, mem in enumerate(self._member):
            mem.name = mem.race + self.opt[i]





