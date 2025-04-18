from pygame import *
import time as t
from random import *
from math import atan2,sin,cos,fabs,pi
window_size = (800,800)
FPS = 60
volume = 0.10
mixer.init()
clock = time.Clock()
font.init()

player_size = {
                "width": round(window_size[0] * .05),
                "height": round(window_size[1] * .05)
            }

player_pos = {
                "x": round(window_size[0] * .50 - player_size["width"] * .50),
                "y": round(window_size[1] * .45)
            }

enemy_size = {
                "width": round(window_size[0] * .06),
                "height": round(window_size[1] * .05 )
            }

class GameSprite(sprite.Sprite):
    def __init__(self, img:str, pos = [0, 0], size = [0, 0], speed = 5):
        """img = адрес изображения
        pos = [X,Y];
        size = [W,H]; """
        super().__init__()

        self.image = transform.scale(image.load(img), size)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1] 
        speed/FPS
        self.speed = speed 
   
    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, img, pos=[0, 0], size=[0, 0], speed=5):
        super().__init__(img, pos, size, speed)
        self.bullet_list = sprite.Group()

        self.bullet_speed = 5
        self.bullet_size=[self.rect.width * .30,
                              self.rect.height * .30]
        
        self.gcd = 0.5
        self.start_t = 0
        self.naw_t = 0
    def update(self, *args, **kwargs):
        pos_mouse = mouse.get_pos()

        self.show()
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x += -self.speed 
        if keys[K_d] and self.rect.x < window_size[0]:
            self.rect.x += self.speed 
        if keys[K_w] and self.rect.y > 0:
            self.rect.y += -self.speed
        if keys[K_s] and self.rect.y < window_size[1] - self.rect.height:
            self.rect.y += self.speed

        if mouse.get_pressed()[0]:

            self.naw_t = t.time()
            if self.naw_t - self.start_t >= self.gcd:
                self.start_t = t.time()
                self.naw_t = self.start_t

                self.fire()
                mixer.music.load("fire.ogg")
                mixer.music.set_volume(volume)
                mixer.music.play()
        return super().update(*args, **kwargs)

    def fire(self):
        pos_mouse = mouse.get_pos()
        dx = pos_mouse[0] - self.rect.centerx
        dy = pos_mouse[1] - self.rect.centery
        direction = atan2(dy, dx)

        bullet = Bullet("екк.png",
                        pos=[self.rect.centerx - 14,
                             self.rect.centery - 14],
                        size=[self.rect.width * .10,
                              self.rect.height * .15],
                        speed = 10,
                        direction=direction)
        self.bullet_list.add(bullet)



class Bullet(GameSprite):
    def __init__(self, img, pos, size, speed, direction):
        super().__init__(img, pos, size, speed)
        self.dx = cos(direction) * self.speed
        self.dy = sin(direction) * self.speed

    def update(self, *args, **kwargs):
        self.show()
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.y < -self.rect.height or self.rect.y > window_size[1] or self.rect.x < -self.rect.width or self.rect.x > window_size[0]:
            self.kill()

        return super().update(*args, **kwargs)


class Enemy(GameSprite):
    def __init__(self, img, size=[0, 0], speed=4):
        super().__init__(img, [1, 1], size, speed)
        self.dx = 0
        self.dy = 0
        self.respawn()

    def respawn(self):
        pos_start = randint(1, 4)
        if pos_start == 1:
            self.rect.x = randint(0, window_size[0])
            self.rect.y = -self.rect.height
        elif pos_start == 2:
            self.rect.x = window_size[0]
            self.rect.y = randint(0, window_size[1])
        elif pos_start == 3:
            self.rect.x = randint(0, window_size[0])
            self.rect.y = window_size[1]  + self.rect.height
        elif pos_start == 4:
            self.rect.x = -self.rect.width
            self.rect.y = randint(0, window_size[1])
    
    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def setMove(self,pos):
        x =  pos[0] - self.rect.centerx
        y =  pos[1] - self.rect.centery
        radian = atan2(y, x)
        #deegrees = radian * 180/pi
        #self.image = transform.rotate(self.image,degrees)
        self.dx = cos(radian) * self.speed
        self.dy = sin(radian) * self.speed

    def update(self, *args, **kwargs):
        self.show()
        if "player_pos" in kwargs:
            self.setMove(kwargs["player_pos"])
        
        self.move()

        return super().update(*args, **kwargs)

window = display.set_mode(window_size)
background = transform.scale(image.load("1673908942_49-zefirka-club-p-igrovoe-pole-vid-sverkhu-56.jpg"), window_size)

display.set_caption("game")
monsters = sprite.Group()
for i in range(2):
    m = Enemy("Без_названия__2_-removebg-preview.png",
                size = (enemy_size["width"],
                        enemy_size["height"]),
                speed = 4)
    monsters.add(m)

player = Player("gamer-removebg-preview.png",
                pos = (player_pos["x"],
                       player_pos["y"]),
                       
                size = (player_size["width"],
                        player_size["height"])
            )

run_game = True
game = True
clock = time.Clock()

fontText = font.Font(None,80)
font2Text = font.Font(None,40)
winNum = 0
loseNum = 5
loseText = fontText.render("Game over ",True,(255,100,100))
isLose = False
isWin = False


while game:
    for ev in event.get():
        if ev.type == QUIT:
            game = False
    window.blit(background, (0,0))
    if run_game:
        player.show()
        player.update()
        monsters.update(player_pos = [player.rect.centerx, player.rect.centery])
        monsters.draw(window)
        player.bullet_list.update()
        list_collide_kill = sprite.groupcollide(player.bullet_list, monsters,True, True)
        for collide in list_collide_kill:
            for i in list_collide_kill[collide]:
                winNum += 1
                m = Enemy("Без_названия__2_-removebg-preview.png",
                    size = (enemy_size["width"],
                            enemy_size["height"]),
                    speed = 4)
                monsters.add(m)
        list_collide_kill = sprite.spritecollide(player, monsters, True)
        for collide in list_collide_kill:
            loseNum -= 1
            m = Enemy("Без_названия__2_-removebg-preview.png",
                size = (enemy_size["width"],
                        enemy_size["height"]),
                speed = 4)
            monsters.add(m)


        loseNumText = font2Text.render("HP:"+str(loseNum),True,(150,150,150))
        window.blit(loseNumText, (10,20))

        winNumText = font2Text.render("KILL:"+str(winNum),True,(150,150,150))
        window.blit(winNumText, (10,50))
        if loseNum <= 0:
            run_game = False
            isWin = False
    else:
        window.blit(loseText,(window_size[0] * .50 - loseNumText.get_width() * .50,
                              window_size[1] * .50 - loseNumText.get_height() * .50))


    display.update()
    clock.tick(FPS)