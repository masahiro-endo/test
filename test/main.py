import pgzrun
 
# 画面サイズ
WIDTH = 640
HEIGHT = 512
TITLE = "2次元リストで迷路を描画する"
LENGTH = 64
RED = 200, 0, 0


# プレイヤーを生成
player = Actor("player")
player.topleft = 1*LENGTH, 1*LENGTH
 
# 迷路データ
map_dungeon = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
 
def set_background():
    screen.fill(RED)


# 描画処理
def draw():
    # 3秒後にset_background関数を呼び出す
    clock.schedule_unique(set_background, 3)
    
    # 迷路を描画
    for y in range(8):
        for x in range(10):
            if map_dungeon[y][x] == 1:
                screen.blit("bk_wall", (x*LENGTH, y*LENGTH))
            else:
                screen.blit("bk_road", (x*LENGTH, y*LENGTH))
     
    # プレイヤーを描画
    player.draw()
 

def on_key_down(key):
    # UPPERCASE
    if key == keys.RIGHT:
        player.left += LENGTH
    if key == keys.LEFT:
        player.left -= LENGTH

def update():
    # LOWERCASE
    if keyboard.right:
        player.left += LENGTH
    if keyboard.left:
        player.left -= LENGTH


# ゲームスタート
pgzrun.go()


