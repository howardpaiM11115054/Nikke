import pygame, sys
import os
import random
import csv
import gamepull

pygame.init()
#set time
clock=pygame.time.Clock()
FPS=60
DISPLAY_WIDTH=800
DISPLAY_HIGH=int(DISPLAY_WIDTH*0.8)
#game vel
GARVITY=0.75
ROWS=16
COLS=150
TILE_SIZE=DISPLAY_HIGH//ROWS# 接觸居離
SCROLL_THRESH=200
TILE_TYPES=22
display_scroll=0
bg_scroll=0
level =1
start_game=False
#display size
DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HIGH))

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
#load world
img_list=[]
for x in range(TILE_TYPES):
    img =pygame.image.load(f'img/Tile/{x}.png')
    img=pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE))
    img_list.append(img)
#back ground image
tree_img=pygame.image.load("./img/background/Tree.png").convert_alpha()
tree_img = pygame.transform.scale(tree_img,(int((tree_img.get_height())),int(tree_img.get_width()*0.2)))
city_img=pygame.image.load("./img/background/City.png").convert_alpha()
city_img = pygame.transform.scale(city_img,(int((city_img.get_height())),int(city_img.get_width()*0.85)))
mountain_img=pygame.image.load("./img/background/Mountain.png").convert_alpha()
sky_img=pygame.image.load("./img/background/Sky.png").convert_alpha()
#button image
start_img=pygame.image.load("./img/button/start_button.png").convert_alpha()
exit_img=pygame.image.load("./img/button/exit_button.png").convert_alpha()
#load image
bullet_img=pygame.image.load("./img/bullet/bullet.png").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img,(int((bullet_img.get_height())*0.5),int(bullet_img.get_width()*0.5)))
grenade_img=pygame.image.load("./img/grenade/00.png").convert_alpha()
grenade_img = pygame.transform.scale(grenade_img,(int((grenade_img.get_height()*0.8)),int(grenade_img.get_width()*0.8)))
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
    sky_width=sky_img.get_width()
    tree_width=tree_img.get_width()
    city_width=city_img.get_width()
    mountain_width=mountain_img.get_width()
    sky_width=sky_img.get_width()
    for x in range(6):
        DISPLAY.blit(sky_img,((x*sky_width)-bg_scroll*0.5,0))
        mountain_img_height = mountain_img.get_height()
        DISPLAY.blit(mountain_img, ((x*mountain_width)-bg_scroll*0.6, int(DISPLAY_HIGH - mountain_img_height - 100)))
        tree_img_height = tree_img.get_height()
        DISPLAY.blit(tree_img, ((x*tree_width)-bg_scroll*0.7, int(DISPLAY_HIGH - tree_img_height )))
        city_img_height =city_img.get_height()
        DISPLAY.blit(city_img, ((x*city_width)-bg_scroll, int(DISPLAY_HIGH - city_img_height+245)))
        
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
        self.width=self.img.get_width()
        self.height=self.img.get_height()
    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown>0:
            self.shoot_cooldown-=1
        
    def move(self,movie_left,movie_right):
        #movement variables
        display_scroll=0
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
            self.vel_y=-12#how high
            self.jump=False
            self.in_air=True
        # 重利 gravity
        self.vel_y+= GARVITY
        if self.vel_y>10:
            self.vel_y
        dy+= self.vel_y
        #check floor 
        for tile in world.obstacle_lst:
           # check floor x
            if tile[1].colliderect(self.rect.x+dx,self.rect.y,self.width,self.height):
                dx=0
                # if ai saw the wall must be turn aronud
                if self.character=='enemy':
                    self.direction*=-1
                    self.move_counter=0
            # check collision in y
            if tile[1].colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
                #if jump
                if self.vel_y <0:
                    self.vel_y=0
                    dy = tile[1].bottom-self.rect.top
                elif self.vel_y >=0:
                    self.vel_y=0
                    self.in_air=False
                    dy = tile[1].top-self.rect.bottom
        if self.character=='character':
            if self.rect.left+dx<0 or self.rect.right+dx>DISPLAY_WIDTH:
                dx=0
        #going to edges or screen banned
        if self.character=='character':
            if self.rect.left+dx<0 or self.rect.right+dx>DISPLAY_WIDTH:
             dx=0

        self.rect.x+=dx
        self.rect.y+=dy
        #update scroll
        if self.character=='character':
            if (self.rect.right>DISPLAY_WIDTH-SCROLL_THRESH and bg_scroll<(world.level_length*TILE_SIZE)-DISPLAY_WIDTH)\
                or (self.rect.left<SCROLL_THRESH and bg_scroll>abs(dx)):
                self.rect.x-=dx
                display_scroll=-dx
        return display_scroll

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
        self.rect.x+=display_scroll
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
class World():
    def __init__(self):
        self.obstacle_lst=[]
    def process_data(self,data):
        self.level_length=len(data[0])
        for y,row in enumerate(data):
            for x,tile in enumerate(row):
                if tile>=0:
                    img=img_list[tile]
                    img_rect=img.get_rect()
                    img_rect.x=x*TILE_SIZE
                    img_rect.y=y*TILE_SIZE
                    tile_data=(img,img_rect)
                    if tile>=0 and tile<=8:
                        self.obstacle_lst.append(tile_data)
                    elif tile ==9 or tile==10:
                        water=Water(img,x*TILE_SIZE,y*TILE_SIZE)
                        water_group.add(water)
                    elif tile >=11 and tile<=14:
                        decoration=Decoration(img,x*TILE_SIZE,y*TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile ==15: 
                        #(self,character,x,y,size,speed,ammo,health,grenades)                                              
                        player= human('character',x*TILE_SIZE,y*TILE_SIZE,0.5,6,20,10,20)
                        HPbar=Healthbar(10,10,player.health,player.health)
                    elif tile ==16:
                        enemy=human('doroenemy',x*TILE_SIZE,y*TILE_SIZE,0.5,2,5,5,5)
                        enemyHP=moveHPbar(enemy)#add enemy HP
                        enemy_group.add(enemy)
                        enemyHP_group.add(enemyHP)
                    elif tile ==17: #ammbox
                        #item box                        
                        item_box=Itembox('bullet',x*TILE_SIZE,y*TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile ==18:
                        item_box=Itembox('grenade',x*TILE_SIZE,y*TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile ==19:                       
                        item_box=Itembox('health',x*TILE_SIZE,y*TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile ==20:
                        exit=Exit(img,x*TILE_SIZE,y*TILE_SIZE)
                        exit_group.add(exit)
        return player,HPbar
    def draw(self):
        for tile in self.obstacle_lst:
            tile[1][0]+=display_scroll
            DISPLAY.blit(tile[0],tile[1])

class Decoration(pygame.sprite.Sprite):
    def __init__(self,img,x,y):
          pygame.sprite.Sprite.__init__(self)
          self.image=img
          self.rect=self.image.get_rect()
          self.rect.midtop=(x+TILE_SIZE//2,y+(TILE_SIZE-self.image.get_height()))
    def update(self):
        self.rect.x+=display_scroll

class Water(pygame.sprite.Sprite):
    def __init__(self,img,x,y):
          pygame.sprite.Sprite.__init__(self)
          self.image=img
          self.rect=self.image.get_rect()
          self.rect.midtop=(x+TILE_SIZE//2,y+(TILE_SIZE-self.image.get_height()))
    def update(self):
        self.rect.x+=display_scroll

class Exit(pygame.sprite.Sprite):
    def __init__(self,img,x,y):
          pygame.sprite.Sprite.__init__(self)
          self.image=img
          self.rect=self.image.get_rect()
          self.rect.midtop=(x+TILE_SIZE//2,y+(TILE_SIZE-self.image.get_height()))
    def update(self):
        self.rect.x+=display_scroll
class Itembox(pygame.sprite.Sprite):
    def __init__(self,item_type,x,y):
          pygame.sprite.Sprite.__init__(self)
          self.item_type=item_type
          self.image =item_boxes[self.item_type]
          self.rect=self.image.get_rect()
          self.rect.midtop=(x+TILE_SIZE//2,y+(TILE_SIZE-self.image.get_height()))
    def update(self):
        #觸碰機制
        self.rect.x+=display_scroll

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
class moveHPbar(pygame.sprite.Sprite):
    def __init__(self, enemy, offset_x=0, offset_y=-10):
        super().__init__()
        # 綁定敵人
        self.enemy = enemy
        self.offset_x = offset_x  # 血條相對於敵人的水平偏移
        self.offset_y = offset_y  # 血條相對於敵人的垂直偏移

        # 創建一個透明的 Surface 作為 image
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

    def update(self):
        # 動態更新血條的位置
        if self.enemy.health > 0:
            self.rect.x = self.enemy.rect.x + self.offset_x
            self.rect.y = self.enemy.rect.y + self.offset_y
        else:
            self.kill()  # 如果敵人死亡，移除血條

    def draw(self):
        if self.enemy.health > 0:
            # 計算血量比例
            ratio = self.enemy.health / self.enemy.max_health
            # 繪製血條
            pygame.draw.rect(DISPLAY, BLACK, (self.rect.x - 2, self.rect.y - 2, 52, 7))  # 外框
            pygame.draw.rect(DISPLAY, RED, (self.rect.x, self.rect.y, 50, 6))            # 背景（紅色）
            pygame.draw.rect(DISPLAY, GREEN, (self.rect.x, self.rect.y, 50 * ratio, 6))  # 當前血量（綠色）

        
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
        
        self.rect.x+=(-self.direction*self.speed)+display_scroll
      #check bullet has gone off display
        if self.rect.right<0 or self.rect.left>DISPLAY_WIDTH:#800
            self.kill()
        #check tile
        for tile in world.obstacle_lst:
            if tile[1].colliderect(self.rect):
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
        self.width=self.image.get_width()
        self.height=self.image.get_height()
        self.direction=direction
    def update(self):
        self.vel_y+=GARVITY
        dx=-self.direction*self.speed
        dy=self.vel_y

        # if self.rect.bottom+dy==500:
        #     self.direction*=-1
        #     dx=self.direction*(self.speed-1)
        for tile in world.obstacle_lst:
            if tile[1].colliderect(self.rect.x+dx,self.rect.y,self.width,self.height):#800
                self.direction*=-1
                dx=-self.direction*self.speed
            # check collision in y
            if tile[1].colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
                self.speed=0
                #if throw up
                if self.vel_y <0:
                    self.vel_y = 0
                    self.speed=7#歸還地面碰裝失去的速度
                    
                    dx=self.direction*self.speed
                    dy = tile[1].bottom-self.rect.top
                elif self.vel_y >=0:
                    self.vel_y=0
                    dy = tile[1].top-self.rect.bottom

        
        self.rect.x+=dx+display_scroll
        self.rect.y+=dy
        
        self.timer-=1
        if self.timer<=0  :
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
        self.rect.center=(x+15,y+10)
        self.counter=0      
    def update(self):
        self.rect.x+=display_scroll
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
enemyHP_group=pygame.sprite.Group()
water_group=pygame.sprite.Group()
decoration_group=pygame.sprite.Group()
exit_group=pygame.sprite.Group()
# #item box
# item_box=Itembox('health',100,450)
# item_box_group.add(item_box)
# item_box=Itembox('bullet',300,450)
# item_box_group.add(item_box)
# item_box=Itembox('grenade',400,450)
# item_box_group.add(item_box)
#build button
start_button=gamepull.Button(DISPLAY_WIDTH//2-10,DISPLAY_HIGH//2-200,start_img,0.5)
exit_button=gamepull.Button(DISPLAY_WIDTH//2-240,DISPLAY_HIGH//2-200,exit_img,0.5)
# # def platyer
# #        (self,character, x,  y, size,speed,ammo,health,grenades)

# player= human('character',200,200,0.6,3,20,10,5)
# HPbar=Healthbar(10,10,player.health,player.health)

# #AI

# enemy=human('doroenemy',100,450,0.6,2,5,5,5)
# enemyHP=moveHPbar(enemy)#add enemy HP
# enemyHP_group.add(enemyHP)
# enemy_group.add(enemy)

# enemy2=human('doroenemy',300,300,0.6,2,5,5,5)
# enemyHP2=moveHPbar(enemy2)#add enemy HP
# enemyHP_group.add(enemyHP2)
# enemy_group.add(enemy2)
# # boss=human("boss",500,400,0.3,5,20,5,5)
# #empty ti;e list
world_data=[]
for row in range(ROWS):
    r=[-1]*COLS
    world_data.append(r)
    #load in level data 
with open(f"level{level}_data.csv",newline='') as csvfile:
    reader=csv.reader(csvfile,delimiter=',')
    for x,row in enumerate(reader):
        for y,tile in enumerate(row):
            world_data[x][y]=int(tile)
world= World()
player,HPbar=world.process_data(world_data)
#main game
while True:
    clock.tick(FPS)
    if not start_game:
        # 菜單畫面
        DISPLAY.fill((0, 0, 0))  # 黑色背景

        # 繪製按鈕
        if start_button.draw(DISPLAY):
            start_game = True  # 切換到遊戲狀態
        if exit_button.draw(DISPLAY):
            running = False  
            pygame.quit()
            sys.exit()# 結束遊戲
    else:
        draw_bg()
        #updata background
        world.draw()
        #show enemy HPbar
        # enemyHP.draw()
        # enemyHP2.draw()
        #show HPbar
        HPbar.draw(player.health)
        #文字數值機制
        draw_text(f'AMMO: {player.ammo}',font,WHITE,10,35)
        # draw_text(f'HP: {player.health}',font,WHITE,10,55)
        draw_text(f'grenade:',font,WHITE,10,65)
        for x in range(player.grenades):
            DISPLAY.blit(grenade_img,(100+(x*30),62))
        #player
        player.update()
        player.draw()

        #enemy
        for enemy in enemy_group:
            enemy.AI()
            enemy.update()
            enemy.draw()
            enemyHP_group.update()
            enemyHP_group.draw(DISPLAY)
        for hp_bar in enemyHP_group:
            hp_bar.draw()
        # #enemy
        # boss.update()
        # boss.draw()d

        

        buttons = pygame.mouse.get_pressed()
        #draw group
        
        explosion_group.update()
        bullet_group.update()
        grenade_group.update()
        item_box_group.update()
        water_group.update()
        decoration_group.update()
        exit_group.update()


        explosion_group.draw(DISPLAY)
        bullet_group.draw(DISPLAY)
        grenade_group.draw(DISPLAY)
        item_box_group.draw(DISPLAY)
        water_group.draw(DISPLAY)
        decoration_group.draw(DISPLAY)
        exit_group.draw(DISPLAY)
    
    

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
        display_scroll=player.move(movie_left,movie_right)
        bg_scroll-=display_scroll
        


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