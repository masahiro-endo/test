import pygame
import numpy as np
import random

# 定数の定義
BOARD_SIZE = 8
CELL_SIZE = 60
INFO_WIDTH = 150  # スコア表示用のスペース
SCREEN_WIDTH = BOARD_SIZE * CELL_SIZE + INFO_WIDTH
SCREEN_HEIGHT = BOARD_SIZE * CELL_SIZE

EMPTY, BLACK, WHITE = 0, 1, 2
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),         (0, 1),
              (1, -1), (1, 0), (1, 1)]

# 色の定義
GREEN = (34, 139, 34)
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (200, 200, 200, 128)  # 半透明のハイライト
TEXT_COLOR = (255, 255, 255)  # スコアの文字色
BG_COLOR = (50, 50, 50)  # スコア表示の背景色

# AIの種類
AI_NONE = 0
AI_RANDOM = 1
AI_MINIMAX = 2

class OthelloGame:
    def __init__(self, ai_type=AI_NONE):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.board[3, 3], self.board[4, 4] = WHITE, WHITE
        self.board[3, 4], self.board[4, 3] = BLACK, BLACK
        self.current_player = BLACK
        self.running = True
        self.ai_type = ai_type  # AIの種類
        self.ai_player = WHITE if ai_type != AI_NONE else None  # AIは白

    def is_valid_move(self, row, col):
        if self.board[row, col] != EMPTY:
            return False
        for dr, dc in DIRECTIONS:
            if self._can_flip(row, col, dr, dc):
                return True
        return False

    def _can_flip(self, row, col, dr, dc):
        opponent = WHITE if self.current_player == BLACK else BLACK
        r, c = row + dr, col + dc
        flipped = False

        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r, c] == opponent:
            r += dr
            c += dc
            flipped = True
        
        if flipped and 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r, c] == self.current_player:
            return True
        return False

    def place_piece(self, row, col):
        if not self.is_valid_move(row, col):
            return False
        self.board[row, col] = self.current_player
        for dr, dc in DIRECTIONS:
            self._flip_pieces(row, col, dr, dc)
        self.current_player = WHITE if self.current_player == BLACK else BLACK
        return True

    def _flip_pieces(self, row, col, dr, dc):
        opponent = WHITE if self.current_player == BLACK else BLACK
        r, c = row + dr, col + dc
        pieces_to_flip = []

        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r, c] == opponent:
            pieces_to_flip.append((r, c))
            r += dr
            c += dc
        
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r, c] == self.current_player:
            for r, c in pieces_to_flip:
                self.board[r, c] = self.current_player

    def has_valid_moves(self):
        return any(self.is_valid_move(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE))

    def get_valid_moves(self):
        return [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.is_valid_move(r, c)]

    def check_game_over(self):
        if not self.has_valid_moves():
            self.current_player = WHITE if self.current_player == BLACK else BLACK
            if not self.has_valid_moves():
                self.running = False

    def get_winner(self):
        black_score, white_score = np.sum(self.board == BLACK), np.sum(self.board == WHITE)
        return "Black Wins!" if black_score > white_score else "White Wins!" if white_score > black_score else "It's a Draw!"

    def get_scores(self):
        return np.sum(self.board == BLACK), np.sum(self.board == WHITE)

    def ai_move(self):
        if self.ai_player != self.current_player:
            return

        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return

        if self.ai_type == AI_RANDOM:
            move = random.choice(valid_moves)
        elif self.ai_type == AI_MINIMAX:
            move = self.minimax_move()
        else:
            return

        self.place_piece(*move)

    def minimax_move(self):
        """簡易Minimax: 1手先を読んで石が増える手を選択"""
        valid_moves = self.get_valid_moves()
        best_move = max(valid_moves, key=lambda move: self.simulate_move(move), default=random.choice(valid_moves))
        return best_move

    def simulate_move(self, move):
        temp_game = OthelloGame()
        temp_game.board = np.copy(self.board)
        temp_game.current_player = self.current_player
        temp_game.place_piece(*move)
        return np.sum(temp_game.board == self.current_player)

def draw_board(screen, game, font):
    screen.fill(GREEN)

    for i in range(1, BOARD_SIZE):
        pygame.draw.line(screen, BLACK_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT), 2)
        pygame.draw.line(screen, BLACK_COLOR, (0, i * CELL_SIZE), (SCREEN_HEIGHT, i * CELL_SIZE), 2)

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if game.board[r, c] == BLACK:
                pygame.draw.circle(screen, BLACK_COLOR, (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
            elif game.board[r, c] == WHITE:
                pygame.draw.circle(screen, WHITE_COLOR, (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

    pygame.draw.rect(screen, BG_COLOR, (BOARD_SIZE * CELL_SIZE, 0, INFO_WIDTH, SCREEN_HEIGHT))

    black_score, white_score = game.get_scores()
    screen.blit(font.render(f"Black: {black_score}", True, TEXT_COLOR), (BOARD_SIZE * CELL_SIZE + 20, 50))
    screen.blit(font.render(f"White: {white_score}", True, TEXT_COLOR), (BOARD_SIZE * CELL_SIZE + 20, 100))




def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("オセロ - モード選択")
    font = pygame.font.Font(None, 36)
    
    mode = int(input("モード選択 (0: 二人対戦, 1: ランダムAI, 2: Minimax AI) → "))
    game = OthelloGame(ai_type=mode)

    while game.running:
        game.ai_move()
        draw_board(screen, game, font)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                row, col = pygame.mouse.get_pos()[1] // CELL_SIZE, pygame.mouse.get_pos()[0] // CELL_SIZE
                if game.place_piece(row, col):
                    game.check_game_over()

    print(game.get_winner())
    pygame.quit()





if __name__ == "__main__":
    main()


