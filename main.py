import pygame
import sys
import random
def laser_update(laser_list, speed=300):
    for laser in laser_list:
        laser.y -= speed * dt
        if laser.bottom < 0:
            laser_list.remove(laser)

def meteor_update(meteor_list, speed=300):
    for meteor_tuple in meteor_list:
        meteor = meteor_tuple[0]
        direction = meteor_tuple[1]
        meteor.center += direction * speed * dt

        if meteor.top > window_height:
            meteor_list.remove(meteor_tuple)

def display_score():
    score_text = f'Score: {pygame.time.get_ticks()//1000}'
    text_surf = font.render(score_text, True, 'White')
    text_rect = text_surf.get_rect(midbottom=(window_width / 2, window_height - 80))
    pygame.draw.rect(display_surface, 'White', text_rect.inflate(30, 30), width=8, border_radius=10)
    display_surface.blit(text_surf, text_rect)

def laser_timer(can_shoot, duration = 500):
    if not can_shoot:
        current_time = pygame.time.get_ticks()
        if current_time-shoot_time>duration:
            can_shoot = True
    return can_shoot

# initialize pygame
pygame.init()

# clock
clock = pygame.time.Clock()

# window
window_width, window_height = 1280, 720

display_surface = pygame.display.set_mode((window_width, window_height))

# title
pygame.display.set_caption('Asteroid')

# importing images
ship_surf = pygame.image.load('./graphics/ship.png').convert_alpha()

background = pygame.image.load('./graphics/background.png').convert()
laser_surf = pygame.image.load('./graphics/laser.png').convert_alpha()
meteor_surf = pygame.image.load('./graphics/meteor.png').convert_alpha()

meteor_list = []

# rectangle size of the image, located with its center in the middle of the screen
ship_rect = ship_surf.get_rect(center=(window_width/2, window_height/2))
# laser_rect = laser_surf.get_rect(midbottom=ship_rect.midtop)
laser_list = []

# laser timer
can_shoot = True
shoot_time = None


# fonts
font = pygame.font.Font('./graphics/subatomic.ttf', 50)


# surface
test_surf = pygame.Surface((400, 100))

# meteor timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 500)

# import sound
laser_sound = pygame.mixer.Sound('./sounds/laser.ogg')
explosion_sound = pygame.mixer.Sound('./sounds/explosion.wav')
background_music = pygame.mixer.Sound('./sounds/music.wav')
background_music.play(-1)

# main game loop
while True:
    # input =>  events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:

            #laser
            laser_rect = laser_surf.get_rect(midbottom=ship_rect.midtop)
            laser_list.append(laser_rect)

            #timer
            can_shoot = False
            shoot_time = pygame.time.get_ticks()

            #play laser sound
            laser_sound.play()

        if event.type == meteor_timer:
            meteor_rect = meteor_surf.get_rect(center=(random.randint(0,window_width),-50))
            direction = pygame.math.Vector2(random.uniform(-0.5, 0.5), 1)
            meteor_list.append((meteor_rect, direction))


    # framerate limit
    dt = clock.tick(120) / 1000
    #print(clock.get_fps())

    time_passed = pygame.time.get_ticks()

    # mouse input
    ship_rect.center = pygame.mouse.get_pos()

    # collision
    for meteor_tuple in meteor_list:
        meteor_rect = meteor_tuple[0]
        if ship_rect.colliderect(meteor_rect):
            pygame.quit()
            sys.exit()

    # laser meteor collision
    for laser_rect in laser_list:
        for meteor_tuple in meteor_list:
            if laser_rect.colliderect(meteor_tuple[0]):
                laser_list.remove(laser_rect)
                meteor_list.remove(meteor_tuple)
                explosion_sound.play()

    # updates
    display_surface.fill((0, 0, 0))

    # placing
    display_surface.blit(background, (0, 0))

    display_score()
    laser_update(laser_list)
    can_shoot = laser_timer(can_shoot, 400)

    display_surface.blit(ship_surf, ship_rect)
    for laser in laser_list:
        display_surface.blit(laser_surf, laser)

    for meteor_tuple in meteor_list:
        display_surface.blit(meteor_surf, meteor_tuple[0])

    meteor_update(meteor_list)


    # display surface
    pygame.display.update()

