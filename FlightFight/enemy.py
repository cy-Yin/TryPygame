import pygame
from random import *


# define the small enemy plane
class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(r"images\enemy1.png").convert_alpha()

        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load(r"images/enemy1_down1.png").convert_alpha(),
            pygame.image.load(r"images/enemy1_down2.png").convert_alpha(),
            pygame.image.load(r"images/enemy1_down3.png").convert_alpha(),
            pygame.image.load(r"images/enemy1_down4.png").convert_alpha(),
        ])

        self.rect = self.image.get_rect()

        self.width, self.height = bg_size[0], bg_size[1]

        self.speed = 2
        # mark whether it is destroyed
        self.active = True
        # to use sprite.collide_mask function to check the crack more accurately
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = randint(0, self.width-self.rect.width)
        self.rect.top = randint(-5 * self.height, 0)

    # set the motion of the small enemy planes
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left = randint(0, self.width-self.rect.width)
        self.rect.top = randint(-5 * self.height, 0)


# define the medium enemy plane
class MidEnemy(pygame.sprite.Sprite):
    # one medium enemy plane needs 8 bullets to destroy
    energy = 8

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = self.image = pygame.image.load(r"images/enemy2.png").convert_alpha()

        self.image_hit = pygame.image.load(r"images/enemy2_hit.png").convert_alpha()

        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load(r"images/enemy2_down1.png").convert_alpha(),
            pygame.image.load(r"images/enemy2_down2.png").convert_alpha(),
            pygame.image.load(r"images/enemy2_down3.png").convert_alpha(),
            pygame.image.load(r"images/enemy2_down4.png").convert_alpha(),
        ])

        self.rect = self.image.get_rect()

        self.width, self.height = bg_size[0], bg_size[1]

        self.speed = 1
        # mark whether it is destroyed
        self.active = True
        # to use sprite.collide_mask function to check the crack more accurately
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = MidEnemy.energy
        self.hit = False
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-10 * self.height, -self.height)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = MidEnemy.energy
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-10 * self.height, -self.height)


# define the large enemy plane
class LargeEnemy(pygame.sprite.Sprite):
    # one medium enemy plane needs 20 bullets to destroy
    energy = 20

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load(r"images\enemy3_n1.png").convert_alpha()
        self.image2 = pygame.image.load(r"images\enemy3_n2.png").convert_alpha()

        self.image_hit = pygame.image.load(r"images/enemy3_hit.png").convert_alpha()

        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load(r"images/enemy3_down1.png").convert_alpha(),
            pygame.image.load(r"images/enemy3_down2.png").convert_alpha(),
            pygame.image.load(r"images/enemy3_down3.png").convert_alpha(),
            pygame.image.load(r"images/enemy3_down4.png").convert_alpha(),
            pygame.image.load(r"images/enemy3_down5.png").convert_alpha(),
            pygame.image.load(r"images/enemy3_down6.png").convert_alpha(),
        ])

        self.rect = self.image1.get_rect()

        self.width, self.height = bg_size[0], bg_size[1]

        self.speed = 1
        # mark whether it is destroyed
        self.active = True
        # to use sprite.collide_mask function to check the crack more accurately
        self.mask = pygame.mask.from_surface(self.image1)
        self.energy = LargeEnemy.energy
        self.hit = False
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-15 * self.height, 5 * self.height)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = LargeEnemy.energy
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-15 * self.height, -5 * self.height)
