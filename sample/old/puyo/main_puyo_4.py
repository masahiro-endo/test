
import pyxel as px
import random

from constant import *
import appconfig as gbl
from scenestate import SceneStates
from actor import *









class ViewModel:
    def __init__(self):
        self.state = SceneStates(self)
        self.reset()

    def reset(self):
        gbl.field = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        gbl.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.spawn_puyo()
        self.game_over = False
        self.state = SceneStates(self)
        self.chain_count = 0
        self.clear_list = []

    def spawn_puyo(self):
        color1 = random.choice(PUYO_COLORS)
        color2 = random.choice(PUYO_COLORS)
        gbl.puyo  = [(COLS // 2, 0, color1), (COLS // 2, 1, color2)]
        gbl.puyoc = [Puyo(self, gbl.puyo[0]), Puyo(self, gbl.puyo[1])]
        if Meth.is_collision(0, 0):
            self.game_over = True


    def update(self):
        if self.game_over:
            if px.btnp(px.KEY_R):
                self.reset()
            return
        self.state.update()


    def check_and_clear(self):

        to_clear = Meth.find_4puyos_toclear()
        if to_clear:
            self.clear_list = to_clear
            self.state.Clear()
            self.chain_count += 1
        else:
            if self.chain_count > 0:
                print(f"{self.chain_count} 連鎖!")
            if Meth.board_is_droping():
                return
            self.spawn_puyo()
            self.state.Play()





class AppView:
    def __init__(self, ViewModel):
        self.vm = ViewModel

        px.init(WIDTH, HEIGHT, title="Puyo Demo")
        px.load("assets_puyo.pyxres")
        px.run(self.update, self.draw)

    def update(self):
        self.vm.update()

    def draw(self):
        px.cls(px.COLOR_BLACK)

        self.draw_board()
        self.vm.state.draw()

        # ゲームオーバー表示
        if self.vm.game_over:
            px.text(WIDTH // 2 - 16, HEIGHT // 2, "GAME OVER", 7)
            px.text(WIDTH // 2 - 20, HEIGHT // 2 + 10, "Press R to Restart", 7)

        # 連鎖数表示
        if self.vm.chain_count > 0:
            px.text(2, 2, f"{self.vm.chain_count} RENSA!", 7)

    def draw_board(self):
        for y in range(ROWS):
            for x in range(COLS):
                if gbl.board[y][x]:
                    gbl.board[y][x].draw()





if __name__ == "__main__":
    vm = ViewModel()
    AppView(vm)



