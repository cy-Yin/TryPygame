# main.py

import pygame
import sys
import traceback
from pygame.locals import *
from random import *

import myplane
import bullet
import enemy
import supply


pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("FlightFight -- Demo")

background = pygame.image.load(r"images\background.png").convert()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# upload the musics to the game
pygame.mixer.music.load(r"sound\game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound(r"sound\bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound(r"sound\use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound(r"sound\supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound(r"sound\get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound(r"sound\get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound(r"sound\upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound(r"sound\enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound(r"sound\enemy1_down.wav")
enemy1_down_sound.set_volume(0.1)
enemy2_down_sound = pygame.mixer.Sound(r"sound\enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound(r"sound\enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound(r"sound\me_down.wav")
me_down_sound.set_volume(0.2)


# add the enemy planes
def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_large_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.LargeEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)


# upgrade the player's level according to the score
# a higher level means more enemies or higher speed of the enemies
def inc_speed(target, inc):
    for each in target:
        each.speed += inc


def main():
    pygame.mixer.music.play(-1)

    # generate "my plane"
    me = myplane.MyPlane(bg_size)

    enemies = pygame.sprite.Group()
    # generate 15 small enemy planes
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)
    # generate 4 medium enemy planes
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)
    # generate 2 large enemy planes
    large_enemies = pygame.sprite.Group()
    add_large_enemies(large_enemies, enemies, 2)

    # generate 4 "normal" bullets at the midtop of "my plane"
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    # generate 4 pairs of "super" bullets at the midtop of "my plane"
    bullet2 = []
    bullet2_index = 0
    # the total number of the "super" bullets is 8, dividing into 4 pairs
    BULLET2_NUM = 8
    for i in range(BULLET2_NUM//2):
        # locate the left one
        bullet2.append(bullet.Bullet2((me.rect.centerx-33, me.rect.centery)))
        # locate the right one
        bullet2.append(bullet.Bullet2((me.rect.centerx+30, me.rect.centery)))

    clock = pygame.time.Clock()

    # index to decide which "destroy" picture to show in each lists when plane get shot
    me_destroy_index = 0
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0

    # show the score on the interface and record it
    score = 0
    score_font = pygame.font.Font(r"font\font.ttf", 36)

    # respond to player's "pause" or "resume" operation
    paused = False
    pause_nor_image = pygame.image.load(r"images\pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load(r"images\pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load(r"images\resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load(r"images\resume_pressed.png").convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width-paused_rect.width-10, 10
    # choose the "pause_nor" as the default setting
    paused_image = pause_nor_image

    # set the player's level and increase the difficulty of the game according to the level
    level = 1

    # set the full-screen bombs
    bomb_image = pygame.image.load(r"images\bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font(r"font\font.ttf", 48)
    # the number of bombs the player has
    bomb_num = 3

    # give a supply item every 30 seconds
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 30*1000)

    # use the "super" bullet timer to restrict its duration
    DOUBLE_BULLET_TIME = USEREVENT + 1

    # mark whether the "super" bullet is being used
    is_double_bullet = False

    # use the timer to stop the invincible status
    INVINCIBLE_TIME = USEREVENT + 2

    # set the number of lives of my plane
    life_image = pygame.image.load(r"images\life.png").convert_alpha()
    life_rect = life_image.get_rect()
    # the player is allowed to have 3 opportunities to achieve the goal
    life_num = 3

    # use the "recorded" to prevent repeating open the record file
    recorded = False

    # show when the game is over
    gameover_font = pygame.font.Font(r"font/font.TTF", 48)
    again_image = pygame.image.load(r"images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load(r"images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    # switch the two "my plane" images to create a dynamic effect
    switch_image = True

    # use the "delay" variable to control the speed
    delay = 100

    # check the game is running or having been paused
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # get the pause-and-resume operations
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        # suspend the item supply
                        # suspend all the musics and sounds
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, 30*1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image

            # use the full-screen bombs
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            # every enemy plane is destroyed
                            if each.rect.bottom > 0:
                                each.active = False

            # give one supply item every 30 seconds
            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                # choose one of the two supply types randomly
                if choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            # initialize the "super" bullet effect
            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

            # initialize the invincible status of my new-born plane
            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)


        # upgrade the player's level when the score reaches 50000, 300000, 600000, 1000000
        # increase the difficulty of game withe the upgrade of the player's level
        # the increase of difficulty means more enemies or higher speed of the enemies
        if level == 1 and score > 50000:
            level = 2
            upgrade_sound.play()
            # add 3 small enemy planes, 2 medium ones and 1 large one
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_large_enemies(large_enemies, enemies, 1)
            # increase the speed of small enemy planes
            inc_speed(small_enemies, 1)
        elif level == 2 and score > 300000:
            level = 3
            upgrade_sound.play()
            # add 5 small enemy planes, 3 medium ones and 2 large ones
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_large_enemies(large_enemies, enemies, 2)
            # increase the speed of small and medium enemy planes
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 3 and score > 600000:
            level = 4
            upgrade_sound.play()
            # add 5 small enemy planes, 3 medium ones and 2 large ones
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_large_enemies(large_enemies, enemies, 2)
            # increase the speed of small and medium enemy planes
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 4 and score > 1000000:
            level = 5
            upgrade_sound.play()
            # add 5 small enemy planes, 3 medium ones and 2 large ones
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_large_enemies(large_enemies, enemies, 2)
            # increase the speed of small and medium enemy planes
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)


        screen.blit(background, (0, 0))


        # when paused = False and my plane has at least one life, continue the game
        if life_num and not paused:
            # get the player's operations of pressing keys to move plane
            key_pressed = pygame.key.get_pressed()
            # move "my plane" as the player commands
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()


            # draw the full-screen bomb supply
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                # check whether it has been received
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    # the player is allowed to have at most 3 full-screen bombs in the inventory
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False

            # draw the "super" bullet supply
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                # check whether it has been received
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    is_double_bullet = True
                    # set the duration of the "super" bullet effect for 18 seconds
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18*1000)
                    bullet_supply.active = False


            # shoot the bullets every 10 frames
            if not(delay % 10):
                bullet_sound.play()
                if not(is_double_bullet):
                    # shoot the "normal" bullets
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index+1) % BULLET1_NUM
                else:
                    # shoot the "super" bullets
                    bullets = bullet2
                    # locate the left one
                    bullets[bullet2_index].reset((me.rect.centerx-33, me.rect.centery))
                    # locate the right one
                    bullets[bullet2_index+1].reset((me.rect.centery+30, me.rect.centerx))
                    bullet2_index = (bullet2_index+2) % BULLET2_NUM

            # check whether the bullet hit the enemy plane
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        # the bullet is destroyed
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in large_enemies:
                                # if a medium or large enemy plane is hit, its energy will be diminished
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    # the medium or large enemy plane is destroyed
                                    e.active = False
                            else:
                                # the small enemy plane is destroyed
                                e.active = False


            # draw small enemy planes on the interface
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # the plane has been destroyed
                    if not(delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index+1) % 4
                        if e1_destroy_index == 0:
                            score += 1000
                            each.reset()

            # draw medium enemy planes on the interface
            for each in mid_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        # when the bullet hits the medium enemy plane
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    # draw the status line to show the enemy's Health Point
                    pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top-5), (each.rect.right, each.rect.top-5), 2)
                    # set the line green when the remained energy is greater than 20 percent of the original energy
                    # else set the line red
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, \
                        (each.rect.left, each.rect.top-5), \
                        (each.rect.left+each.rect.width*energy_remain, each.rect.top-5), 2)

                else:
                    # the plane has been destroyed
                    if not(delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index+1) % 4
                        if e2_destroy_index == 0:
                            score += 6000
                            each.reset()

            # draw large enemy planes on the interface
            for each in large_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        # when the bullet hits the large enemy plane
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        # use the image switch to add a dynamic effect
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # draw the status line to show the enemy's Health Point
                    pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top-5), (each.rect.right, each.rect.top-5), 2)
                    # set the line green when the remained energy is greater than 20 percent of the original energy
                    # else set the line red
                    energy_remain = each.energy / enemy.LargeEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,\
                        (each.rect.left, each.rect.top-5),\
                        (each.rect.left+each.rect.width*energy_remain, each.rect.top-5), 2)

                    # play sound to tell player the large enemy plane is coming
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play(-1)
                else:
                    # the plane has been destroyed
                    if not(delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index+1) % 6
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 10000
                            each.reset()

            # check whether "my plane" is collided and destroyed
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                    e.active = False

            # draw "my plane" on the interface
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                # the plane has been destroyed
                if not(delay % 3):
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index+1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        # my new-born plane will be in an invincible status for 3 seconds
                        pygame.time.set_timer(INVINCIBLE_TIME, 3*1000)

            # draw the text to show the number of full_screen bombs
            bomb_text = bomb_font.render("x %d" % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height-10-bomb_rect.height))
            screen.blit(bomb_text, (20+bomb_rect.width, height-5-text_rect.height))

            # draw the life_image(s) to allow player know how many lives his/her plane has by counting the number
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, (width-10-(i+1)*life_rect.width, height-10-life_rect.height)) 

            # draw the score text
            score_text = score_font.render("SCORE : %s" % str(score), True, WHITE)
            screen.blit(score_text, (10, 5))

        elif life_num == 0:
            # stop the background music
            pygame.mixer.music.stop()
            # stop the sound effects
            pygame.mixer.stop()
            # stop the supply of special items
            pygame.time.set_timer(SUPPLY_TIME, 0)
        
            if not recorded:
                recorded = True
                # from the record file get the highest score
                with open(r"record.txt",'r') as file:
                    record_score = int(file.read())
                # refresh the record if the newest score is higher than any one of thr history scores
                if score > record_score:
                    with open(r"record.txt",'w') as file:
                        file.write(str(score))

            # draw the GAMEOVER interface
            # draw the record(the highest score) before this try
            record_score_text = score_font.render("Best : %d" % record_score, True, WHITE)
            screen.blit(record_score_text, (50, 50))

            gameover_text1 = gameover_font.render("Your Score", True, WHITE)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = (width-gameover_text1_rect.width)//2, height//3
            screen.blit(gameover_text1, gameover_text1_rect)
            
            # draw the newest score
            gameover_text2 = gameover_font.render(str(score), True, WHITE)
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = (width-gameover_text2_rect.width)//2, gameover_text1_rect.bottom+10
            screen.blit(gameover_text2, gameover_text2_rect)

            # draw the try-again option
            again_rect.left, again_rect.top = (width-again_rect.width)//2, gameover_text2_rect.bottom+50
            screen.blit(again_image, again_rect)
            # draw the game-over option
            gameover_rect.left, gameover_rect.top = (width-again_rect.width)//2, again_rect.bottom+10
            screen.blit(gameover_image, gameover_rect)

            # if the player press the mousebutton1
            if pygame.mouse.get_pressed()[0]:
                # get the cursor position
                pos = pygame.mouse.get_pos()
                # if the player chooses "try again" option
                if again_rect.left < pos[0] < again_rect.right and again_rect.top < pos[1] < again_rect.bottom:
                    # restart the game
                    main()
                # if the player chooses "game over" option   
                elif gameover_rect.left < pos[0] < gameover_rect.right and gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # exit from the game
                    pygame.quit()
                    sys.exit()

        # draw the "pause" button
        screen.blit(paused_image, paused_rect)

        # slow down the speed of image switch
        # set the image to switch every 5 frames
        if not(delay % 5):
            switch_image = not switch_image

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    else:
        traceback.print_exc()
        pygame.quit()
        input()
