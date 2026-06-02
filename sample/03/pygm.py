import pygame
import sys




# 初期化
pygame.init()

# 画面サイズ
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball Simulation")

# 色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 物理パラメータ
gravity = 0.5          # 重力加速度
bounciness = 0.6       # 反発係数（1.0で完全反発、0で反発なし）
friction = 0.99        # 摩擦係数（横方向の減速）

# ボールの初期状態
ball_radius = 30
ball_x = WIDTH // 2
ball_y = 100
ball_vx = 3
ball_vy = 0

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 重力適用
    ball_vy += gravity

    # 位置更新
    ball_x += ball_vx
    ball_y += ball_vy

    # 床との衝突判定
    if ball_y + ball_radius > HEIGHT:
        ball_y = HEIGHT - ball_radius
        ball_vy = -ball_vy * bounciness  # 反発
        ball_vx *= friction              # 摩擦で横速度減衰

    # 壁との衝突判定
    if ball_x - ball_radius < 0 or ball_x + ball_radius > WIDTH:
        ball_vx = -ball_vx * bounciness

    # 描画
    screen.fill(BLACK)
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)
    pygame.display.flip()

    clock.tick(60)
