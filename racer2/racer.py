#importing
import pygame
import sys
import random, time
from pygame.locals import *

#initialize
pygame.init()

#setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

#variables for colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#other variables for screen, coins etc.
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SPEED = 5
SCORE = 0
COIN_SCORE = 0

#setting up fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("racer2/AnimatedStreet.png")

#creating wh screen
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)

#creating objects
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("racer2/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE, SPEED
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            # Increase speed of enemies after every N coins
            if SCORE % 5 == 0:
                SPEED += 5

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("racer2/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("racer2/—Pngtree—gold dollar coin_6848497.png") 
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        # Randomly generate coins with different weights on the road
        self.weight = random.uniform(0.5, 1.5)  # Random weight between 0.5 and 1.5

    def move(self):
        self.rect.move_ip(0, SPEED * self.weight)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
            self.rect.centerx = random.randint(40, SCREEN_WIDTH - 40)

#setting up sprites        
P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)  
all_sprites.add(E1)
coin_list = pygame.sprite.Group()

INC_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(INC_COIN, 2000)

while True:
    for event in pygame.event.get():
        #adding coin to the main group
        if event.type == INC_COIN:
            new_coin = Coin()
            all_sprites.add(new_coin)
            coin_list.add(new_coin)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_score = font_small.render("Coins: " + str(COIN_SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coin_score, (300, 10))

    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    #game over window
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('racer2/crash.wav').play()
        time.sleep(1)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    coins_collected = pygame.sprite.spritecollide(P1, coin_list, True)
    if coins_collected:
        COIN_SCORE += len(coins_collected)

    pygame.display.update()
    FramePerSec.tick(FPS)
