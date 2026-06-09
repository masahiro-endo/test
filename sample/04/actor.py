import pyxel as px
from UI import *
from actorstate import *








# 呪文インデックス定数
SPELL_FIRE = 0
SPELL_RETURN = 1
SPELL_HEAL = 2
SPELL_BURST = 3



# フィールド用障害物（kind = 0:ドア 1:宝箱 2:人）
class Obstacle:
    def __init__(self, x, y, z, kind=0, val=0):
        self.x = x
        self.y = y
        self.z = z
        self.kind = kind
        self.val = val

    def draw(self, pl_x, pl_y, pl_z):
        ox = self.x * 16 - pl_x
        oy = self.y * 16 - pl_y
        if abs(ox) < 64 and abs(oy) < 64 and abs(self.z == pl_z):
            if self.kind == 0:
                u, v = 2, 1
            elif self.kind == 1:
                u, v = 3, 1
            else:
                u, v = 2 + (px.frame_count % 30) // 15, 2
            px.blt(56 + ox, 48 + oy, 0, u * 16, v * 16, 16, 16, 1)


# 戦闘用キャラクタ（自分とモンスター）
class Actor:
    def __init__(self, name, hp, mp, atk, spd, resist=0, img=None, gold=0):
        self.name = name
        self.mhp = hp
        self.hp = hp
        self.mmp = mp
        self.mp = mp
        self.atk = atk
        self.spd = spd
        self.resist = resist  # 呪文（ファイア）耐性
        self.img = img  # モンスターの場合の画像イメージ
        self.gold = gold  # 勝利時報酬

class Party:
    def __init__(self):
        self.pl = Actor("あなた", 30, 6, 12, 12)
        # self.go_start_location()
        self.gold = 0
        self.keys = 0  # カギの数
        self.flags = []  # フラグ（宝箱、扉などの判定用）
        self.enc = 0  # エンカウント
        self.frames = 0

        self.state = ActorStates()
        (self.dx, self.dy, self.spd) = (0, 0, 4)

    def update(self):
        self.state.update()
    def draw(self):
        self.state.draw()

    # メニュー用ウィンドウ生成
    def menu_show(self):
        pl = self.pl
        t = [
            f"HP {pad(pl.hp,3)}/{pad(pl.mhp,3)}",
            f"MP  {pad(pl.mp,2)}/ {pad(pl.mmp,2)}",
            f"ちから {pad(pl.atk,2)}  はやさ {pad(pl.spd,2)}",
            f" {pad(self.gold,4)}G  カギ {pad(self.keys,2)}こ",
        ]
        Window.open("menu_stat", 0, 0, 16, 10, t)
        Window.message([f"いま ちか{self.z+1}かいに います", " セーブ じゅもん リセット"])
        self.cur = Cursor("menu", [1, 5, 10], 14, -1)



# 呪文
class Spell:
    def __init__(self, name, mp, on_menu, desc):
        self.name = name
        self.mp = mp
        self.on_menu = on_menu
        self.desc = desc

    def get_mp(self, pl):
        # ヒールやバーストは消費MPが状況依存
        if self.name == "ヒール":
            return min(pl.mp, (pl.mhp - pl.hp + 4) // 5)
        elif self.name == "バースト":
            return pl.mp
        return self.mp




class Resources:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Resources, cls).__new__(cls)
            # 障害物（ドア、宝箱、NPC）データ
            cls._instance.obstacles = {
                "0-1": Obstacle(8, 19, 0, 2),
                "0-2": Obstacle(3, 19, 0, 2),
                "0-3": Obstacle(8, 28, 0, 2),
                "0-4": Obstacle(12, 19, 0, 2),
                "0-5": Obstacle(12, 28, 0, 2),
                "0-6": Obstacle(11, 16, 0, 1),
                "0-7": Obstacle(11, 17, 0, 1, 100),
                "0-8": Obstacle(4, 25, 0, 0),
                "0-9": Obstacle(5, 27, 0, 2),
                "1-1": Obstacle(4, 6, 1, 0),  # ドア1（直行）
                "1-2": Obstacle(27, 3, 1, 2),
                "1-3": Obstacle(7, 21, 1, 1, 50),
                "1-4": Obstacle(8, 12, 1, 1, 6),
                "1-5": Obstacle(12, 12, 1, 1, 110),
                "1-6": Obstacle(16, 24, 1, 1, 80),
                "1-7": Obstacle(24, 10, 1, 1),  # カギ1
                "1-8": Obstacle(13, 8, 1, 0),  # ドア2（宝部屋）
                "1-9": Obstacle(8, 7, 1, 1, 100),
                "1-10": Obstacle(11, 7, 1, 1, 100),
                "1-11": Obstacle(8, 9, 1, 1, 100),
                "1-12": Obstacle(11, 9, 1, 1, 100),
                "2-1": Obstacle(17, 10, 2, 1, 170),
                "2-2": Obstacle(17, 20, 2, 1, 73),
                "2-3": Obstacle(21, 10, 2, 1, 25),
                "2-4": Obstacle(21, 20, 2, 1, 256),
                "2-5": Obstacle(21, 4, 2, 2),
                "2-6": Obstacle(28, 28, 2, 1),  # カギ2
                "2-7": Obstacle(23, 4, 2, 0),  # ドア3（ヒール）
                "3-1": Obstacle(6, 22, 3, 2),
                "3-2": Obstacle(4, 6, 3, 0),  # ドア4（直行）
                "3-3": Obstacle(24, 12, 3, 1),  # カギ3
                "3-4": Obstacle(25, 12, 3, 1, 1000),
                "3-5": Obstacle(4, 10, 3, 0),  # ドア5
                "4-1": Obstacle(16, 11, 4, 1),  # カギ4
                "4-2": Obstacle(18, 25, 4, 1),  # カギ5
                "4-3": Obstacle(4, 27, 4, 2),
            }
            # 会話イベントデータ
            cls._instance.talks = {
                "0-1": ["ちか5かいに ねむる", "ひほうを さがしてまいれ"],
                "0-2": ["いずみのみずを のむと", "HPとMPが かいふくするぞ"],
                "0-4": ["XキーかBボタンで", "メニューを ひらけるぞ"],
                "0-5": ["とびらを あけるには", "カギが ひつようだ"],
                "0-9": ["このさきには", "モンスターが でるぜ"],
                "1-2": ["おまえには もう", "おしえることは ないよ"],
                "2-5": ["まいった！"],
                "3-1": ["チクショウ！"],
            }
            # モンスターデータ
            cls._instance.monsters = (
                ["かぼちゃ", 12, 0, 6, 12, 0, 0, 20],
                ["こおに", 24, 0, 10, 13, 0, 1, 40],
                ["おにび", 32, 2, 14, 18, 1, 2, 80],
                ["ゆうれい", 40, 0, 17, 32, 0, 3, 160],
                ["にんじゃ", 64, 0, 34, 28, 0, 4, 320],
                ["まどうし", 120, 4, 8, 15, 0, 5, 0],
                ["だてんし", 200, 0, 20, 27, 1, 6, 0],
                ["めがみ", 400, 0, 99, 99, 0, 7, 0],
            )
            # 呪文データ
            cls._instance.spells = [
                Spell(
                    "ファイア", 2, False, ["ちいさな ひのたまを", "てきにぶつけて ダメージ"]
                ),
                Spell("リターン", 6, True, ["スタートいちに", "テレポートする"]),
                Spell("ヒール", 0, True, ["HPを かいふく", "かいふくしたぶんMPをつかう"]),
                Spell(
                    "バースト",
                    0,
                    False,
                    ["すべての まりょくを", "てきにぶつけて だいダメージ"],
                ),
            ]

        return cls._instance

def get_resource():
    return Resources()

