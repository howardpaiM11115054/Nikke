import pygame, sys
import os
import random
pygame.init()
#set time
clock=pygame.time.Clock()
FPS=60

#game vel
GARVITY=0.75
TILE_SIZE= 20# 接觸居離
#display size
DISPLAY = pygame.display.set_mode((800,600))

pygame.display.set_caption("damo")
#背景顏色
DISPLAY.fill((0,0,0))
def click():
    pygame.quit()
    sys.exit()
#def player activate
movie_left=False
movie_right=False
shoot=False
grenade=False
grenade_thrown=False
#load image
bullet_img=pygame.image.load("./img/bullet/bullet.png").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img,(int((bullet_img.get_height())*0.5),int(bullet_img.get_width()*0.5)))
grenade_img=pygame.image.load("./img/grenade/00.png").convert_alpha()
grenade_img = pygame.transform.scale(grenade_img,(int((grenade_img.get_height()*0.7)),int(grenade_img.get_width()*0.7)))
HPbox_img=pygame.image.load("./img/box/HPbox/00.png").convert_alpha()
HPbox_img = pygame.transform.scale(HPbox_img,(int((HPbox_img.get_height()*0.5)),int(HPbox_img.get_width()*0.5)))
bulletbox_img=pygame.image.load("./img/box/bulletbox/00.png").convert_alpha()
bulletbox_img = pygame.transform.scale(bulletbox_img,(int((bulletbox_img.get_height()*0.5)),int(bulletbox_img.get_width()*0.5)))
grenadebox_img=pygame.image.load("./img/box/grenadebox/00.png").convert_alpha()
grenadebox_img = pygame.transform.scale(grenadebox_img,(int((grenadebox_img.get_height()*0.5)),int(grenadebox_img.get_width()*0.5)))
item_boxes={
    'health':HPbox_img,
    'bullet':bulletbox_img,
    'grenade':grenadebox_img
}
#def color
BG=(50,40,60)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLACK=(0,0,0)

font =pygame.font.SysFont('Futura',30)
def draw_text(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    DISPLAY.blit(img,(x,y))

#更新背景
def draw_bg():
    DISPLAY.fill(BG)
    pygame.draw.line(DISPLAY,RED,(0,500),(800,500))
class human(pygame.sprite.Sprite):
    def __init__(self,character,x,y,size,speed,ammo,health,grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive=True
        self.character=character
        self.speed=speed
        self.ammo=ammo
        self.grenades=grenades
        self.health=health
        self.max_health=self.health
        self.start_ammo=ammo
        self.shoot_cooldown=0
        self.direction=1
        self.vel_y =0
        self.jump=False
        self.in_air=False
        self.flip=False
        self.animation_list=[]
        self.index=0
        self.run_index=0
        self.update_time=pygame.time.get_ticks()
        temp_list=[]
        # AI 
        self.move_counter=0
        self.vision=pygame.Rect(0,0,150,20)
        self.idling =False
        self.idling_counter=0
        # activate animation
        animation_type=['breathing','run','death']
        for animation in animation_type:
            temp_list=[]

            num_of_frams=len(os.listdir(f'./img/{self.character}/{animation}'))
            for i in range(num_of_frams):
                img= pygame.image.load(f"./img/{self.character}/{animation}/0{i}.png").convert_alpha()
                img = pygame.transform.scale(img,(int((img.get_height()*size)),int(img.get_width()*size)))
                # self.animation_list.append(img)
                temp_list.append(img)
            self.animation_list.append(temp_list)
        
        # for i in range(5):
        #     img= pygame.image.load(f"./img/{self.character}/breathing/0{i}.png")
        #     img = pygame.transform.scale(img,(int((img.get_height()*size)),int(img.get_width()*size)))
        #     self.animation_list.append(img)

        ####################################################################################################
        self.img=self.animation_list[self.run_index][self.index]
        self.rect=self.img.get_rect()
        self.rect.center=(x,y)
    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown>0:
            self.shoot_cooldown-=1
        
    def move(self,movie_left,movie_right):
        #movement variables
        dx=0
        dy=0

        if movie_left:
            dx=-self.speed
            self.flip=False
            self.direction=1
        if movie_right:
            dx=self.speed
            self.flip=True
            self.direction=-1
        
        if self.jump==True and self.in_air==False:
            self.vel_y=-11#hiw high
            self.jump=False
            self.in_air=True
        # 重利 gravity
        self.vel_y+= GARVITY
        if self.vel_y>10:
            self.vel_y
        dy+= self.vel_y
        # floor =500
        if self.rect.bottom+dy>500:
            dy=500-self.rect.bottom
            self.in_air=False#回歸地面

        self.rect.x+=dx
        self.rect.y+=dy

    def shoot(self):
        if self.shoot_cooldown==0 and self.ammo>0:
            self.shoot_cooldown=20
            bullet=Bullet(self.rect.centerx-(0.75*self.rect.size[0]*self.direction),self.rect.centery,self.direction)
            bullet_group.add(bullet)
            #釦子但
            self.ammo-=1
    def enemyshoot(self):
        if self.shoot_cooldown==0 and self.ammo>0:
            self.shoot_cooldown=20
            bullet=Bullet(self.rect.centerx-(0.6*self.rect.size[0]*self.direction),self.rect.centery,self.direction)
            bullet_group.add(bullet)
            #釦子但
            self.ammo-=1
    def AI(self):
        if self.alive and player.alive:
            if self.idling==False and random.randint(1,200)==2:
                self.updata_action(0)
                self.idling=True
                self.idling_counter=50
            # find player
            if self.vision.colliderect(player.rect):
                self.updata_action(0)
                self.idling=True
                self.enemyshoot()
                
                
            if self.idling==False:
                if self.direction==-1:
                    AI_moving_right= True
                else:
                    AI_moving_right=False
                AI_moving_left= not AI_moving_right
                self.move(AI_moving_left,AI_moving_right)
                self.updata_action(1)#runing
                self.move_counter+=1

                self.vision.center=(self.rect.centerx-75*self.direction,self.rect.centery)
                # pygame.draw.rect(DISPLAY,RED,self.vision)
                if self.move_counter>TILE_SIZE:
                    self.direction*=-1
                    self.move_counter*=-1
            else:
                self.idling_counter-=1
                if self.idling_counter<=0:
                    self.idling=False
                self.vision.center=(self.rect.centerx-75*self.direction,self.rect.centery)
                # pygame.draw.rect(DISPLAY,RED,self.vision)
    def update_animation(self):
        #timer
        ANIMATION_COOLDOWN=100

        self.img=self.animation_list[self.run_index][self.index]
        if pygame.time.get_ticks()-self.update_time>ANIMATION_COOLDOWN:
            self.update_time=pygame.time.get_ticks()
            self.index+=1
            # self.index=self.index%5
        if self.index>=len(self.animation_list[self.run_index]):
            if self.alive==False:
                self.index=len(self.animation_list[self.run_index])-1 
                self.kill()
            else: 
                self.index=0
    def updata_action(self,new_action):
        if new_action != self.run_index:
            self.run_index=new_action
            #updata aaa
            self.index=0
            self.update_time=pygame.time.get_ticks()
    def check_alive(self):
        if self.health<=0:
            self.health=0
            self.speed=0
            self.alive=False
            self.updata_action(2)

    def draw(self):
        DISPLAY.blit(pygame.transform.flip(self.img,self.flip,False),self.rect)
        pygame.draw.rect(DISPLAY,RED,self.rect,1)#碰撞箱

class Itembox(pygame.sprite.Sprite):
    def __init__(self,item_type,x,y):
          pygame.sprite.Sprite.__init__(self)
          self.item_type=item_type
          self.image =item_boxes[self.item_type]
          self.rect=self.image.get_rect()
          self.rect.midtop=(x+TILE_SIZE//2,y+(TILE_SIZE-self.image.get_height()))
    def update(self):
        #觸碰機制
        if pygame.sprite.collide_rect(self,player):
            #ccheak box
            if self.item_type=='health':
                player.health+=7
                print(player.health)
                if player.health>player.max_health:
                    player.health=player.max_health
            if self.item_type=='grenade':
                player.grenades+=5
                print(player.grenades)
            if self.item_type=='bullet':
                player.ammo+=10
                print(player.ammo)
            self.kill()

class Healthbar():
    offset_x=0
    offset_y=-20
    def __init__(self,x,y,health,max_health):
        self.x=x
        self.y=y
        self.heslth=health
        self.max_health=max_health

    def draw(self,health):
        self.heslth=health
        #比例換算
        ratio=self.heslth/self.max_health
        pygame.draw.rect(DISPLAY,BLACK,(self.x-2,self.y-2,154,24))
        pygame.draw.rect(DISPLAY,RED,(self.x,self.y,150,20))
        pygame.draw.rect(DISPLAY,GREEN,(self.x,self.y,150*ratio,20))
class moveHPbar():
    def __init__(self, enemy, offset_x=0, offset_y=-10):
        # 綁定敵人
        self.enemy = enemy
        self.offset_x = offset_x  # 血條相對於敵人的水平偏移
        self.offset_y = offset_y  # 血條相對於敵人的垂直偏移

    def draw(self):
        if self.enemy.health > 0:
            # 計算血條位置
            x = self.enemy.rect.x + self.offset_x
            y = self.enemy.rect.y + self.offset_y

            # 比例換算
            ratio = self.enemy.health / self.enemy.max_health
            pygame.draw.rect(DISPLAY, BLACK, (x - 2, y - 2, 52, 7))  # 外框
            pygame.draw.rect(DISPLAY, RED, (x, y, 50, 6))            # 背景（紅色）
            pygame.draw.rect(DISPLAY, GREEN, (x, y, 50 * ratio, 6))  # 當前血量（綠色）
        else:
            pass
class Bullet(pygame.sprite.Sprite):
      def __init__(self, x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.flip=True
        self.speed=10
        self.image=pygame.transform.flip(bullet_img, direction == 1, False)
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.direction=direction
        if direction==1:
            self.flip=False
        else:
            self.flip=True
            
            
      def update(self):
        
        self.rect.x+=(-self.direction*self.speed)
      #check bullet has gone off display
        if self.rect.right<0 or self.rect.left>800:#800
            self.kill()
        
    # #hit enumy
        if pygame.sprite.spritecollide(player,bullet_group,False):
            if player.alive:
                player.health-=1
                print(player.health)
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy,bullet_group,False):
                if enemy.alive:
                    enemy.health-=1
                    print(enemy.health)
                    self.kill()
        
class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        
        # 初始化變數
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image=grenade_img
        self.direction = direction
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.direction=direction
    def update(self):
        self.vel_y+=GARVITY
        dx=-self.direction*self.speed
        dy=self.vel_y

        # if self.rect.bottom+dy==500:
        #     self.direction*=-1
        #     dx=self.direction*(self.speed-1)
        
        if self.rect.bottom+dy>530: #回歸地面
            dy=520-self.rect.bottom
            self.speed=0
        self.rect.x+=dx
        self.rect.y+=dy
        if self.rect.left+dx<0 or self.rect.right+dx>800:#800
            self.direction*=-1
            dx=self.direction*(self.speed-3)
        self.timer-=1
        if self.timer<=0 or self.speed==0 :
            self.kill()
            explosion=Explosion(self.rect.x,self.rect.y,0.5)
            explosion_group.add(explosion)
            # do damage to all staff
            if abs(self.rect.centerx-player.rect.centerx)<TILE_SIZE*2 and \
               abs(self.rect.centery-player.rect.centery)<TILE_SIZE*2 :
                player.health-=3
            for enemy in enemy_group:
                if abs(self.rect.centerx-enemy.rect.centerx)<TILE_SIZE*2 and \
                   abs(self.rect.centery-enemy.rect.centery)<TILE_SIZE*2 :
                    enemy.health-=3
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        
        # 初始化變數
        self.images=[]
        for num in range(1,6):
            img =pygame.image.load(f'img/explosion/exp{num}.png').convert_alpha()
            img =pygame.transform.scale(img,(int((img.get_height()*0.5)),int(img.get_width()*0.5)))
            self.images.append(img)
        self.frame_index=0
        self.image=self.images[self.frame_index]
        self.rect=self.image.get_rect()
        self.rect.center=(x+40,y+20)
        self.counter=0      
    def update(self):
        explosion_speed=4
        self.counter+=1
        if self.counter>=explosion_speed:
            self.counter=0
            self.frame_index+=1
            if self.frame_index>= len(self.images):
                self.kill()
            else:
                self.image=self.images[self.frame_index]  
# groups
enemy_group=pygame.sprite.Group()
bullet_group=pygame.sprite.Group()
grenade_group=pygame.sprite.Group()
explosion_group=pygame.sprite.Group()
item_box_group=pygame.sprite.Group()

#item box
item_box=Itembox('health',100,450)
item_box_group.add(item_box)
item_box=Itembox('bullet',300,450)
item_box_group.add(item_box)
item_box=Itembox('grenade',400,450)
item_box_group.add(item_box)

# def platyer
#        (self,character, x,  y, size,speed,ammo,health,grenades)

player= human('character',200,200,0.6,3,20,10,5)
HPbar=Healthbar(10,10,player.health,player.health)

#AI

enemy=human('doroenemy',100,450,0.6,2,5,5,5)
enemyHP=moveHPbar(enemy)

enemy2=human('doroenemy',300,300,0.6,2,5,5,5)
enemyHP2=moveHPbar(enemy2)
enemy_group.add(enemy)
enemy_group.add(enemy2)
# boss=human("boss",500,400,0.3,5,20,5,5)

#main game
while True:
    clock.tick(FPS)
    draw_bg()
    #show HPbar
    enemyHP.draw()
    enemyHP2.draw()
    HPbar.draw(player.health)
    #文字數值機制
    draw_text(f'AMMO: {player.ammo}',font,WHITE,10,35)
    # draw_text(f'HP: {player.health}',font,WHITE,10,55)
    draw_text(f'grenade:',font,WHITE,10,65)
    for x in range(player.grenades):
        DISPLAY.blit(grenade_img,(65+(x*30),25))
    #player
    player.update()
    player.draw()

    #enemy
    for enemy in enemy_group:
        enemy.AI()
        enemy.update()
        enemy.draw()

    # #enemy
    # boss.update()
    # boss.draw()d


    buttons = pygame.mouse.get_pressed()
    #draw group
    explosion_group.update()
    bullet_group.update()
    grenade_group.update()
    item_box_group.update()
    explosion_group.draw(DISPLAY)
    bullet_group.draw(DISPLAY)
    grenade_group.draw(DISPLAY)
    item_box_group.draw(DISPLAY)
    if player.alive:
        #shooting
        if movie_left or movie_right :
            if shoot:
                player.shoot()
            if grenade and grenade_thrown==False and player.grenades>0:
                grenade=Grenade(player.rect.centerx+(-0.7*player.rect.size[0]*player.direction),
                                player.rect.top,
                                player.direction)
                grenade_group.add(grenade)
                grenade_thrown=True
                player.grenades-=1

        if player.in_air:
            player.updata_action(0)
        #show step 跑或休息
        if movie_left or movie_right:
            player.updata_action(1)#1=run
        else:
            player.updata_action(0)
        player.move(movie_left,movie_right)


    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            sys.exit()
         # 滑鼠按鍵處理
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左鍵
                shoot = True
            elif event.button == 3:  # 右鍵（手榴彈）
                grenade = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 左鍵
                shoot = False
            elif event.button == 3:  # 右鍵（手榴彈）
                grenade = False
                grenade_thrown=False
        # keyboard 
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_a:
                movie_left=True
            if event.key==pygame.K_d:
                movie_right=True
            if event.key==pygame.K_SPACE and player.alive:
                player.jump=True
            # if buttons[0]and player.alive:
            #     shoot=True
            # if event.key==pygame.K_a:
            #     movie_left=True
        # keyborad ending
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_a:
                movie_left=False
            if event.key==pygame.K_d:
                movie_right=False
            if event.key==pygame.K_SPACE:
                player.jump=False
        # if event.type== pygame.MOUSEBUTTONDOWN:
        #     click()
        

     
    pygame.display.update()