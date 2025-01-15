import pygame
import random

# 初始化 Pygame
pygame.init()

# 设置窗口大小
WIDTH, HEIGHT = 800, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game with Images")

# 加载图片
dino_img = pygame.image.load('./S__9945093_0.jpg')
dino_img = pygame.transform.scale(dino_img, (60, 60))  # 调整图片大小

obstacle_img = pygame.image.load('./S__9945098.jpg')
obstacle_img = pygame.transform.scale(obstacle_img, (40, 50))  # 调整图片大小

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 小恐龙属性
dino_width, dino_height = 60, 60
dino_x, dino_y = 50, HEIGHT - dino_height - 10
velocity = 5
is_jumping = False
jump_height = 20

# 障碍物属性
obstacle_width, obstacle_height = 50, 50
obstacle_x = WIDTH
obstacle_y = HEIGHT - obstacle_height - 10
obstacle_speed = 5

# 游戏时钟
clock = pygame.time.Clock()

# 游戏主循环
running = True
score = 0
while running:
    clock.tick(30)
    win.fill(WHITE)

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 控制跳跃
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True

    if is_jumping:
        dino_y -= jump_height
        jump_height -= 1
        if jump_height < -20:
            is_jumping = False
            jump_height = 20

    # 移动障碍物
    obstacle_x -= obstacle_speed
    if obstacle_x < -obstacle_width:
        obstacle_x = WIDTH
        score += 1  # 增加分数

    # 检测碰撞
    dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

    if dino_rect.colliderect(obstacle_rect):
        print("Game Over!")
        print(f"Your Score: {score}")
        running = False

    # 绘制恐龙和障碍物图片
    win.blit(dino_img, (dino_x, dino_y))
    win.blit(obstacle_img, (obstacle_x, obstacle_y))

    # 显示分数
    font = pygame.font.SysFont("comicsans", 30)
    score_text = font.render(f"Score: {score}", True, BLACK)
    win.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()