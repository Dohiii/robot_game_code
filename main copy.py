import pygame
import sys
import math
import random
from pygame import display
from pygame import image
from pygame.constants import KEYDOWN
from pygame.transform import scale
import os
import csv

from spark import Spark


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

FPS = 60
clock = pygame.time.Clock()


# define game ariables
GRAVITY = 0.75
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
level = 1

# define player actions variable.
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

# load images:
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load(
    'img/icons/grenade_box.png').convert_alpha()

item_boxes = {
    'Health': health_box_img,
    'Ammo': ammo_box_img,
    'Grenade': grenade_box_img,
}
# world images (store tiles in a list)
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/Tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)




sparks = []

# Defined colors
BG = (144, 201, 120)
RED = (255, 22, 18)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# define font
font = pygame.font.SysFont('Futura', 30)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg(bg):
    screen.fill(bg)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))





            #********************************************************************************                    
                                             # classes
            #********************************************************************************   



class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type,  x, y, scale, speed, ammo, grenades, health):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.grenades = grenades
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.health = health
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # create AI specific variables
        self.move_counter = 0
        # enemy line of sight
        self.vision = pygame.Rect(0, 0,
                                  150 # vision
                                  , 20)
        
        self.idling = False
        self.idling_counter = 0
        
        
        
        # load all images for players
        anumation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in anumation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in folder
            num_of_frames = len(os.listdir(
                f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(
                    f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.stay_dead = self.animation_list[3][7]
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.draw_health()
        self.check_alive()

        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # reset movement variables
        dx = 0
        dy = 0
        # assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # Jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        # update rectangle
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.9 * self.rect.size[0] * self.direction),
                            self.rect.centery, self.direction)
            bullet_group.add(bullet)
            # reduse ammo
            self.ammo -= 1
       
      # ai for NPCs       
    def ai(self):
        if self.alive and player.alive:   
            # idling check
            if self.idling == False and random.randint(1, 200) == 1:
                self.idling = True
                self.update_action(0) # Idle animation
                self.idling_counter = 50
            
            # check if player are in line of vision of AI
            if self.vision.colliderect(player.rect):
                self.shoot()
                self.update_action(0) # Idle animation
            # if AI doesnt see player all this code is running!
            else: 
                # movement code
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1) # run animation
                    self.move_counter += 1
                    # update AI vision
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    
                    
        #********************************************************************************                    
                            # this line is to test vision
                            # pygame.draw.rect(screen, RED, self.vision, 2)
        #********************************************************************************                                 
                     
                    # timer how far enemy can walk
                    if self.move_counter > TILE_SIZE:
                        self.move_counter *= -1
                        self.direction *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter == 0:
                        self.idling = False
            
            
            
            

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enought time has passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if animation run out reset it back to start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if new action is different from previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw_health(self):
        ratio = self.health / self.max_health
        if self.alive == True:
            pygame.draw.rect(screen, BLACK, (self.rect.x - 2, self.rect.y - 5,
                            self.max_health + 4, 7))
            pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 4,
                            self.max_health, 5))
            pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 4,
                            (self.health) * ratio, 5))

    def draw(self):
        screen.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)

class World():
    def __init__(self):
        self.obstacle_list = []
        
    def process_data(self, data):
        # iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    # create rect
                    img_rect = img.get_rect()
                    #give position on the grid
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    #checking for collisions
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Decorations(img, x * TILE_SIZE, y * TILE_SIZE, 'Water')
                        water_group.add(water)
                    elif tile >=11 and tile <= 14:
                        decoration = Decorations(img, x * TILE_SIZE, y * TILE_SIZE, 'Decoration')
                        decoration_group.add(decoration)
                    # Player and NPCs
                    # create a player
                    elif tile == 15:
                        player = Soldier('player', x * TILE_SIZE, y* TILE_SIZE, 2, 4, 20, 5, 55)
                    #------------------------ NPCs
                    elif tile == 16:
                        enemy = Soldier('enemy', x * TILE_SIZE, y* TILE_SIZE, 2, 2, 20, 2, 55)
                        enemy_group.add(enemy)
                        
                    # temp - create item boxes
                    elif tile == 17: #create Ammo box
                        item_box = ItemBox('Ammo', 600, 250)
                        item_box_group.add(item_box)
                    elif tile == 18: #create Grenade box
                        item_box = ItemBox('Grenade', 500, 250)
                        item_box_group.add(item_box)
                    elif tile == 19: #create Health box
                        item_box = ItemBox('Health', 400, 250)
                        item_box_group.add(item_box)
                    #create exit
                    elif tile == 20:
                        exit = Decorations(img, x * TILE_SIZE, y * TILE_SIZE, 'Exit')
                        exit_group.add(exit)
        return player
    
    def draw(self):
        for tile in self.obstacle_list:
            screen.blit(tile[0], tile[1])
                                               
class Decorations(pygame.sprite.Sprite):
    def __init__(self, img, x, y, type_of_decoration):
        pygame.sprite.Sprite.__init__(self)
        # tipes of decoration "Decoration"  "Water" "Exit"
        self.type_of_decoration = type_of_decoration
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +(TILE_SIZE - self.image.get_height()))
        

                          

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def update(self):
        # check if player collide with item_box
        if pygame.sprite.collide_rect(self, player):
            # check what kind of box it was
            if self.item_type == 'Health':
                player.health += 25
                # make maximum health do not go up with medical kit over max health
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 10
            elif self.item_type == 'Grenade':
                player.grenades += 3
        # delete the item box
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # move bullet
        self.rect.x += (self.direction * self.speed)
        # check if bullets has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        # check collisiion with charaters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                spark_hit(player)
                self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 10
                    spark_hit(enemy)
                    # update if is alive
                    if enemy.health <= 0:
                        enemy.alive = False
                    self.kill()


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = - 11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0

        # check if grenades has gone off screen
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed

        # update grenade position
        self.rect.x += dx
        self.rect.y += dy

        # count down timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y - 38, 1.2)
            explosion_group.add(explosion)

            # do damage to anyone in range (player and bots)
            # player
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 1 and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 1:
                player.health -= 45
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 35
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 3 and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 3:
                player.health -= 17
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 4 and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 4:
                player.health -= 11

            # enemy
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 1 and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 1:
                    enemy.health -= 45
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 25
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 3 and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 3:
                    enemy.health -= 17
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 4 and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 4:
                    enemy.health -= 12
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 5 and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 5:
                    enemy.health -= 5


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 11):
            img = pygame.image.load(
                f'img/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(
                img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        EXPLOSION_SPEED = 4
        # update explosion animation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            # if animation is complete delete an explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]

            #********************************************************************************                    
                                        # Sprite Groups and Instanses
            #********************************************************************************   


# Create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()


        #********************************************************************************                    
                                            #MAIN LOOP
        #********************************************************************************   
#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

# load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
            
world = World()
player = world.process_data(world_data)



run = True
while run:
    clock.tick(FPS)

    # update background
    draw_bg(BG)
    
    # draw world map
    world.draw()

    # show player health

    # show ammo/ granedes/ health
    draw_text(f'AMMO : ', font, WHITE, 10, 20)
    for x in range(player.ammo):
        screen.blit(bullet_img, (90 + (x*10), 25))
    draw_text(f'GRENADE : ', font, WHITE, 10, 40)
    for x in range(player.grenades):
        screen.blit(grenade_img, (130 + (x*20), 42.5))

    player.update()
    player.draw()
    
    # Draw enemyes
    for enemy in enemy_group:
        enemy.ai()
        enemy.update()
        enemy.draw()

    # update and draw Groups
    bullet_group.update()
    bullet_group.draw(screen)

    grenade_group.update()
    grenade_group.draw(screen)

    explosion_group.update()
    explosion_group.draw(screen)

    item_box_group.update()
    item_box_group.draw(screen)
    
    water_group.update()
    water_group.draw(screen)
    
    decoration_group.update()
    decoration_group.draw(screen)
    
    enemy_group.update()
    enemy_group.draw(screen)

    # sparks
    def spark_shoot(shooter):
        for i, spark in sorted(enumerate(sparks), reverse=True):
            spark.move(1)
            spark.draw(screen)
            if not spark.alive:
                sparks.pop(i)

        mx, my = enemy.rect.top, enemy.rect.left
        sparks.append(Spark([shooter.rect.centerx + (0.6 * shooter.rect.size[0] * shooter.direction), shooter.rect.centery,
                             enemy.direction], math.radians(random.randint(0, 360)), random.randint(2, 2), ('ORANGE'), 0.7))

    def spark_hit(victum):
        for i, spark in sorted(enumerate(sparks), reverse=True):
            spark.move(1)
            spark.draw(screen)
            if not spark.alive:
                sparks.pop(i)

        sparks.append(Spark([victum.rect.centerx, victum.rect.centery,
                             enemy.direction], math.radians(random.randint(0, 360)), random.randint(2, 3), ('RED'), 2))

    # update player actions
    if player.alive:
        # shoot bullets:
        if shoot:
            if player.ammo > 0:
                spark_shoot(player)
            player.shoot()
        # through grenade
        elif grenade and grenade_thrown == False and player.grenades > 0:
            grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),
                              player.rect.top, player.direction)
            grenade_group.add(grenade)
            grenade_thrown = True
            # reduce amaunt of granades
            player.grenades -= 1

        # moving character
        if player.in_air:
            player.update_action(2)  # means jump
        elif moving_left or moving_right:
            player.update_action(1)  # means run
        else:
            player.update_action(0)  # means IDLE
        player.move(moving_left, moving_right)
    else:
        player.update_action(3)  # means death

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        # Keybord presses:
        if event.type == pygame.KEYDOWN:
            # quit game
            if event.key == pygame.K_ESCAPE:
                run = False
            # restart game
            # if event.key == pygame.K_r and not player.alive():
            #     main()
            # move caracter
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            # shoot
            if event.key == pygame.K_SPACE:
                shoot = True
            # Grenade
            if event.key == pygame.K_q:
                grenade = True
            # Jumping
            if event.key == pygame.K_w and player.alive:
                player.jump = True

        # keybord button released:
        if event.type == pygame.KEYUP:
            # move caracter
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            # no shoot
            if event.key == pygame.K_SPACE:
                shoot = False
            # no grenade
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False

    pygame.display.update()
