import pygame
import random
class BoardGrid:
    def __init__(self):
        # 変数を定義
        self.square_num = 8 
        self.screen_width = 800
        self.screen_height = 800

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        #１マスの大きさ
        self.suqare_size = self.screen_width // self.square_num
        #色
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.RED = (255,0,0)
        self.GREEN = (0,128,0)
        self.BLUE = (0,0,255)
        self.YELLOW = (255,255,0)

        self.font = pygame.font.SysFont(None, 100)
        self.win_black = self.font.render("黒が勝ったよ！", False, self.BLACK, self.RED)
        self.win_white = self.font.render("白が勝ったよ！", False, self.WHITE, self.RED)
        self.drow = self.font.render("引き分け！", False, self.BLUE, self.RED)
        self.restart = self.font.render("リスタート", False, self.BLUE, self.RED)

        # 黒：1、白：-1　8×8マス
        self.board =[[0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,-1,1,0,0,0],
                     [0,0,0,1,-1,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0]]
    
    def draw_grid(self):
        for i in range(self.square_num):
            # 横線
            pygame.draw.line(self.screen,
                              self.BLACK,
                              (0, i * self.suqare_size),
                              (self.screen_width, i * self.suqare_size),
                              3
                                )
            # 縦線
            pygame.draw.line(self.screen,
                              self.BLACK,
                              ( i * self.suqare_size, 0),
                              (i * self.suqare_size, self.screen_height),
                              3
                                )
    def draw_board(self):
        for row_index, row in enumerate(self.board):
            for col_index,col in enumerate(row):
                # 黒の時
                if col == 1:
                    pygame.draw.circle(
                        self.screen,
                        self.BLACK,
                        (col_index * self.suqare_size + 50,
                         row_index* self.suqare_size + 50),
                         45
                    )
                # 白の時
                elif col == -1:
                    pygame.draw.circle(
                        self.screen,
                        self.WHITE,
                        (col_index * self.suqare_size + 50,
                         row_index* self.suqare_size + 50),
                         45
                    )

class Play:
    def __init__(self):
        self.player = 1 #黒スタート
        self.vec_table = [
            (-1,-1), 
            (0,-1),
            (1,-1),
            (-1,0),
            (1,0),
            (-1,1),
            (0,1),
            (1,1)
        ]
    
    # 石をおける場所を取得
    def get_valid_positions(self,boardGrid):
        valid_position_list = []
        for row in range(boardGrid.square_num):
            for col in range(boardGrid.square_num):
                if boardGrid.board[row][col]==0:
                    for vx, vy in self.vec_table:
                        x = vx + col
                        y = vy + row
                        if(0<= x < boardGrid.square_num
                           and 0 <= y < boardGrid.square_num
                           and boardGrid.board[y][x] == -self.player):
                            while True:
                                x += vx
                                y += vy
                                if(0<= x < boardGrid.square_num
                                    and 0 <= y < boardGrid.square_num
                                    and boardGrid.board[y][x] == -self.player):
                                    continue
                                elif(0<= x < boardGrid.square_num
                                    and 0 <= y < boardGrid.square_num
                                    and boardGrid.board[y][x] == self.player):
                                    valid_position_list.append((col,row))
                                    break
                                else:
                                    break
        return valid_position_list            
    
    def flip_pieces(self, col, row, boardGrid):
        for vx, vy in self.vec_table:
            flip_list = []
            x = vx + col
            y = vy + row
            while(0<= x < boardGrid.square_num
                    and 0 <= y < boardGrid.square_num
                    and boardGrid.board[y][x] == -self.player):
                flip_list.append((x,y))
                x += vx
                y += vy
                if(0<= x < boardGrid.square_num
                    and 0 <= y < boardGrid.square_num
                    and boardGrid.board[y][x] == self.player):
                    for flip_x, flip_y in flip_list:
                        boardGrid.board[flip_y][flip_x] = self.player



def main():
    pygame.init()
    pygame.display.set_caption("オセロ")

    # 定数
    FPS = 60
    clock = pygame.time.Clock()

    game_over = False
    pass_num =  0
    run = True

    boardGrid = BoardGrid()
    play = Play()

    while run:
        boardGrid.screen.fill(boardGrid.GREEN)
        boardGrid.draw_grid()
        boardGrid.draw_board()

        valid_position_list = play.get_valid_positions(boardGrid)
        for x,y in valid_position_list:
            pygame.draw.circle(
                boardGrid.screen,
                boardGrid.YELLOW,
                (
                    x * boardGrid.suqare_size + 50,
                    y *  boardGrid.suqare_size + 50,
                ),
                45,
            )
        
        if len(valid_position_list) < 1:
            play.player *= -1
            pass_num += 1
        
        if pass_num > 1:
            pass_num = 2
            game_over = True
        
        # 勝敗チェック
        black_num = 0
        white_num = 0
        if game_over:
            black_num = sum(row.count(1) for row in boardGrid.board)
            white_num = sum(row.count(-1) for row in boardGrid.board)
            if black_num > white_num:
                boardGrid.screen.blit(boardGrid.win_black,(230,200))
            elif white_num > black_num:
                boardGrid.screen.blit(boardGrid.win_white,(230,200))
            else:
                boardGrid.screen.blit(boardGrid.drow,(230,200))
            
            boardGrid.screen.blit(boardGrid.restart,(180,400))

        
        if play.player == -1:
            
            x, y =valid_position_list[1]
            # 石をひっくり返す
            play.flip_pieces(x, y, boardGrid)
            boardGrid.board[y][x] = play.player
            play.player *= -1
            pass_num = 0



        for evet in pygame.event.get():
            if evet.type == pygame.QUIT:
                run = False
            elif evet.type == pygame.KEYDOWN:
                if evet.key == pygame.K_ESCAPE:
                    run = False
            
            # マウスがクリックされたとき
            if evet.type == pygame.MOUSEBUTTONDOWN:
                if game_over == False:
                    mx, my =pygame.mouse.get_pos()
                    x = mx // boardGrid.suqare_size
                    y = my // boardGrid.suqare_size
                    if boardGrid.board[y][x] == 0 and (x,y) in valid_position_list:
                        # 石をひっくり返す
                        play.flip_pieces(x, y, boardGrid)
                        boardGrid.board[y][x] = play.player
                        play.player *= -1
                        pass_num = 0
                        
                else:
                    boardGrid.board =[
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,-1,1,0,0,0],
                     [0,0,0,1,-1,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0]]
                    play.player = 1
                    game_over = False
                    pass_num = 0


        pygame.display.update()
        clock.tick(FPS)


main()