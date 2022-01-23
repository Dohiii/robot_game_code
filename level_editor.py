from os import write
import pygame
import button
import csv
import pickle

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#game window 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

# define game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS 
TILE_TYPES = 21  # changing depending on level editor and number of tiles

#define game variables
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

#load images

#mountains
background_img_1 = pygame.image.load('img/Background/desert1.png').convert_alpha()
background_img_1 = pygame.transform.scale(background_img_1, (1280, 720))

background_img_2 = pygame.image.load('img/Background/desert2.png').convert_alpha()
background_img_2 = pygame.transform.scale(background_img_2, (1280, 720))

background_img_main = pygame.image.load('img/Background/desert_main.png').convert_alpha()
background_img_main = pygame.transform.scale(background_img_main, (1280, 720))

# pines
# background_img_1 = pygame.image.load('img/Background/pine1.png').convert_alpha()
# background_img_1 = pygame.transform.scale(background_img_1, (1280, 720))

# background_img_2 = pygame.image.load('img/Background/pine2.png').convert_alpha()
# background_img_2 = pygame.transform.scale(background_img_2, (1280, 720))

# background_img_main = pygame.image.load('img/Background/mountain.png').convert_alpha()
# background_img_main = pygame.transform.scale(background_img_main, (1280, 720))

sky_cloud = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

# nav buttons GUI
save_img = pygame.image.load('img/save_btn.png').convert_alpha()
load_img = pygame.image.load('img/load_btn.png').convert_alpha()


# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)


# cloud1 = pygame.image.load('img/Background/cloud1.png').convert_alpha()
# cloud2 = pygame.image.load('img/Background/cloud2.png').convert_alpha()
# cloud3 = pygame.image.load('img/Background/cloud3.png').convert_alpha()
# cloud4 = pygame.image.load('img/Background/cloud4.png').convert_alpha()
# cloud5 = pygame.image.load('img/Background/cloud5.png').convert_alpha()
# cloud6 = pygame.image.load('img/Background/cloud6.png').convert_alpha()
# cloud7 = pygame.image.load('img/Background/cloud7.png').convert_alpha()
# cloud8 = pygame.image.load('img/Background/cloud8.png').convert_alpha()



# define colors 
GREEN = (144,201,120)
WHITE = (255,255,255)
RED = (255,18,22)

#define font
font = pygame.font.SysFont('Futura', 30)

# MOST IMPORTANT 
# create empty tile list inside a list of rows!
world_data = []
# create one row length of maximum collomns
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)
    
#create ground
for tile in range(0, MAX_COLS):
    # 0 to every index in last(lowest) list in list
    world_data[ROWS-1][tile] = 0

# function to put output text onto the screen
def draw_text(text,font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))


# create function for drawing background 
def draw_bg():
    screen.fill(GREEN)
    width = background_img_1.get_width()
    
    # range means how long lvl will be in width
    for x in range(4):
        
        screen.blit(background_img_main, ((x * width)-scroll * 0.5,0))
        screen.blit(sky_cloud, ((x * width)-scroll * 0.5,0))
        screen.blit(background_img_1, ((x * width)-scroll * 0.6,0))
        screen.blit(background_img_2, ((x * width)-scroll * 0.8,0))
        
        # screen.blit(cloud1, ((x * width)-scroll + 200 ,24))
        # screen.blit(cloud2, ((x * width)-scroll+ 600,89))
        # screen.blit(cloud2, ((x * width)-scroll+ 1000,168))
        # screen.blit(cloud7, ((x * width)-scroll+ 1190,180))
        # screen.blit(cloud3, ((x * width)-scroll + 500,23))
        # screen.blit(cloud4, ((x * width)-scroll+ 900,60))
        # screen.blit(cloud5, ((x * width)-scroll+ 350,150))
        # screen.blit(cloud6, ((x * width)-scroll+ 104,60))
        # screen.blit(cloud6, ((x * width)-scroll+ 823,89))
        # screen.blit(cloud7, ((x * width)-scroll+ 129,210))
        # screen.blit(cloud8, ((x * width)-scroll+ 532,23))

def draw_grid():
    #vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    
    #horizontal lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))
        
        
# function to draw tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))
            


# create Buttons
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
# make a button list
button_list = []
button_col = 0
button_row = 0

for i in range(len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col ==3 :
        button_row += 1
        button_col = 0



run = True
while run:
    clock.tick(FPS)
    
    draw_bg()
    draw_grid()
    draw_world()
    
    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text(f'Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)
    
    #save and load data
    if save_button.draw(screen):
        # save level data
        #pickle version (create piton list)
        # pickle_out = open(f'level{level}_data', 'wb')
        # pickle.dump(world_data, pickle_out)
        # pickle_out.close()
        with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in world_data:
                writer.writerow(row)
    # load level data
    if load_button.draw(screen):
        # reset scroll to ZERO
        # scroll = 0
        # # load with pickle
        # world_data = []
        # pickle_in = open(f'level{level}_data', 'rb')
        # world_data = pickle.load(pickle_in)
        
        
        #load csv
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

                
    
    # draw tile panel and tiles
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))
    
    #choose a tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count
            
    # highlite selected tile
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3 )
    
    # scroll the map
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed
        
    # add new tiles to the screen
    # get mouse position
    pos = pygame.mouse.get_pos()
    
    mx = (pos[0] + scroll )// TILE_SIZE
    my = pos[1] // TILE_SIZE
    
    # check if ccordinates is in draw tiles area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        #update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[my][mx] != current_tile:
                world_data[my][mx] = current_tile
        # right lick to clear tiles
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[my][mx] = -1
        

                    
        
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keybord presses 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 5
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 1
    
    pygame.display.update()

pygame.quit()