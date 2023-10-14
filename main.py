#Создай собственный Шутер!
from random import randint
from pygame import *
from time import time as timer


class GameSprite(sprite.Sprite):
    def __init__(self, image_file, x, y, speed, size_x, size_y):
        super().__init__() 
        self.image = transform.scale(
            image.load(image_file), (size_x, size_y)
        )  
        self.speed = speed  
        self.rect = (
            self.image.get_rect()
        )  
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < height - 150:
            self.rect.y += self.speed
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < height - 150:
            self.rect.y += self.speed
window = display.set_mode((width, height))
display.set_caption("Ping Pong")
back = (200, 255, 255)  
window.fill(back)
clock = time.Clock()
FPS = 60

font.init()
font1 = font.SysFont("Arial", 36)
lose1 = font1.render("PLAYER 1 LOSE!", True, (180, 0, 0))
lose2 = font1.render("PLAYER 2 LOSE!", True, (180, 0, 0))

racket1 = Player("racket.png", 30, 200, 4, 50, 150)
racket2 = Player("racket.png", 520, 200, 4, 50, 150)
ball = GameSprite("tenis_ball.png", 200, 200, 4, 50, 50)
ball_x = 3
ball_y = 3

finish = False
game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.fill(back)    
        racket1.update_l()  
        racket2.update_r()
        ball.rect.x += ball_x
        ball.rect.y += ball_y
        if sprite.collide_rect(racket1, ball):
            ball_x *= -1
        if sprite.collide_rect(racket2, ball):
            ball_x *= -1

        if ball.rect.y < 0 or ball.rect.y > height - 50:
            ball_y *= -1

       
        if ball.rect.x < 0:
            finish = True
            window.blit(lose1, (200, 200)) 
        if ball.rect.x > width - 50:
            finish = True
            window.blit(lose2, (200, 200)
        # обновление картинок объектов
        racket1.reset()
        racket2.reset()        
        ball.reset()

    display.update()
    clock.tick(FPS)
