import pygame
import random

class BoardGrid:
    def __init__(self):
        # 変数を定義
        self.square_num = 20
        self.screen_width = 1000
        self.screen_height = 1000
        
        #爆弾数
        self.bomb_count = 15
        #旗の数は爆弾数 + 2とする
        self.flag_count = self.bomb_count + 2

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        #１マスの大きさ(50)
        self.suqare_size = self.screen_width // self.square_num
        #色
        self.BLACK = (0,0,0)
        self.GREY = (192,192,192)
        self.SNOW=(255,250,250)
        self.MOCA=(255,228,181)
        self.WHITE = (255,255,255)
        self.RED = (255,0,0)
        self.GREEN = (0,128,0)
        self.BLUE = (0,0,255)
        self.YELLOW = (255,255,0)

        # TODO
        self.font = pygame.font.SysFont(None, 100)
        self.font2 = pygame.font.SysFont(None, 40)

        self.success = self.font.render("SUCCESS!!", False, self.BLACK, self.GREEN)
        self.lose = self.font.render("LOSE....", False, self.WHITE, self.RED)
        self.drow = self.font.render("引き分け！", False, self.BLUE, self.RED)
        self.restart = self.font.render("リスタート", False, self.BLUE, self.RED)

        # 盤面作成
        self.board =self.init_board(self.bomb_count)
    
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
    # 盤面内の描画を行う
    # 爆弾：-1、何もなし：-2、爆弾表示用：21、クック後の数値：0～8、旗表示用:9～10
    def draw_board(self):
        for row_index, row in enumerate(self.board):
            for col_index,col in enumerate(row):
                # 周りの地雷数が１より大きいとき
                if col >=  0 and col <=8:
                    pygame.draw.rect(self.screen, self.SNOW, (col_index * self.suqare_size, row_index* self.suqare_size, 50, 50))
                    text =  self.font2.render(str(col), True, self.BLACK) 
                    self.screen.blit(text, [col_index * self.suqare_size + 15,  row_index* self.suqare_size+10])
                #爆弾を描画
                elif col == 21:
                    img1 = pygame.image.load("bomb.png")
                    img1 = pygame.transform.scale(img1, (50, 50)) #200 * 130に画像を縮小
                    self.screen.blit(img1, [col_index * self.suqare_size ,  row_index* self.suqare_size])
                # 旗を描画
                elif col == 10 or col == 9:
                    img1 = pygame.image.load("flag.png")
                    img1 = pygame.transform.scale(img1, (50, 50)) #200 * 130に画像を縮小
                    self.screen.blit(img1, [col_index * self.suqare_size ,  row_index* self.suqare_size])
    
    # 爆弾と旗の数を描画する
    def draw_bomb_flag_count(self):
        bomb_msg =  "Bomb: " + str(self.bomb_count)
        bomb_txt =  self.font2.render(bomb_msg, True, self.RED) 
        self.screen.blit(bomb_txt, [2 , 0])

        usage_flag_count = 0
        # 現在使用された旗をカウント
        for i in self.board:
            usage_flag_count += (i.count(10) + i.count(9))
        #残りの旗を表示
        flag_msg =  "Flag: " + str(self.flag_count - usage_flag_count)
        flag_txt =  self.font2.render(flag_msg, True, self.GREEN) 
        self.screen.blit(flag_txt, [150 , 0])

    
    def init_board(self, bombCount):
        board = []

        # 二次元配列を作成
        for row in range(self.square_num):
            boardChild = []
            for col in range(self.square_num):
                boardChild.append(-2)
            board.append(boardChild)
        
        # 地雷を埋め込む(地雷:-1、何もなし：-2)
        while bombCount > 0: 
            # 地雷の位置をランダムに決定
            j = random.randint(0, self.square_num - 1)
            i = random.randint(0, self.square_num - 1)

            if board[i][j] != -1:
                # まだ地雷が設定されていなければ、地雷(-1)を設置
                board[i][j] = -1
                bombCount -=1
        return board


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

    # クリックした箇所が地雷かどうか判別
    def check_bomb(self, boardGrid, mx, my):
        if boardGrid.board[my][mx] == -1:
            return True
        else:
            return False
        

    
    # クリックしたところの周りの地雷数をカウント
    def search_inspector(self, boardGrid, mx, my):
        bomb_count = 0
        for vx, vy in self.vec_table:
            x = vx + mx
            y = vy + my
            if(0<= x < boardGrid.square_num
                and 0 <= y < boardGrid.square_num
                and (boardGrid.board[y][x] == -1 or (boardGrid.board[y][x] -11) == -1)):
                # 盤面の枠内かつ、地雷の場所ならカウントアップ
                # 旗が立っているマスが爆弾であった場合を考慮する
                bomb_count += 1

        return bomb_count    

    # 指定された場所の周りをオープンする
    def open(self, boardGrid, mx, my):
        for vx, vy in self.vec_table:
            x = vx + mx
            y = vy + my
            if(0<= x < boardGrid.square_num
                and 0 <= y < boardGrid.square_num
                and boardGrid.board[y][x] == -2):
                # 盤面の枠内かつ、まだ未オープンの個所ならばオープンにする
                cnt = Play.search_inspector(self=self,boardGrid=boardGrid,mx=x, my=y)
                boardGrid.board[y][x] = cnt    

def checkJudge(board):
    #ゲームクリアしたかどうかを判定
    unOpen = 0
    for i in board:
        unOpen += i.count(-2)
    if unOpen  == 0:
        return True
    else:
        return False


def main():
    pygame.init()
    pygame.display.set_caption("マインスイーパー")

    # 定数
    FPS = 60
    clock = pygame.time.Clock()
    LEFT = 1
    RIGHT = 3


    game_over = False
    game_success = False

    boardGrid = BoardGrid()
    play = Play()

    run = True
    while run:
        boardGrid.screen.fill(boardGrid.GREY)
        boardGrid.draw_grid()
        boardGrid.draw_board()
        boardGrid.draw_bomb_flag_count()

        #ゲームオーバー時の処理
        if game_over:
            #失敗のメッセージ表示
            boardGrid.screen.blit(boardGrid.lose,(230,200))
        if game_success:
            #成功時のメッセージ表示
            boardGrid.screen.blit(boardGrid.success,(230,200))



        # イベント処理
        for evet in pygame.event.get():
            if evet.type == pygame.QUIT:
                run = False
            
            # クリックされたとき
            if evet.type == pygame.MOUSEBUTTONDOWN:
                mx, my =pygame.mouse.get_pos()
                x = mx // boardGrid.suqare_size
                y = my // boardGrid.suqare_size
                print(f'{x}、{y}')

                if game_over or game_success:
                    #ゲームオーバーまたは成功の場合、再スタート
                    game_over = False
                    game_success = False
                    # ボード再作成（初期化）
                    boardGrid = BoardGrid()
                else:
                    if boardGrid.board[y][x] >= 0:
                        # 既にクリックされている個所の場合、スキップ
                        continue


                    # 左クリックされたとき
                    if evet.button == LEFT:
                        # 地雷かどうか判別
                        if play.check_bomb(boardGrid, x, y):
                            # 地雷なら終了
                            game_over = True
                            print("OUT!!!!!")

                            #爆弾設定(爆弾:21)
                            #boardGrid.board[y][x] = 21

                            # すべての爆弾を表示する
                            for row_index, row in enumerate(boardGrid.board):
                                for col_index,col in enumerate(row):
                                    if col == -1:
                                        boardGrid.board[row_index][col_index] = 21


                           

                            
                        else:
                            # 地雷でなければ周りの地雷数取得して、設定
                            count = play.search_inspector(boardGrid, x, y)
                            print(count)
                            # 0～8のどれか
                            boardGrid.board[y][x] = count

                            if count == 0:
                                #数字0の場合、周りの個所もオープンする
                                play.open(boardGrid, x, y)
                           
                
                    # 右クリックの場合は旗を立てる(旗:9～10)
                    elif evet.button == RIGHT:

                        # 残りの旗数をチェック
                        
                        usage_flag_count = 0
                        # 現在使用された旗をカウント
                        for i in boardGrid.board:
                            usage_flag_count += (i.count(10) + i.count(9)) 
                        if boardGrid.flag_count > usage_flag_count:
                            # まだ旗が残っていたら旗を設定
                            boardGrid.board[y][x] =  boardGrid.board[y][x] + 11
                    
                    #ゲームクリアしたかどうかを判定
                    if checkJudge(boardGrid.board):
                        game_success = True



        pygame.display.update()
        clock.tick(FPS)


main()

