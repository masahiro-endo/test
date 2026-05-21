import asyncio

import pygame

# 関数---------------------------------------------------------------------------


# ボード盤面描画に関する処理
class BoardGrid:
    # 初期処理（コンストラクタ）
    def __init__(self):
        # マスの個数
        self.square_num = 8
        # ウィンドウの作成
        self.screen_width = 800
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        # 1マスの大きさ（// →切り捨て除算）
        self.square_size = self.screen_width // self.square_num
        # 色の設定
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 128, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)

        # フォントの設定
        self.font = pygame.font.SysFont(None, 100, bold=False, italic=False)

        self.black_win_surface = self.font.render(
            "Black Win!", False, self.BLACK, self.RED
        )
        self.white_win_surface = self.font.render(
            "White Win!", False, self.WHITE, self.RED
        )
        self.draw_surface = self.font.render("Draw...", False, self.BLUE, self.RED)
        self.reset_surface = self.font.render(
            "Click to reset!", False, self.BLACK, self.RED
        )

        # 盤面（黒：1、白：-1）8マス×8マス
        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, -1, 1, 0, 0, 0],
            [0, 0, 0, 1, -1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]

    # グリッド線の描画
    def draw_grid(self):
        # マス目分線引く
        for i in range(self.square_num):
            # 横線
            pygame.draw.line(
                self.screen,
                self.BLACK,
                (0, i * self.square_size),
                (self.screen_width, i * self.square_size),
                3,
            )
            # 縦線
            pygame.draw.line(
                self.screen,
                self.BLACK,
                (i * self.square_size, 0),
                (i * self.square_size, self.screen_height),
                3,
            )

    # 盤面の描画
    def draw_board(self):
        # 盤面全体のループ
        for row_index, row in enumerate(self.board):
            # 1行ずつループ
            for col_index, col in enumerate(row):
                # 黒だったら
                if col == 1:
                    pygame.draw.circle(
                        self.screen,
                        self.BLACK,
                        (
                            col_index * self.square_size + 50,
                            row_index * self.square_size + 50,
                        ),
                        45,
                    )
                # 白だったら
                elif col == -1:
                    pygame.draw.circle(
                        self.screen,
                        self.WHITE,
                        (
                            col_index * self.square_size + 50,
                            row_index * self.square_size + 50,
                        ),
                        45,
                    )


# プレイヤー操作に関するクラス
class PlayerOpe:
    # 初期処理（コンストラクタ）
    def __init__(self):
        # プレイヤー(最初は黒からスタート)
        self.player = 1
        # 自分から見た時の四方八方
        self.vec_table = [
            (-1, -1),  # 左上
            (0, -1),  # 上
            (1, -1),  # 右上
            (-1, 0),  # 左
            (1, 0),  # 右
            (-1, 1),  # 左下
            (0, 1),  # 下
            (1, 1),  # 右下
        ]

    # 石を置ける場所の取得
    def get_valid_positions(self, boardGrid):
        valid_position_list = []
        # 8回ループ
        for row in range(boardGrid.square_num):
            # 8回ループ
            for col in range(boardGrid.square_num):
                # 石を置いていないマスのみチェック
                if boardGrid.board[row][col] == 0:
                    for vx, vy in self.vec_table:
                        x = vx + col
                        y = vy + row
                        # マスの範囲内、かつプレイヤーの石と異なる石がある場合、その方向は引き続きチェック
                        if (
                            0 <= x < boardGrid.square_num
                            and 0 <= y < boardGrid.square_num
                            and boardGrid.board[y][x] == -self.player
                        ):
                            # どこかでbreakするまで永遠ループ
                            while True:
                                x += vx
                                y += vy
                                # プレイヤーの石と異なる色の石がある場合、その方向は引き続きチェック
                                if (
                                    0 <= x < boardGrid.square_num
                                    and 0 <= y < boardGrid.square_num
                                    and boardGrid.board[y][x] == -self.player
                                ):
                                    # 再度ループ続行
                                    continue
                                # プレイヤーの石と同色の石がある場合、石を置けるためインデックスを保存
                                elif (
                                    0 <= x < boardGrid.square_num
                                    and 0 <= y < boardGrid.square_num
                                    and boardGrid.board[y][x] == self.player
                                ):
                                    valid_position_list.append((col, row))
                                    break
                                else:
                                    break
        return valid_position_list

    # 石をひっくり返す
    def flip_pieces(self, col, row, boardGrid):
        for vx, vy in self.vec_table:
            flip_list = []
            x = vx + col
            y = vy + row
            while (
                0 <= x < boardGrid.square_num
                and 0 <= y < boardGrid.square_num
                and boardGrid.board[y][x] == -self.player
            ):
                flip_list.append((x, y))
                x += vx
                y += vy
                if (
                    0 <= x < boardGrid.square_num
                    and 0 <= y < boardGrid.square_num
                    and boardGrid.board[y][x] == self.player
                ):
                    for flip_x, flip_y in flip_list:
                        boardGrid.board[flip_y][flip_x] = self.player


# -------------------------------------------------------------------------------


# メインループ=======================================================================
def main():
    # async def main():
    pygame.init()
    pygame.display.set_caption("オセロ")

    # FPSの設定
    FPS = 60
    clock = pygame.time.Clock()
    game_over = False
    pass_num = 0

    boardGrid = BoardGrid()
    playerOpe = PlayerOpe()

    run = True
    while run:
        # 背景の塗りつぶし
        boardGrid.screen.fill(boardGrid.GREEN)
        # グリッド線の描画
        boardGrid.draw_grid()

        # 盤面の描画
        boardGrid.draw_board()

        # 石を置ける場所の取得
        valid_position_list = playerOpe.get_valid_positions(boardGrid)

        # 石を置ける場所の取得
        for x, y in valid_position_list:
            pygame.draw.circle(
                boardGrid.screen,
                boardGrid.YELLOW,
                (x * boardGrid.square_size + 50, y * boardGrid.square_size + 50),
                45,
                3,
            )

        # 石を置ける場所がない場合、パス
        if len(valid_position_list) < 1:
            playerOpe.player *= -1
            pass_num += 1

        # ゲームオーバー判定
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
                boardGrid.screen.blit(boardGrid.black_win_surface, (230, 200))
            elif black_num < white_num:
                boardGrid.screen.blit(boardGrid.white_win_surface, (230, 200))
            else:
                boardGrid.screen.blit(boardGrid.draw_surface, (280, 200))

            boardGrid.screen.blit(boardGrid.reset_surface, (180, 400))

        # イベントの取得
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            # マウスクリック
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over == False:
                    mx, my = pygame.mouse.get_pos()
                    x = mx // boardGrid.square_size
                    y = my // boardGrid.square_size
                    if boardGrid.board[y][x] == 0 and (x, y) in valid_position_list:
                        # 石をひっくり返す
                        playerOpe.flip_pieces(x, y, boardGrid)
                        boardGrid.board[y][x] = playerOpe.player
                        playerOpe.player *= -1
                        pass_num = 0

                else:
                    boardGrid.board = [
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, -1, 1, 0, 0, 0],
                        [0, 0, 0, 1, -1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                    ]
                    playerOpe.player = 1
                    game_over = False
                    pass_num = 0

        # 更新
        pygame.display.update()
        # await asyncio.sleep(0)
        clock.tick(FPS)


main()
# asyncio.run(main())

# ===============================================================================

pygame.quit()
