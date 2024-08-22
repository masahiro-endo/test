import pygame
from pygame.locals import *
from UI import *
import os
import struct
import codecs
import control 
from actor import *


GS = 32





class Map:
    # main()のload_mapchips()でセットされる
    images = []  # マップチップ（ID->イメージ）
    movable_type = []  # マップチップが移動可能か？（0:移動不可, 1:移動可）
    def __init__(self, name, party):
        self.name = name
        self.row = -1  # 行数
        self.col = -1  # 列数
        self.map = []  # マップデータ（2次元リスト）
        self.charas = []  # マップにいるキャラクターリスト
        self.events = []  # マップにあるイベントリスト
        self.party = party  # Partyの登録（衝突判定用）
        self.load()  # マップをロード
        self.load_event()  # イベントをロード
    def create(self, dest_map):
        """dest_mapでマップを初期化"""
        self.name = dest_map
        self.charas = []
        self.events = []
        self.load()
        self.load_event()
    def add_chara(self, chara):
        """キャラクターをマップに追加する"""
        self.charas.append(chara)
    def update(self):
        """マップの更新"""
        # マップにいるキャラクターの更新
        for chara in self.charas:
            chara.update(self)  # mapを渡す
    def draw(self, screen, offset):
        """マップを描画する"""
        offsetx, offsety = offset
        # マップの描画範囲を計算
        startx = int(offsetx / GS)
        endx = int(startx + SCR_RECT.width/GS + 1)
        starty = int(offsety / GS)
        endy = int(starty + SCR_RECT.height/GS + 1)
        # マップの描画
        for y in range(starty, endy):
            for x in range(startx, endx):
                # マップの範囲外はデフォルトイメージで描画
                # この条件がないとマップの端に行くとエラー発生
                if x < 0 or y < 0 or x > self.col-1 or y > self.row-1:
                    screen.blit(self.images[self.default], (x*GS-offsetx,y*GS-offsety))
                else:
                    screen.blit(self.images[self.map[y][x]], (x*GS-offsetx,y*GS-offsety))
        # このマップにあるイベントを描画
        for event in self.events:
            event.draw(screen, offset)
        # このマップにいるキャラクターを描画
        for chara in self.charas:
            chara.draw(screen, offset)
    def is_movable(self, x, y):
        """(x,y)は移動可能か？"""
        # マップ範囲内か？
        if x < 0 or x > self.col-1 or y < 0 or y > self.row-1:
            return False
        # マップチップは移動可能か？
        if self.movable_type[self.map[y][x]] == 0:
            return False
        # キャラクターと衝突しないか？
        for chara in self.charas:
            if chara.x == x and chara.y == y:
                return False
        # イベントと衝突しないか？
        for event in self.events:
            if self.movable_type[event.mapchip] == 0:
                if event.x == x and event.y == y:
                    return False
        # 先頭プレイヤーと衝突しないか？
        # 先頭プレイヤー以外は無視
        player = self.party.member[0]
        if player.x == x and player.y == y:
            return False
        return True
    def get_chara(self, x, y):
        """(x,y)にいるキャラクターを返す。いなければNone"""
        for chara in self.charas:
            if chara.x == x and chara.y == y:
                return chara
        return None
    def get_event(self, x, y):
        """(x,y)にあるイベントを返す。なければNone"""
        for event in self.events:
            if event.x == x and event.y == y:
                return event
        return None
    def remove_event(self, event):
        """eventを削除する"""
        self.events.remove(event)
    def load(self):
        """バイナリファイルからマップをロード"""
        file = os.path.join("data", self.name + ".map")
        fp = open(file, "rb")
        # unpack()はタプルが返されるので[0]だけ抽出
        self.row = struct.unpack("i", fp.read(struct.calcsize("i")))[0]  # 行数
        self.col = struct.unpack("i", fp.read(struct.calcsize("i")))[0]  # 列数
        self.default = struct.unpack("B", fp.read(struct.calcsize("B")))[0]  # デフォルトマップチップ
        # マップ
        self.map = [[0 for c in range(self.col)] for r in range(self.row)]
        for r in range(self.row):
            for c in range(self.col):
                self.map[r][c] = struct.unpack("B", fp.read(struct.calcsize("B")))[0]
        fp.close()
    def load_event(self):
        """ファイルからイベントをロード"""
        file = os.path.join("data", self.name + ".evt")
        # テキスト形式のイベントを読み込む
        fp = codecs.open(file, "r", "utf-8")
        for line in fp:
            line = line.rstrip()  # 改行除去
            if line.startswith("#"): continue  # コメント行は無視
            if line == "": continue  # 空行は無視
            data = line.split(",")
            event_type = data[0]
            if event_type == "BGM":  # BGMイベント
                self.play_bgm(data)
            elif event_type == "CHARA":  # キャラクターイベント
                self.create_chara(data)
            elif event_type == "MOVE":  # 移動イベント
                self.create_move(data)
            elif event_type == "TREASURE":  # 宝箱
                self.create_treasure(data)
            elif event_type == "DOOR":  # とびら
                self.create_door(data)
            elif event_type == "OBJECT":  # 一般オブジェクト（玉座など）
                self.create_obj(data)
        fp.close()
    def play_bgm(self, data=None):
        """BGMを鳴らす"""
        if not data:
            pygame.mixer.music.load(self.bgm_file)
            pygame.mixer.music.play(-1)
        else:
            bgm_file = "%s.mp3" % data[1]
            self.bgm_file = os.path.join("bgm", bgm_file)
            pygame.mixer.music.load(self.bgm_file)
            pygame.mixer.music.play(-1)
    def create_chara(self, data):
        """キャラクターを作成してcharasに追加する"""
        name = data[1]
        x, y = int(data[2]), int(data[3])
        direction = int(data[4])
        movetype = int(data[5])
        message = data[6]
        chara = Character(name, (x,y), direction, movetype, message)
        self.charas.append(chara)
    def create_move(self, data):
        """移動イベントを作成してeventsに追加する"""
        x, y = int(data[1]), int(data[2])
        mapchip = int(data[3])
        dest_map = data[4]
        dest_x, dest_y = int(data[5]), int(data[6])
        move = MoveEvent((x,y), mapchip, dest_map, (dest_x,dest_y))
        self.events.append(move)
    def create_treasure(self, data):
        """宝箱を作成してeventsに追加する"""
        x, y = int(data[1]), int(data[2])
        item = data[3]
        treasure = Treasure((x,y), item)
        self.events.append(treasure)
    def create_door(self, data):
        """とびらを作成してeventsに追加する"""
        x, y = int(data[1]), int(data[2])
        door = Door((x,y))
        self.events.append(door)
    def create_obj(self, data):
        """一般オブジェクトを作成してeventsに追加する"""
        x, y = int(data[1]), int(data[2])
        mapchip = int(data[3])
        obj = Object((x,y), mapchip)
        self.events.append(obj)




class Treasure():
    """宝箱"""
    def __init__(self, pos, item):
        self.x, self.y = pos[0], pos[1]  # 宝箱座標
        self.mapchip = 46  # 宝箱は46
        self.image = Map.images[self.mapchip]
        self.rect = self.image.get_rect(topleft=(self.x*GS, self.y*GS))
        self.item = item  # アイテム名
    def open(self):
        """宝箱をあける"""
        sounds["treasure"].play()
        # TODO: アイテムを追加する処理
    def draw(self, screen, offset):
        """オフセットを考慮してイベントを描画"""
        offsetx, offsety = offset
        px = self.rect.topleft[0]
        py = self.rect.topleft[1]
        screen.blit(self.image, (px-offsetx, py-offsety))
    def __str__(self):
        return "TREASURE,%d,%d,%s" % (self.x, self.y, self.item)

class Door:
    """とびら"""
    def __init__(self, pos):
        self.x, self.y = pos[0], pos[1]
        self.mapchip = 45
        self.image = Map.images[self.mapchip]
        self.rect = self.image.get_rect(topleft=(self.x*GS, self.y*GS))
    def open(self):
        """とびらをあける"""
        sounds["door"].play()
    def draw(self, screen, offset):
        """オフセットを考慮してイベントを描画"""
        offsetx, offsety = offset
        px = self.rect.topleft[0]
        py = self.rect.topleft[1]
        screen.blit(self.image, (px-offsetx, py-offsety))
    def __str__(self):
        return "DOOR,%d,%d" % (self.x, self.y)

class Object:
    """一般オブジェクト"""
    def __init__(self, pos, mapchip):
        self.x, self.y = pos[0], pos[1]
        self.mapchip = mapchip
        self.image = Map.images[self.mapchip]
        self.rect = self.image.get_rect(topleft=(self.x*GS, self.y*GS))
    def draw(self, screen, offset):
        """オフセットを考慮してイベントを描画"""
        offsetx, offsety = offset
        px = self.rect.topleft[0]
        py = self.rect.topleft[1]
        screen.blit(self.image, (px-offsetx, py-offsety))
    def __str__(self):
        return "OBJECT,%d,%d,%d" % (self.x, self.y, mapchip)







class Title:
    """タイトル画面"""
    START, CONTINUE, EXIT = 0, 1, 2
    def __init__(self, msg_engine):
        self.msg_engine = msg_engine
        self.title_img = control.Ctl.load_image("data", "python_quest.png", -1)
        self.cursor_img = control.Ctl.load_image("data", "cursor2.png", -1)
        self.menu = self.START
        self.play_bgm()
    def update(self):
        pass
    def draw(self, screen):
        screen.fill((0,0,128))
        # タイトルの描画
        screen.blit(self.title_img, (20,60))
        # メニューの描画
        self.msg_engine.draw_string(screen, (260,240), "ＳＴＡＲＴ")
        self.msg_engine.draw_string(screen, (260,280), "ＣＯＮＴＩＮＵＥ")
        self.msg_engine.draw_string(screen, (260,320), "ＥＸＩＴ")
        # クレジットの描画
        self.msg_engine.draw_string(screen, (130,400), "２００８　ＰＹＴＨＯＮでゲームつくりますがなにか？")
        # メニューカーソルの描画
        if self.menu == self.START:
            screen.blit(self.cursor_img, (240, 240))
        elif self.menu == self.CONTINUE:
            screen.blit(self.cursor_img, (240, 280))
        elif self.menu == self.EXIT:
            screen.blit(self.cursor_img, (240, 320))
    def play_bgm(self):
        bgm_file = "title.mp3"
        bgm_file = os.path.join("bgm", bgm_file)
        pygame.mixer.music.load(bgm_file)
        pygame.mixer.music.play(-1)






class Battle:
    """戦闘画面"""
    def __init__(self, msgwnd, msg_engine):
        self.msgwnd = msgwnd
        self.msg_engine = msg_engine
        # 戦闘コマンドウィンドウ
        self.cmdwnd = BattleCommandWindow(Rect(96, 338, 136, 136), self.msg_engine)
        # プレイヤーステータス（Playerクラスに実装した方がよい）
        status = [["けんし　", 16, 0, 1],
                  ["エルフ　", 15, 24, 1],
                  ["そうりょ", 10, 8, 1],
                  ["まどうし", 8, 12, 1]]
        # 戦闘ステータスウィンドウ
        self.status_wnd = []
        self.status_wnd.append(BattleStatusWindow(Rect(90, 8, 104, 136), status[0], self.msg_engine))
        self.status_wnd.append(BattleStatusWindow(Rect(210, 8, 104, 136), status[1], self.msg_engine))
        self.status_wnd.append(BattleStatusWindow(Rect(330, 8, 104, 136), status[2], self.msg_engine))
        self.status_wnd.append(BattleStatusWindow(Rect(450, 8, 104, 136), status[3], self.msg_engine))
        self.monster_img = control.Ctl.load_image("data", "dragon.png", -1)
    def start(self):
        """戦闘の開始処理、モンスターの選択、配置など"""
        self.cmdwnd.hide()
        for bsw in self.status_wnd:
            bsw.hide()
        self.msgwnd.set("やまたのおろちが　あらわれた。")
        self.play_bgm()
    def update(self):
        pass
    def draw(self, screen):
        screen.fill((0,0,0))
        screen.blit(self.monster_img, (200, 170))
        self.cmdwnd.draw(screen)
        for bsw in self.status_wnd:
            bsw.draw(screen)
    def play_bgm(self):
        bgm_file = "battle.mp3"
        bgm_file = os.path.join("bgm", bgm_file)
        pygame.mixer.music.load(bgm_file)
        pygame.mixer.music.play(-1)

class BattleCommandWindow(Window):
    """戦闘のコマンドウィンドウ"""
    LINE_HEIGHT = 8  # 行間の大きさ
    ATTACK, SPELL, ITEM, ESCAPE = range(4)
    COMMAND = ["たたかう", "じゅもん", "どうぐ", "にげる"]
    def __init__(self, rect, msg_engine):
        Window.__init__(self, rect)
        self.text_rect = self.inner_rect.inflate(-32, -16)
        self.command = self.ATTACK  # 選択中のコマンド
        self.msg_engine = msg_engine
        self.cursor = control.Ctl.load_image("data", "cursor2.png", -1)
        self.frame = 0
    def draw(self, screen):
        Window.draw(self, screen)
        if self.is_visible == False: return
        # コマンドを描画
        for i in range(0, 4):
            dx = self.text_rect[0] + MessageEngine.FONT_WIDTH
            dy = self.text_rect[1] + (self.LINE_HEIGHT+MessageEngine.FONT_HEIGHT) * (i % 4)
            self.msg_engine.draw_string(screen, (dx,dy), self.COMMAND[i])
        # 選択中のコマンドの左側に▶を描画
        dx = self.text_rect[0]
        dy = self.text_rect[1] + (self.LINE_HEIGHT+MessageEngine.FONT_HEIGHT) * (self.command % 4)
        screen.blit(self.cursor, (dx,dy))
    def show(self):
        """オーバーライド"""
        self.command = self.ATTACK  # 追加
        self.is_visible = True

class BattleStatusWindow(Window):
    """戦闘画面のステータスウィンドウ"""
    LINE_HEIGHT = 8  # 行間の大きさ
    def __init__(self, rect, status, msg_engine):
        Window.__init__(self, rect)
        self.text_rect = self.inner_rect.inflate(-32, -16)
        self.status = status  # status = ["なまえ", HP, MP, LV]
        self.msg_engine = msg_engine
        self.frame = 0
    def draw(self, screen):
        Window.draw(self, screen)
        if self.is_visible == False: return
        # ステータスを描画
        status_str = [self.status[0], u"H%3d" % self.status[1], u"M%3d" % self.status[2], u"%s%3d" % (self.status[0][0], self.status[3])]
        for i in range(0, 4):
            dx = self.text_rect[0]
            dy = self.text_rect[1] + (self.LINE_HEIGHT+MessageEngine.FONT_HEIGHT) * (i % 4)
            self.msg_engine.draw_string(screen, (dx,dy), status_str[i])




class MoveEvent():
    """移動イベント"""
    def __init__(self, pos, mapchip, dest_map, dest_pos):
        self.x, self.y = pos[0], pos[1]  # イベント座標
        self.mapchip = mapchip  # マップチップ
        self.dest_map = dest_map  # 移動先マップ名
        self.dest_x, self.dest_y = dest_pos[0], dest_pos[1]  # 移動先座標
        self.image = Map.images[self.mapchip]
        self.rect = self.image.get_rect(topleft=(self.x*GS, self.y*GS))
    def draw(self, screen, offset):
        """オフセットを考慮してイベントを描画"""
        offsetx, offsety = offset
        px = self.rect.topleft[0]
        py = self.rect.topleft[1]
        screen.blit(self.image, (px-offsetx, py-offsety))
    def __str__(self):
        return "MOVE,%d,%d,%d,%s,%d,%d" % (self.x, self.y, self.mapchip, self.dest_map, self.dest_x, self.dest_y)
