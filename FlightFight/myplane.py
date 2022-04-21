import pygame


class MyPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load(r"images\me1.png").convert_alpha()
        self.image2 = pygame.image.load(r"images\me2.png").convert_alpha()

        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load(r"images/me_destroy_1.png").convert_alpha(),
            pygame.image.load(r"images/me_destroy_2.png").convert_alpha(),
            pygame.image.load(r"images/me_destroy_3.png").convert_alpha(),
            pygame.image.load(r"images/me_destroy_4.png").convert_alpha(),
        ])

        self.rect = self.image1.get_rect()

        self.width, self.height = bg_size[0], bg_size[1]

        self.speed = 10
        # mark whether it is destroyed
        self.active = True
        # set the invincible state during which my new-born plane cannot be destroyed
        self.invincible = False
        # to use sprite.collide_mask function to check the crack more accurately
        self.mask = pygame.mask.from_surface(self.image1)
        # at the beginning locate "my plane" in the middle of the lower part
        # reserve an area about 60 pixels long to place the status line on it
        self.rect.left = (self.width-self.rect.width)//2
        self.rect.top = self.height-self.rect.height-60

    # definite the motion of "my plane"
    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.bottom < self.height-60:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height-60

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width

    # set the new-born plane when the former one has been destroyed
    def reset(self):
        self.rect.left = (self.width-self.rect.width)//2
        self.rect.top = self.height-self.rect.height-60
        self.active = True
        # at the beginning the new-born plane is invincible
        self.invincible = True
