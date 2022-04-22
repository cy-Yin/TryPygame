import pygame


# define the "normal" bullet
class Bullet1(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(r"images\bullet1.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position

        self.speed = 12
        # check if the bullet moves to the end of the interface or collides with enemies
        # If so, the bullet need to be redrawn at the midtop of "my plane"
        self.active = False
        # to use sprite.collide_mask function to check the collision more accurately
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            # the bullet is destroyed
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True


# define the "super" bullet
class Bullet2(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(r"images\bullet2.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position

        # set the "super" bullet faster than the "normal" conterpart
        self.speed = 14
        # check if the bullet moves to the end of the interface or collides with enemies
        # If so, the bullet need to be redrawn at the midtop of "my plane"
        self.active = False
        # to use sprite.collide_mask function to check the collision more accurately
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            # the bullet is destroyed
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True
