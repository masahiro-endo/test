import pygame
import random
class BoardGrid:
    def __init__(self):
        # 変数を定義
        self.square_num = 20
        self.screen_width = 800
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        # 1マスの大きさ
        self.square_size = self.screen_width // self.square_num
        # 色
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.RED = (255,0,0)
        self.GREEN = (0,128,0)
        self.BLUE = (0,0,255)
        self.YELLOW = (255,255,0)
        self.DODGER_BLUE = (30,144,255)
        self.DEEP_SKY_BLUE = (0,191,255)
        self.font = pygame.font.SysFont(None, 32)
        self.font_finish = pygame.font.SysFont(None, 120)
        self.game_over = self.font_finish.render("GAME OVER", False, self.RED, self.BLACK)
        self.clear = self.font_finish.render("CLEAR!", False, self.YELLOW, self.BLUE)
        self.restart = self.font.render("RESTART", False, self.BLUE, self.YELLOW)
        self.board = [[-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                      [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2]]
        # ランダム設定
        self.random = 1 #self.square_num * self.square_num // 8
        #self.random = 1
        while self.random > 0:
            j = random.randint(0, self.square_num - 1)
            l = random.randint(0, self.square_num - 1)
            if self.board[j][l] == -2:
                self.board[j][l] = -1
                self.random -= 1
        print(j)
        print(self.board)
    def draw_grid(self):
        for i in range(self.square_num):
            # 横線
            pygame.draw.line(self.screen,
                             self.DODGER_BLUE,
                             (0, i * self.square_size),
                             (self.screen_width, i * self.square_size),
                             2
                             )
            # 縦線
            pygame.draw.line(self.screen,
                             self.DODGER_BLUE,
                             (i * self.square_size, 0),
                             (i * self.square_size, self.screen_width),
                             2
                             )
    def draw_board(self):
        for row_index, row in enumerate(self.board):
            for col_index, col in enumerate(row):
                if 0 <= col <= 8:
                # number
                    pygame.draw.rect(
                    self.screen,
                    self.GREEN,
                    (col_index * self.square_size,
                    row_index * self.square_size,
                    40,
                    40)
                    )
                    text = self.font.render(str(col), True, self.YELLOW)
                    self.screen.blit(text, [col_index * self.square_size + 15, row_index * self.square_size + 10])
                if col == -3:
                    # TODO：エラーあり                    
                    pygame.draw.rect(
                    self.screen,
                    self.RED,
                    (col_index * self.square_size,
                    row_index * self.square_size,
                    40,
                    40)
                    )
                    img1 = pygame.image.load("bomb.png")
                    img1_2 = pygame.transform.scale(img1,(40,40))
                    self.screen.blit(img1_2,[col_index * self.square_size,row_index * self.square_size])
                #旗
                if -5 <= col <= -4:
                    img2 = pygame.image.load("flag.png")
                    img2_2 = pygame.transform.scale(img2,(40,40))
                    self.screen.blit(img2_2,[col_index * self.square_size,row_index * self.square_size])
class Play:
    def __init__(self):
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

        self.flag_count = 0

    def flip_pieces(self, col, row, boardGrid):
        print(col)
        print(row)
        bomb_list = 0
        for vx, vy in self.vec_table:
            x = vx + col
            y = vy + row
            if (0<= x < boardGrid.square_num
                and 0 <= y < boardGrid.square_num
                and (boardGrid.board[y][x] == -1 or boardGrid.board[y][x] == -4)):
                bomb_list += 1
        print (bomb_list)
        if boardGrid.board[row][col] == -2:
            boardGrid.board[row][col] = bomb_list
            return False
        elif boardGrid.board[row][col] == -1:
            boardGrid.board[row][col] = -3
            for row_index, row in enumerate(boardGrid.board):
                for col_index, col in enumerate(row):
                    if boardGrid.board[row_index][col_index] == -1:
                        boardGrid.board[row_index][col_index] = -3
            return True
    
    def auto_open(self, boardGrid, mx, my):
        for vx, vy in self.vec_table:
            x = vx + mx
            y = vy + my
            if(0 <= x < boardGrid.square_num
               and 0 <= y < boardGrid.square_num
               and boardGrid.board[y][x] == -2):
                #盤面のなかかつ、未オープンなら開く
                self.flip_pieces(x, y, boardGrid)

    def flag(self, boardGrid, x, y):
        if(0 <= x < boardGrid.square_num
            and 0 <= y < boardGrid.square_num):
            max = boardGrid.square_num * boardGrid.square_num // 8
            if boardGrid.board[y][x] == -2 or boardGrid.board[y][x] == -1:
                if 0 <= self.flag_count < max:
                    if boardGrid.board[y][x] == -2:
                        boardGrid.board[y][x] = -5
                        self.flag_count += 1
                    elif boardGrid.board[y][x] == -1:
                        boardGrid.board[y][x] = -4
                        self.flag_count += 1
            else:
                if 0 < self.flag_count <= max:
                    if boardGrid.board[y][x] == -5:
                        boardGrid.board[y][x] = -2
                        self.flag_count += -1
                    elif boardGrid.board[y][x] == -4:
                        boardGrid.board[y][x] = -1
                        self.flag_count += -1

def main():
    pygame.init()
    pygame.display.set_caption("マインスイーパー")
    # 定数
    FPS = 60
    clock = pygame.time.Clock()
    game_over = False
    clear = False
    run = True
    boardGrid = BoardGrid()
    play = Play()
    count_check = 0
    left = 1
    right = 3
    while run:
        boardGrid.screen.fill(boardGrid.DEEP_SKY_BLUE)
        boardGrid.draw_grid()
        boardGrid.draw_board()        
        if game_over:
            boardGrid.screen.blit(boardGrid.game_over, (200,200))
        if clear:
            boardGrid.screen.blit(boardGrid.clear, (200,200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                # K_キー名
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                #左クリック
                if event.button == left:
                    if game_over == False and clear == False:
                        mx, my = pygame.mouse.get_pos()
                        x = mx // boardGrid.square_size
                        y = my // boardGrid.square_size
                        if boardGrid.board[y][x] == -1 or boardGrid.board[y][x] == -2:  #まだひっくり返してない                      
                            game_over = play.flip_pieces(x, y, boardGrid)
                            #もし結果が0だったら周りも開く
                            if game_over == False and boardGrid.board[y][x] == 0:
                                play.auto_open(boardGrid, x, y)
                            #クリア条件
                            count_check = 0
                            for row_index, row in enumerate(boardGrid.board):
                                for col_index, col in enumerate(row):
                                    if boardGrid.board[row_index][col_index] != -2 and boardGrid.board[row_index][col_index] != -5:
                                        count_check += 1
                            if count_check == 400:
                                clear = True
                    else:
                        boardGrid.board = [[-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2],
                                        [-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2]]
                        boardGrid.random = boardGrid.square_num * boardGrid.square_num // 8
                        while boardGrid.random > 0:
                            j = random.randint(0, boardGrid.square_num - 1)
                            l = random.randint(0, boardGrid.square_num - 1)
                            if boardGrid.board[j][l] == -2:
                                boardGrid.board[j][l] = -1
                                boardGrid.random -= 1
                        game_over = False
                        clear = False
                        play.flag_count = 0
                #右クリック
                elif event.button == right:
                    if game_over == False and clear == False:
                        mx, my = pygame.mouse.get_pos()
                        x = mx // boardGrid.square_size
                        y = my // boardGrid.square_size
                        #if boardGrid.board[y][x] == -1 or boardGrid.board[y][x] == -2:  #まだひっくり返してない 
                        play.flag(boardGrid, x, y)
        pygame.display.update()
        clock.tick(FPS)
main()