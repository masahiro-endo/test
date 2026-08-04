
import pyxel as px
from enum import Enum, IntEnum, auto



# ゲーム設定
WIDTH, HEIGHT = 80, 120
CELL_SIZE = 8
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
PUYO_COLORS = [px.COLOR_RED, 
               px.COLOR_GREEN, 
               px.COLOR_NAVY, 
               px.COLOR_YELLOW]  # 赤, 緑, 青, 黄
GRAVITY = 0.5


