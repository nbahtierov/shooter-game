from pygame import *
from random import randint
from time import time as timer
clock = time.Clock()
FPS = 60
window = display.set_mode((700, 500))
display.set_caption('Шутер')

background = transform.scale(image.load('galaxy.jpg'), (700, 500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
lost = 0
score = 0
font.init()
font1 = font.SysFont('Arial', 36)
text_score = font1.render('Счёт:' + str(lost), 1, (255, 255 , 230))
text_lose = font1.render('Пропущено:' + str(lost), 1, (10, 240, 255))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
        mixer.music.load('fire.ogg')
        mixer.music.play()
        pass

class Enemy(GameSprite):
    def update(self):
        global lost
        if self.rect.y > 450:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1

            self.speed = randint(1, 5)
        self.rect.y += self.speed

class Asteroids(GameSprite):
    def update(self):
        if self.rect.y > 450:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            #lost = lost + 1

            self.speed = randint(1, 5)
        self.rect.y += self.speed
asteroids = sprite.Group()
for i in range(3):
    aster = Asteroids('asteroid.png', randint(80, 620), -40,80, 50, randint(1, 7))
    asteroids.add(aster)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

           

bullets = sprite.Group()

enemies = sprite.Group()
for i in range(5):
    m = Enemy('ufo.png', randint(80, 620), -80, 80, 50, randint(1, 5))
    enemies.add(m)   
        
player = Player('rocket.png', 700//2, 500-100, 80, 100, 10)
game = True
finish = False
life = 3
life_text = font.SysFont('luminari', 70).render(str(life), True, (255, 255, 255))
num_fire = 0
rel_time = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and e.key == K_SPACE:
            if num_fire < 5 and rel_time == False:
                num_fire += 1
                player.fire()
            if num_fire >= 5 and rel_time == False:
                last_time = timer()
                rel_time = True
    if life == 0:
        finish = True
    if not finish:
        window.blit(background, (0, 0))
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                
                reload = font.SysFont('verdana', 40).render('Wait! reloading...', True, (255, 255, 255))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        sprites_list = sprite.groupcollide(enemies, bullets, True, True)
        for i in sprites_list:
            m = Enemy('ufo.png', randint(80, 620), -80, 80, 50, randint(1, 5))
            enemies.add(m)
            score += 1

        player_enemies_list = sprite.spritecollide(player, enemies, True)
        for i in player_enemies_list:
            life -= 1
            m = Enemy('ufo.png', randint(80, 620), -80, 80, 50, randint(1, 5))
            enemies.add(m)
            life_text = font.SysFont('', 70).render(str(life), True, (255, 255, 255))
        window.blit(life_text, (600, 0))
        player_enemies_list = sprite.spritecollide(player, asteroids, True)
        for i in player_enemies_list:
            life -= 1
            player_enemies_list = sprite.spritecollide(player, enemies, True)
        text_score = font1.render('Счёт: ' + str (score), True, (255, 0, 0))
        clock.tick(FPS)
        player.reset()
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (10, 240, 255))
        bullets.draw(window)
        bullets.update()
        if score > 35:
            finish = True
        if lost  > 40:
            finish = True
        enemies.draw(window)
        asteroids.draw(window)
        asteroids.update()
        enemies.update()
        player.update()
        window.blit(text_lose, (0, 0))
        window.blit(text_score, (-1, 27))
    display.update()
    clock.tick(FPS)

