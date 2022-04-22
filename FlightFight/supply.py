import pygame
from random import *


# define the supply of "super" bullets
class Bullet_Supply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(r"images\bullet_supply.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.bottom = randint(0, self.width-self.rect.width), -100

        self.speed = 5
        # check whether it is time to give the supply item and whether it is available
        self.active = False
        # to use sprite.collide_mask function to check the collision more accurately
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = randint(0, self.width-self.rect.width), -100


# define the supply of full-screen bombs
class Bomb_Supply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(r"images\bomb_supply.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.bottom = randint(0, self.width-self.rect.width), -100
        
        self.speed = 5
        # check whether it is time to give the supply item and whether it is available
        self.active = False
        # to use sprite.collide_mask function to check the collision more accurately
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = randint(0, self.width-self.rect.width), -100
