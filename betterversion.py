import pygame
import sys

class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.image = pygame.image.load('./graphics/ship.png').convert_alpha()
        self.rect = self.image.get_rect(center=(window_width/2, window_height/2))

        # timer
        self.can_shoot = True
        self.shoot_time = None

    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 500:
                self.can_shoot = True

    def laser_shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            print('shoot')
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()


    def update(self):
        self.laser_timer()
        self.input_position()
        self.laser_shoot()

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)

        self.image = pygame.image.load('./graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)

pygame.init()

# clock
clock = pygame.time.Clock()

# window
window_width, window_height = 1280, 720
display_surface = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Space shooter')

# background
background_surf = pygame.image.load('./graphics/background.png').convert()

# sprite groups
spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()

# sprite creation
ship = Ship(spaceship_group)
laser = Laser(laser_group, ship.rect.midtop)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    dt = clock.tick() / 1000

    # update
    spaceship_group.update()

    # background
    display_surface.blit(background_surf, (0, 0))
    # graphics
    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)

    pygame.display.update()



