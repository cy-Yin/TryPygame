import pygame
import sys
import traceback
from pygame.locals import *
from random import *


# "Ball" class inherits from parent class "Sprite"
class Ball(pygame.sprite.Sprite):
    def __init__(self, grayball_image, greenball_image, position, speed, bg_size, target):
        # initialize the pygame.sprite
        pygame.sprite.Sprite.__init__(self)

        self.grayball_image = pygame.image.load(grayball_image).convert_alpha()
        self.greenball_image = pygame.image.load(greenball_image).convert_alpha()
        self.rect = self.grayball_image.get_rect()
        # put the ball in the certain position
        self.rect.left, self.rect.top = position
        # set "side" attribute to represent direction
        self.side = [choice([-1, 1]), choice([-1, 1])]
        self.speed = speed
        self.collide = False
        self.target = target
        # at the beginning no ball is under control
        self.control = False
        self.width, self.height = bg_size[0], bg_size[1]
        self.radius = self.rect.width / 2

    def move(self):
        if self.control:
            self.rect = self.rect.move(self.speed)
        else:
            self.rect = self.rect.move((self.side[0] * self.speed[0], self.side[1] * self.speed[1]))

        # If the ball passes through the top of the page, it will appear from the bottom. 
        # Similarly, if the ball comes in from the left, it comes out on the right.
        if self.rect.right <= 0:
            self.rect.left = self.width
        elif self.rect.left >= self.width:
            self.rect.right = 0
        elif self.rect.bottom <= 0:
            self.rect.top = self.height
        elif self.rect.top >= self.height:
            self.rect.bottom = 0

    # check whether the motion of the cursor fits with the target range we set
    def check(self, motion):
        if self.target < motion < self.target + 5:
            return True
        else:
            return False
            

# design the control panel for the cursor moving within it
class Glass(pygame.sprite.Sprite):
    def __init__(self, glass_image, mouse_image, bg_size):
        # initialize the pygame.sprite
        pygame.sprite.Sprite.__init__(self)
        
        self.glass_image = pygame.image.load(glass_image).convert_alpha()
        self.glass_rect = self.glass_image.get_rect()
        # put the "glass" panel at the bottom of the interface
        self.glass_rect.left, self.glass_rect.top = (bg_size[0] - self.glass_rect.width) // 2, bg_size[1] - self.glass_rect.height

        self.mouse_image = pygame.image.load(mouse_image).convert_alpha()
        self.mouse_rect = self.mouse_image.get_rect()
        self.mouse_rect.left, self.mouse_rect.top = self.glass_rect.left, self.glass_rect.top
        # set the mouse invisible
        pygame.mouse.set_visible(False)
        

def main():
    pygame.init()

    grayball_image = r"gray_ball.png"
    greenball_image = r"green_ball.png"
    glass_image = r"glass.png"
    mouse_image = r"hand.png"
    bg_image = r"background.png"

    running = True

    # add the background music
    pygame.mixer.music.load(r"bg_music.mp3")
    pygame.mixer.music.play()

    # add the sound effects
    loser_sound = pygame.mixer.Sound(r"loser.wav")
    laugh_sound = pygame.mixer.Sound(r"laugh.wav")
    winner_sound = pygame.mixer.Sound(r"winner.wav")
    hole_sound = pygame.mixer.Sound(r"hole.wav")

    # game over when the music ends
    GAMEOVER = USEREVENT
    pygame.mixer.music.set_endevent(GAMEOVER)

    # set the size of the interface according to the background picture
    bg_size = width, height = 1024, 681
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption("Play the ball - Demo")

    background = pygame.image.load(bg_image).convert_alpha()

    # define the location of five holes respectively
    # the first two numbers in each tuple restrict the targeted range of each.rect.left
    # the rest two numbers in each tuple restrict the targeted range of each.rect.top
    hole = [(117, 119, 199, 201), 
            (225, 227, 390, 392), 
            (503, 505, 320, 322), 
            (698, 700, 192, 194), 
            (906, 908, 419, 421)
    ]

    # save the messages that will be printed
    msgs = []

    # create a list to store the balls
    balls = []
    group = pygame.sprite.Group()

    # create 5 balls
    BALL_NUM=5
    for i in range(BALL_NUM):
        # set random positions and speeds for the balls respectively at the beginning
        position = randint(0, width-100), randint(0, height-100)
        speed = [randint(1, 10), randint(1, 10)]
        # when the frequency of cursor motion reach the range from 5*(i+1) to 5*(i+2), the number i ball gets controlled (turn green)
        ball = Ball(grayball_image, greenball_image, position, speed, bg_size, 5 * (i+1))
        # check whether the latest created ball influences other balls (make other balls stuck)
        while pygame.sprite.spritecollide(ball, group, False, pygame.sprite.collide_circle):
            ball.rect.left, ball.rect.top = randint(0, width-100), randint(0, height-100)
        balls.append(ball)
        group.add(ball)

    # create the "glass" control panel
    glass = Glass(glass_image, mouse_image, bg_size)

    # "motion" records the number of events created by the motion of the cursor motion in control panel
    motion = 0

    # create the second user-defined event (the first one is "GAMEOVER" in line 91)
    # check the number of events created by the cursor motion every minute (1000 ms)
    MYTIMER = USEREVENT + 1 
    pygame.time.set_timer(MYTIMER, 1000)

    # set the repeatable response when a key is pressed down continuously
    # the frequency of the response is set 100ms
    # so when gameplayer press down a key of WASD over a period of time, the controlled ball will keep speeding up in certain direction
    pygame.key.set_repeat(100, 100)

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # when lose the game
            elif event.type == GAMEOVER:
                loser_sound.play()
                pygame.time.delay(2000)
                laugh_sound.play()
                running = False

            # check the number of events created by the cursor motion every minute
            elif event.type == MYTIMER:
                if motion:
                    for each in group:
                        if each.check(motion):
                            # make the current ball stop at once and under control
                            each.speed = [0, 0]
                            each.control = True
                    motion = 0

            elif event.type == MOUSEMOTION:
                motion += 1

            # when the ball is under control, gameplayer is allowed to use KEY_WASD to move this ball
            # the KEYDOWN event is checked every 100ms to simulate the speed-up effect
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    for each in group:
                        if each.control:
                            each.speed[1] -= 1
                if event.key == K_s:
                    for each in group:
                        if each.control:
                            each.speed[1] += 1
                if event.key == K_a:
                    for each in group:
                        if each.control:
                            each.speed[0] -= 1
                if event.key == K_d:
                    for each in group:
                        if each.control:
                            each.speed[0] += 1

                if event.key == K_SPACE:
                    # check whether a ball is within the range of a hole
                    for each in group:
                        if each.control:
                            for i in hole:
                                if i[0] <= each.rect.left <= i[1] and i[2] <= each.rect.top <= i[3]:
                                    # play the sound to show a ball has been put down into the hole successfully
                                    hole_sound.play()
                                    each.speed = [0, 0]
                                    # remove the hole-held ball from the group so other ones will avoid a collision with it
                                    group.remove(each)
                                    # put this ball at the top of the "balls" list 
                                    # so that it will be drawn firstly when the interface is refreshed
                                    # other balls will cover it when passing it rather than be covered
                                    temp = balls.pop(balls.index(each))
                                    balls.insert(0, temp)
                                    # at most one ball in a hole
                                    hole.remove(i)
                            # the player win this game when no hole is left empty
                            if not hole:
                                pygame.mixer.music.stop()
                                # play congratulation sound!
                                winner_sound.play()
                                pygame.time.delay(3000)
                                msg = pygame.image.load(r"win.png").convert_alpha()
                                msg_pos = (width - msg.get_width()) // 2, (height - msg.get_height()) // 2
                                msgs.append((msg, msg_pos))
                                laugh_sound.play()

            
        screen.blit(background, (0, 0))
        screen.blit(glass.glass_image, glass.glass_rect)

        # get the current of the mouse and set a new cursor to replace the default one 
        glass.mouse_rect.left, glass.mouse_rect.top = pygame.mouse.get_pos()
        # restrict the cursor motion with in the "glass" panel
        if glass.mouse_rect.left < glass.glass_rect.left:
            glass.mouse_rect.left = glass.glass_rect.left
        if glass.mouse_rect.left > glass.glass_rect.right - glass.mouse_rect.width:
            glass.mouse_rect.left = glass.glass_rect.right - glass.mouse_rect.width
        if glass.mouse_rect.top < glass.glass_rect.top:
            glass.mouse_rect.top = glass.glass_rect.top
        if glass.mouse_rect.top > glass.glass_rect.bottom - glass.mouse_rect.height:
            glass.mouse_rect.top = glass.glass_rect.bottom - glass.mouse_rect.height

        screen.blit(glass.mouse_image, glass.mouse_rect)

        for each in balls:
            # let the balls begin to move!
            each.move()
            # the ball will get another random speed after a collision
            if each.collide:
                each.speed = [randint(1, 10), randint(1, 10)]
                each.collide = False
            # when the ball is under control, it turns green
            # when the ball has not been under control yet. it remains gray
            if each.control:
                screen.blit(each.greenball_image, each.rect)
            else:
                screen.blit(each.grayball_image, each.rect)

        # when the collision happens
        for each in group:
            # firstly remove this ball from the group to avoid detecting whether the ball collides with itself
            group.remove(each)
            # use the "collision detection" function --> detect the collision of this circle
            # determine whether the current ball collides with other(s)
            if pygame.sprite.spritecollide(each, group, False, pygame.sprite.collide_circle):
                # when collided, the ball get a reverse speed direction
                each.side[0] = -each.side[0]
                each.side[1] = -each.side[1]
                each.collide = True
                if each.control:
                    each.side[0] = -1
                    each.side[1] = -1
                    # when the ball is collided by other ball(s), this ball turns gray and uncontrolled
                    each.control = False
            # add this judged ball back to the group
            group.add(each)

        for msg in msgs:
            screen.blit(msg[0], msg[1])

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    # if exceptions appears when running the code, they will be reported rather than be ignored
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        # free up initialized resources
        pygame.quit()
        input()
        
