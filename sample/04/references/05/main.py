import pyxel
import math # math.floorを使うので必要
import random
import array2d
import gameobject
import ease
from enum import Enum

def to_absolute(path):
    return "/Users/syun/Desktop/tilemap2/" + path

# 状態
class State(Enum):
    Standby = 1 # 待機中
    Moving  = 2 # 移動中 
    GameClear = 3 # ゲームクリア
    MovingEnemy = 4 # 敵の接近
    GameOver = 5 # ゲームオーバー
    
    EraseLine = 10 # ライン消し

class Chip:
    Empty  = 0 # 何もない
    Door   = 4 # ゴール
    Player = 8 # プレイヤー
    ClosedDoor = 9 # 閉まったドア
    Enemy1 = 13 # 敵1
    Enemy2 = 14 # 敵2
    Enemy3 = 18 # 敵3

class Player(gameobject.GameObject):
    MOVE_SPEED = 10 # 移動速度

    State_Standby = 1
    State_Moving  = 2
    def __init__(self):
        gameobject.GameObject.__init__(self)
        self.state = self.State_Standby
        self.timer = 0
        self.set_position(0, 0)
    def is_standby(self):
        return self.state == self.State_Standby
    def set_position(self, x, y):
        gameobject.GameObject.set_position(self, x, y)
        self.xnext, self.ynext = x, y
    def set_next(self, xnext, ynext):
        self.xnext, self.ynext = xnext, ynext
        self.state = self.State_Moving
        self.timer = 0
    def update(self):
        if self.state == self.State_Moving:
            self.timer += 1
            if self.timer >= self.MOVE_SPEED:
                self.state = self.State_Standby
                self.x = self.xnext
                self.y = self.ynext
    def draw(self):
        px = self.x
        py = self.y
        if self.state == self.State_Moving:
            # 移動中だけ特殊処理
            dx = self.xnext - self.x
            dy = self.ynext - self.y
            # 移動先との差を線形補間する
            px += dx * self.timer / self.MOVE_SPEED
            py += dy * self.timer / self.MOVE_SPEED
        Map.draw_chip(px, py, Chip.Player)        

class Enemy(gameobject.GameObject):
    MOVE_SPEED = 20

    State_CantMove      = 1 # 移動できない
    State_CloseToPlayer = 2 # プレイヤーに近く
    State_End           = 3 # 近づき終わった

    parent = None
    target = None
    
    @classmethod
    def create(cls, num):
        cls.parent = gameobject.GameObjectManager(num, Enemy)
    @classmethod
    def add(cls, x, y):
        obj = cls.parent.add()
        if obj is None:
            return None
        obj.init(x, y)
    @classmethod
    def found_player(cls):
        for obj in cls.parent.pool:
            if obj.exists == False:
                continue
            if obj.state in [Enemy.State_CloseToPlayer, Enemy.State_End]:
                return True
        return False
    @classmethod
    def cought_player(cls):
        for obj in cls.parent.pool:
            if obj.exists == False:
                continue
            if obj.state == Enemy.State_End:
                return True
        return False

    def __init__(self):
        gameobject.GameObject.__init__(self)
    def init(self, x, y):
        self.x = x
        self.y = y
        self.xnext = x
        self.ynext = y
        self.timer = random.randint(0, 100)
        self.state = self.State_CantMove

    def update(self):
        if self.state == self.State_CantMove:
            self.timer += 1
            if Map.get(self.x, self.y) != Chip.Empty:
                # プレイヤーに近づく
                self.state = self.State_CloseToPlayer
                self.timer = 0
                self.xnext = self.target.x
                self.ynext = self.target.y

        elif self.state == self.State_CloseToPlayer:
            # プレイヤーに近づく
            self.timer += 1
            if self.timer >= self.MOVE_SPEED:
                self.state = self.State_End
                self.x = self.xnext
                self.y = self.ynext
        elif self.state == self.State_End:
            self.timer += 1

    def draw(self):
        chip = Chip.Enemy1
        if self.timer%40 < 8:
            chip = Chip.Enemy2
        if self.state in [self.State_CloseToPlayer, self.State_End]:
            if self.timer%8 < 4:
                chip = Chip.Enemy3
        
        px, py = self.x, self.y
        if self.state == self.State_CloseToPlayer:
            # 移動中だけ特殊処理
            dx = self.xnext - self.x
            dy = self.ynext - self.y
            # 移動先との差を線形補間する
            px += dx * self.timer / self.MOVE_SPEED
            py += dy * self.timer / self.MOVE_SPEED
        
        Map.draw_chip(px, py, chip)


# テトリミノクラス
class Mino:
    PARTTERN_0 = [
        [
            0, 0, 1, 0,
            0, 1, 2, 1,
            0, 0, 0, 0,
            0, 0, 0, 0,
        ],
        [
            0, 0, 1, 0,
            0, 0, 2, 1,
            0, 0, 1, 0,
            0, 0, 0, 0,
        ],
        [
            0, 0, 0, 0,
            0, 1, 2, 1,
            0, 0, 1, 0,
            0, 0, 0, 0,
        ],
        [
            0, 0, 1, 0,
            0, 1, 2, 0,
            0, 0, 1, 0,
            0, 0, 0, 0,
        ],
    ]
    PARTTERN_1 = [
        [
            0, 0, 1, 0,
            1, 1, 2, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
        ],
        [
            0, 1, 0, 0,
            0, 1, 0, 0,
            0, 2, 1, 0,
            0, 0, 0, 0,
        ],
        [
            0, 0, 0, 0,
            0, 2, 1, 1,
            0, 1, 0, 0,
            0, 0, 0, 0,
        ],
        [
            0, 0, 0, 0,
            0, 1, 2, 0,
            0, 0, 1, 0,
            0, 0, 1, 0,
        ],
    ]
    PARTTERN_2 = [
        [
            0, 2, 1, 0,
            1, 1, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
        ],
        [
            1, 0, 0, 0,
            2, 1, 0, 0,
            0, 1, 0, 0,
            0, 0, 0, 0,
        ],
        [
            0, 2, 1, 0,
            1, 1, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
        ],
        [
            1, 0, 0, 0,
            2, 1, 0, 0,
            0, 1, 0, 0,
            0, 0, 0, 0,
        ],
    ]
    PARTTERN_3 = [
        [
            0, 1, 0, 0,
            0, 2, 0, 0,
            0, 1, 0, 0,
            0, 1, 0, 0,
        ],
        [
            0, 0, 0, 0,
            1, 2, 1, 1,
            0, 0, 0, 0,
            0, 0, 0, 0,
        ],
        [
            0, 1, 0, 0,
            0, 2, 0, 0,
            0, 1, 0, 0,
            0, 1, 0, 0,
        ],
        [
            0, 0, 0, 0,
            1, 2, 1, 1,
            0, 0, 0, 0,
            0, 0, 0, 0,
        ],
    ]
    def __init__(self):
        self.data = array2d.Array2D(4, 4)
        self.idx = 0
        self.rot = 0
        self.set_position(0, 0)
        self.set_pattern(self.idx)

    def set_pattern(self, idx):
        if idx == 0:
            list = self.PARTTERN_0[self.rot]
        elif idx == 1:
            list = self.PARTTERN_1[self.rot]
        elif idx == 2:
            list = self.PARTTERN_2[self.rot]
        elif idx == 3:
            list = self.PARTTERN_3[self.rot]
        for i, v in enumerate(list):
            self.data.set_from_idx(i, v)

    def set_position(self, x, y):
        self.x = math.floor(x/Map.SIZE)*Map.SIZE
        self.y = math.floor(y/Map.SIZE)*Map.SIZE

    def rotate(self):
        self.rot += 1
        if self.rot >= 4:
            self.rot = 0
        self.set_pattern(self.idx)

    def update(self):
        # 更新
        # マウス座標を設定
        self.set_position(pyxel.mouse_x, pyxel.mouse_y)
        if pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON):
            self.rotate()

    def get_center(self):
        # 中心座標を取得する
        ofs_x = math.floor(self.x/Map.SIZE)
        ofs_y = math.floor(self.y/Map.SIZE)
        # 中心座標を取得する
        cx, cy = self.data.search(2)
        ofs_x -= cx
        ofs_y -= cy
        return ofs_x, ofs_y

    def get_center2(self):
        # 中心座標を取得する
        ofs_x = math.floor(self.x/Map.SIZE)
        ofs_y = math.floor(self.y/Map.SIZE)
        return ofs_x, ofs_y

    def put(self):
        # テトリミノを配置する
        ofs_x, ofs_y = self.get_center()

        xline = []
        yline = []

        for j in range(self.data.height):
            for i in range(self.data.width):
                val = self.data.get(i, j)
                if val == 0:
                    continue
                x = i + ofs_x
                y = j + ofs_y
                v = Map.get(x, y)
                Map.set(x, y, 1)
                if v == 0:
                    # 新たに揃ったかどうか
                    # X軸
                    if self.check_to_erase_line_xaxis(y):
                        yline.append(y)
                    # Y軸
                    if self.check_to_erase_line_yaxis(x):
                        xline.append(x)
        
        for x in xline:
            LineEffect.add(x, 0, 1, Map.HEIGHT)
        for y in yline:
            LineEffect.add(0, y, Map.WIDTH, 1)
        
        self.idx += 1
        if self.idx > 3:
            self.idx = 0
        self.set_pattern(self.idx)

    def check_to_erase_line_xaxis(self, y):
        for i in range(Map.WIDTH):
            if Map.get(i, y) == 0:
                return False
        return True
    def check_to_erase_line_yaxis(self, x):
        for j in range(Map.HEIGHT):
            if Map.get(x, j) == 0:
                return False
        return True
    def draw(self):
        # 中心座標を取得する
        cx, cy = self.data.search(2)
        for j in range(self.data.height):
            for i in range(self.data.width):
                v = self.data.get(i, j)
                if v < 1:
                    continue
                px = self.x + (i * Map.SIZE)
                py = self.y + (j * Map.SIZE)
                px -= (cx * Map.SIZE)
                py -= (cy * Map.SIZE)
                px += 1
                py += 1
                s = Map.SIZE - 2
                pyxel.rect(px, py, px+s, py+s, 6)
    def draw_line(self):
        # 中心座標を取得する
        cx, cy = self.data.search(2)
        for j in range(self.data.height):
            for i in range(self.data.width):
                v = self.data.get(i, j)
                if v < 1:
                    continue
                px = self.x + (i * Map.SIZE)
                py = self.y + (j * Map.SIZE)
                px -= (cx * Map.SIZE)
                py -= (cy * Map.SIZE)
                pyxel.rectb(px, py, px+Map.SIZE, py+Map.SIZE, 7)

class LineEffect(gameobject.GameObject):
    TIMER_DESTROY = 20

    parent = None
    @classmethod
    def create(cls, num):
        cls.parent = gameobject.GameObjectManager(num, LineEffect)
    @classmethod
    def add(cls, x, y, w, h):
        obj = cls.parent.add()
        if obj is None:
            return
        obj.init(x, y, w, h)
    def __init__(self):
        gameobject.GameObject.__init__(self)
        self.init(0, 0, 0, 0)
    def init(self, x, y, width, height):
        self.timer = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def update(self):
        self.timer += 1
        if self.timer > self.TIMER_DESTROY:
            for e in Enemy.parent.pool:
                if e.exists == False:
                    continue
                for j in range(self.height):
                    for i in range(self.width):
                        x = self.x + i
                        y = self.y + j
                        if e.x == x and e.y == y:
                            e.exists = False
            self.exists = False
    def draw(self):
        px, py = Map.to_screen(self.x, self.y)
        w = self.width * Map.SIZE
        h = self.height * Map.SIZE
        rate = 1.0 * self.timer / self.TIMER_DESTROY
        rate = 0
        dx = w * 1 * ease.expoOut(rate)
        dy = h * -1 * ease.expoOut(rate)
        w += dx
        h += dy
        if self.timer%2 == 0:
            pyxel.rect(px-dx, py-dy, px+w, py+h, 7)
        pyxel.rectb(px-dx, py-dy, px+w, py+h, 8)
class Map:
    SIZE = 8 # チップサイズ
    WIDTH = 6
    HEIGHT = 6
    CHIP_WIDTH = 5 # 1列に5つ並んでいる
    CHIP_HEIGHT = 5 # 5行並んでいる
    DATA = array2d.Array2D()
    
    # 生成
    @classmethod
    def create(cls, width, height):
        cls.DATA.create(width, height)
    
    # 存在数を取得する
    @classmethod
    def count(cls, val):
        return cls.DATA.count(val)

    # 値の設定
    @classmethod
    def set(cls, x, y, v):
        cls.DATA.set(x, y, v)
    @classmethod
    def set_from_idx(cls, idx, v):
        cls.DATA.set_from_idx(idx, v)
    
    # 値の取得
    @classmethod
    def get(cls, x, y):
        return cls.DATA.get(x, y)

    # 値の検索
    @classmethod
    def search(cls, val):
        return cls.DATA.search(val)

    # マップチップ座標をスクリーン座標に変換
    @classmethod
    def to_screen(cls, i, j):
        return (i * cls.SIZE, j * cls.SIZE)
    
    # マップの描画
    @classmethod
    def draw(cls):
        for j in range(cls.HEIGHT):
            for i in range(cls.WIDTH):
                val = cls.get(i, j)
                if val == 0:
                    continue
                x, y = cls.to_screen(i, j)
                x += 1
                y += 1
                s = cls.SIZE-2
                pyxel.rect(x, y, x+s, y+s, 5)
        # cls.DATA.foreach(lambda x, y, val: cls.draw_chip(x, y, val))

    # マップチップの描画
    @classmethod
    def draw_chip(cls, i, j, val):
        # スクリーン座標に変換
        x, y = cls.to_screen(i, j)
        # チップ画像の座標を計算
        u = (val % cls.CHIP_WIDTH) * cls.SIZE
        v = (math.floor(val / cls.CHIP_WIDTH)) * cls.SIZE
        pyxel.blt(x, y, 0, u, v, cls.SIZE, cls.SIZE, 2)

    @classmethod
    def dump(cls):
        cls.DATA.dump()

# ドアクラス
class Door:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.opened = False
    def update(self):
        if Map.get(self.x, self.y) != 0:
            self.opened = True
    def check_clear(self, x, y):
        return self.x == x and self.y == y
    def draw(self):
        chip = Chip.ClosedDoor
        if self.opened:
            chip = Chip.Door
        Map.draw_chip(self.x, self.y, chip)

class App:
    MOVE_SPEED = 10 # 移動速度
    def __init__(self):        
        pyxel.init(160, 120, fps=60)
        self.init() # 初期化
        pyxel.mouse(True) # マウスを表示する
        pyxel.image(0).load(0, 0, to_absolute("tileset.png"))
        pyxel.run(self.update, self.draw)

    def init(self):
        # 初期化
        # マップデータ読み込み
        self.load_map(to_absolute("map.txt"))
        # プレイヤーの位置を取得
        xplayer, yplayer = Map.search(Chip.Player)
        # マップデータからプレイヤーを削除
        Map.set(xplayer, yplayer, Chip.Empty)
        self.player = Player()
        self.player.set_position(xplayer, yplayer)
        Map.set(xplayer, yplayer, 1) # プレイヤー開始地を踏破扱いにする

        # ドアの生成
        xdoor, ydoor = Map.search(Chip.Door)
        self.door = Door(xdoor, ydoor)
        # ドア情報を消しておく
        Map.set(xdoor, ydoor, Chip.Empty)

        # テトリミノ
        self.mino = Mino()

        LineEffect.create(32)

        # 敵の生成
        Enemy.target = self.player
        Enemy.create(32)
        cnt = Map.count(Chip.Enemy1)
        for i in range(cnt):
            xenemy, yenemy = Map.search(Chip.Enemy1)
            Enemy.add(xenemy, yenemy)
            Map.set(xenemy, yenemy, Chip.Empty) # チップを消しておく

        self.state = State.Standby # 状態

    def load_map(self, txt):
        # マップ読み込み
        map = []
        map_file = open(txt)
        for line in map_file:
            # １行ずつ読み込み
            data = line.split(",")
            for d in data:
                # 余分な文字を削除
                s = d.strip()
                if s == "":
                    break
                v = int(d.strip())
                map.append(v)

        # マップ生成
        Map.create(Map.WIDTH, Map.HEIGHT)
        for i, v in enumerate(map):
            Map.set_from_idx(i, v)

    def update(self):
        if pyxel.btnp(pyxel.KEY_R):
            # リスタート
            self.init()
            return

        # プレイヤーの更新
        self.player.update()

        # 更新
        if self.state == State.Standby:
            # 敵の更新
            Enemy.parent.update()
            # キー入力待ち
            if self.input_key():
                # 移動開始する
                self.state = State.Moving
        elif self.state == State.Moving:
            # 移動中
            if self.player.is_standby():
                # 移動完了
                if LineEffect.parent.count_exists() > 0:
                    # ライン消去エフェクト
                    self.state = State.EraseLine
                    return

                # 敵の更新
                Enemy.parent.update()
                if Enemy.found_player():
                    # プレイヤーを見つけた
                    self.state = State.MovingEnemy
                elif self.door.check_clear(self.player.x, self.player.y):
                    # ゴールにたどり着いたのでゲームクリア
                    self.state = State.GameClear
                else:
                    self.state = State.Standby
        elif self.state == State.MovingEnemy:
            # 敵の更新
            Enemy.parent.update()
            # 敵移動中
            if Enemy.cought_player():
                # プレイヤーを捕捉した
                self.state = State.GameOver
        elif self.state == State.GameOver:
            # 敵の更新
            Enemy.parent.update()
        elif self.state == State.EraseLine:
            LineEffect.parent.update()
            if LineEffect.parent.count_exists() == 0:
                Enemy.parent.update()
                if Enemy.found_player():
                    # プレイヤーを見つけた
                    self.state = State.MovingEnemy
                elif self.door.check_clear(self.player.x, self.player.y):
                    # ゴールにたどり着いたのでゲームクリア
                    self.state = State.GameClear
                else:
                    self.state = State.Standby


    def input_key(self):
        # キー入力判定
        self.mino.update()

        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            # 配置する
            self.mino.put()
            self.door.update()
        else:
            # 入力していない
            return False

        # プレイヤーの異動先を設定する
        cx, cy = self.mino.get_center2()
        xnext, ynext = cx, cy
        if self.door.opened:
            xnext, ynext = self.door.x, self.door.y

        self.player.set_next(xnext, ynext)
        return True

    def draw(self):
        pyxel.cls(0)

        if self.state in [State.Standby, State.Moving, State.GameClear, State.EraseLine]:
            # マップの描画
            self.draw_map()
        # テトリミノの描画
        if self.state == State.Standby:
            self.draw_mino()
        # ドアの描画
        self.draw_door()
        # プレイヤーの描画
        self.draw_player()
        # 敵の描画
        Enemy.parent.draw()

        # ライン消去エフェクト
        if self.state == State.EraseLine:
            LineEffect.parent.draw()

        if pyxel.frame_count%24 < 4:
            if self.state == State.Standby:
                self.mino.draw_line()

        if self.state == State.GameClear:
            pyxel.text(4, 52, "GAME CLEAR", 9)
        elif self.state == State.GameOver:
            pyxel.text(4, 52, "GAME OVER", 9)

    # プレイヤーの描画
    def draw_player(self):
        self.player.draw()

    def draw_door(self):
        # ドアの描画
        self.door.draw()

    def draw_map(self):
        # 外枠の描画
        ofs_x = 0
        ofs_y = 0
        pyxel.rectb(ofs_x, ofs_y, Map.SIZE*Map.WIDTH, Map.SIZE*Map.HEIGHT, 5)

        # グリッドの描画
        for i in range(Map.WIDTH):
            x1 = ofs_x + (Map.SIZE * i)
            x2 = x1
            y1 = ofs_y
            y2 = ofs_y + (Map.SIZE * Map.WIDTH) 
            pyxel.line(x1, y1, x2, y2, 5)
        for j in range(Map.HEIGHT):
            x1 = ofs_x
            x2 = ofs_x + (Map.SIZE * Map.HEIGHT)
            y1 = ofs_y + (Map.SIZE * j)
            y2 = y1
            pyxel.line(x1, y1, x2, y2, 5)
        
        # 各チップの描画
        Map.draw()

    def draw_mino(self):
        self.mino.draw()

App()
