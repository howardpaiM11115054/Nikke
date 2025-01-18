import pygame
class Button():
    def __init__(self,x,y,image,scale):
        width=image.get_width()
        height=image.get_height()
        self.image=pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.clicked=False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        # 檢查滑鼠懸停狀態
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked :
                action = True
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        # 無論是否滑鼠懸停，都需要繪製按鈕
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
