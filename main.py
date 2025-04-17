from pygame import *
import time as t
from random import *

window_size = (800,800)
FPS = 60
volume = 0.10
mixer.init()
clock = time.Clock()
font.init()

player_size = {
                "width": round(window_size[0] * .35),
                "height": round(window_size[1] * .30)
            }

player_pos = {
                "x": round(window_size[0] * .50 - player_size["width"] * .50),
                "y": round(window_size[1] * .45)
            }

enemy_size = {
                "width": round(window_size[0] * .30),
                "height": round(window_size[1] * .20 )
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
        self.show()
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x += -self.speed 
        if keys[K_d]:
            self.rect.x += self.speed 
        if keys[K_w]:
            self.rect.y += -self.speed
        if keys[K_s]:
            self.rect.y += self.speed

        if keys[K_SPACE]:

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
        bullet = Bullet("екк.png",
                        pos=[self.rect.centerx - 15,
                             self.rect.y + 100],
                        size=[self.rect.width * .10,
                              self.rect.height * .15],
                        speed = 10)
        self.bullet_list.add(bullet)
class Bullet(GameSprite):
    def update(self, *args, **kwargs):
        self.show()
        self.rect.x += self.speed

        if self.rect.y < -self.rect.height:
            self.kill()


        return super().update(*args, **kwargs)

class Enemy(GameSprite):
    def __init__(self, img, size=[0, 0], speed=5):
        super().__init__(img, [1, 1], size, speed)
        self.respawn()

    def respawn(self):
        self.rect.x = randint(0, window_size[0] - self.rect.width)
        self.rect.y = randint(0, window_size[1]  -self.rect.height)
    
    def update(self, *args, **kwargs):
        self.show()

        return super().update(*args, **kwargs)

window = display.set_mode(window_size)
background = transform.scale(image.load("1673908920_2-zefirka-club-p-igrovoe-pole-vid-sverkhu-2.jpg"), window_size)

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

while game:
    for ev in event.get():
        if ev.type == QUIT:
            game = False
    window.blit(background, (0,0))
    if run_game:
        player.show()
        player.update()
        monsters.update()
        monsters.draw(window)
        player.bullet_list.update()
        list_collide_kill = sprite.groupcollide(player.bullet_list, monsters,True, True)
        for collide in list_collide_kill:
            for i in list_collide_kill[collide]:
                m = Enemy("Без_названия__2_-removebg-preview.png",
                    size = (enemy_size["width"],
                            enemy_size["height"]),
                    speed = 5)
                monsters.add(m)

    display.update()
    clock.tick(FPS)