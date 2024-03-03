#Create your own shooter

from pygame import *
from random import randint



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed


    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)





class Enemy(GameSprite):
    
    def update(self):
        global missed
        self.rect.y += self.speed
        
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width-80)
            missed += 1



class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        
        if self.rect.y < 0:
            self.kill()





win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter Game")
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
clock = time.Clock()


FPS = 60
isRunning = True
finished = False

ship = Player('rocket.png', 5, win_height-100, 80, 100, 10)


enemies = sprite.Group()
for i in range(6):
    enemy = Enemy('ufo.png', randint(80, win_width-80), -40, 80, 50, randint(1, 5))
    enemies.add(enemy)

bullets = sprite.Group()





font.init()
font_1 = font.SysFont("comicsansms", 36)


score = 0
missed = 0



lose = font_1.render('YOU LOST!!', True, (180, 0, 0))

win = font_1.render('YOU WIN!', True, (255, 255, 255))







while isRunning:
    for e in event.get():
        if e.type == QUIT:
            isRunning = False
   
        elif e.type == MOUSEBUTTONDOWN:
            ship.fire()




    if not finished:
        window.blit(background, (0,0))


        text = font_1.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        

        text = font_1.render("Missed: " + str(missed), 1, (255, 255, 255))
        window.blit(text, (10,50))
    
    
        ship.update()
        ship.reset()
    
        enemies.update()
        enemies.draw(window)

        bullets.update()
        bullets.draw(window)


        collides = sprite.groupcollide(enemies, bullets, True, True)
        for c in collides:
            score = score + 1
            enemy = Enemy('ufo.png', randint(80, win_height-80), -40, 80, 50, randint(1, 5))
            enemies.add(enemy)

        if sprite.spritecollide(ship, enemies, False):
            finish = True
            window.blit(lose, (200, 200))

        if missed == 10:
            finished = True
            window.blit(lose, (200, 200))



        if score == 20:
            finished = True
            window.blit(background, (0,0))


            text = font_1.render("Score: " + str(score), 1, (255, 255, 255))
            window.blit(text, (10, 20))
        

            text = font_1.render("Missed: " + str(missed), 1, (255, 255, 255))
            window.blit(text, (10,50))
    
    
            ship.update()
            ship.reset()
    
            enemies.update()
            enemies.draw(window)

            bullets.update()
            bullets.draw(window)
            window.blit(win, (200, 200))



        display.update()
        clock.tick(FPS)