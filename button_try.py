import pygame

# 初始化 Pygame
pygame.init()
DISPLAY = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
FPS = 60

# 初始化變數
start_game = False
running = True

# 定義按鈕類
class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        # 檢測滑鼠懸停與點擊
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        # 繪製按鈕
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

# 加載按鈕圖片
start_img = pygame.Surface((200, 80))
start_img.fill((0, 255, 0))  # 綠色按鈕
exit_img = pygame.Surface((200, 80))
exit_img.fill((255, 0, 0))  # 紅色按鈕

# 創建按鈕對象
start_button = Button(300, 250, start_img, 1)
exit_button = Button(300, 350, exit_img, 1)

# 遊戲主循環
while running:
    clock.tick(FPS)

    if not start_game:
        # 菜單畫面
        DISPLAY.fill((0, 0, 0))  # 黑色背景

        # 繪製按鈕
        if start_button.draw(DISPLAY):
            start_game = True  # 切換到遊戲狀態
        if exit_button.draw(DISPLAY):
            running = False  # 結束遊戲
    else:
        # 遊戲畫面
        DISPLAY.fill((50, 50, 150))  # 遊戲背景

        # 返回到主菜單（測試用）
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                start_game = False

    # 更新畫面
    pygame.display.update()

    # 檢測退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
