# Pygame Zero: ゴールするだけのゲーム
 
import pgzrun
from enum import Enum

# キャラクタチップサイズ
CSIZE = 64  # 64px X 64px
CL_WHITE = 0, 0, 192  # 色
 
# 画面サイズ
WIDTH = CSIZE * 5  # 320px
HEIGHT = CSIZE * 5  # 320px
TITLE = "ゴールするだけのゲーム"
 
# ゲームの状態
class STS(Enum):
    GAME = 0       # ゲーム中
    GAMECLEAR = 1  # ゲームクリア
global status
status = STS.GAME
 
# マップデータ
map = [
    [0, 1, 0, 1, 1],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 1, 1, 0],
]

class Player(Actor):
    def __init__(self, name):
        super().__init__(name)
        self.pos = 0, 0
        self.isMoving = False
        self.isRunning = True

# プレイヤーを生成
px = py = 0  # プレイヤーのマップ上座標を設定
player = Player("player")
player.topleft = px * CSIZE, py * CSIZE  # マップ上の座標を描画座標に変換してプレイヤーを描画


# ゴールを生成
gx = gy = 4  # ゴールのマップ上座標を設定
goal = Actor("bk_goal")
goal.topleft = gx * CSIZE, gy * CSIZE  # マップ上の座標を描画座標に変換してゴールを描画
 
# 移動先位置を現在の位置に設定（初期状態）
xnext = px
ynext = py
 
# 描画関数
def draw_map():
    # 壁を描画
    for y in range(5):
        for x in range(5):
            if map[y][x] == 1:
                screen.blit("bk_wall", (x*CSIZE, y*CSIZE))
            else:
                screen.blit("bk_road", (x*CSIZE, y*CSIZE))
     
    # キャラクタ描画
    player.draw()
    goal.draw()

    if status == STS.GAMECLEAR:
        screen.draw.text("GAME CLEAR !!", (100, 220), color=CL_WHITE, fontsize=32, fontname="notosansjp-medium")

 
# フレーム処理
def update():
    draw_map()  # マップを描画
 
# キーボードが押された時の処理
def on_key_down(key):
    global px, py, xnext, ynext
 
    # キー入力をチェック
    if key == keys.A:
        xnext -= 1  # 左
    elif key == keys.D:
        xnext += 1  # 右
    elif key == keys.W:
        ynext -= 1  # 上
    elif key == keys.S:
        ynext += 1  # 下
 
    # 移動先が壁かどうかチェック
    if check_wall():  # 壁である
        xnext = px
        ynext = py
    else:  # 壁でない
        px = xnext
        py = ynext
     
    # プレイヤーを移動先に描画
    player.left = xnext * CSIZE
    player.top = ynext * CSIZE
 
    # プレイヤーがゴールに接触したか
    if player.collidepoint(goal.pos):
        goal.pos = -100, -100
        print("ゲームクリア！")
        status = STS.GAMECLEAR


# 移動先が壁かどうかのチェック関数
def check_wall():
    if xnext < 0 or xnext >= len(map[0]) or ynext < 0 or ynext >= len(map):  # マップ外も壁と判定
        return True
    elif map[ynext][xnext] == 1:  # 壁
        return True
 
    return False  # 移動可能
 
# ゲームスタート
pgzrun.go()

