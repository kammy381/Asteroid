import pygame
import sys
import random
class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.image = pygame.image.load('./graphics/ship.png').convert_alpha()
        self.rect = self.image.get_rect(center=(window_width/2, window_height/2))

        #masks  needs to be called mask,  like rect also needs to be called rect
        self.mask = pygame.mask.from_surface(self.image)

        # timer
        self.can_shoot = True
        self.shoot_time = None

        #sound
        self.laser_sound = pygame.mixer.Sound('./sounds/laser.ogg')


    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def meteor_collisions(self):
        if pygame.sprite.spritecollide(self,meteor_group,False, pygame.sprite.collide_mask):
            pygame.quit()
            sys.exit()

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 500:
                self.can_shoot = True

    def laser_shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            Laser(laser_group,self.rect.midtop)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            self.laser_sound.play()


    def update(self):
        self.laser_timer()
        self.input_position()
        self.laser_shoot()
        self.meteor_collisions()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        meteor_surf = pygame.image.load('./graphics/meteor.png').convert_alpha()
        size = pygame.math.Vector2(meteor_surf.get_size()) * random.uniform(0.2,2)
        self.scaled_image = pygame.transform.scale(meteor_surf, size)
        self.image = self.scaled_image
        self.rect = self.image.get_rect(center=(random.randint(-100,window_width+100),-100))
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5), 1)
        self.speed = 100

        #mask
        self.mask = pygame.mask.from_surface(self.image)

        #rotato potato
        self.rotation = 0
        self.rotation_speed = random.randint(20,50)

    def rotate(self):
        self.rotation += self.rotation_speed * dt
        rotated_surf = pygame.transform.rotozoom(self.scaled_image, self.rotation,1)
        self.image = rotated_surf
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.rotate()
        if self.rect.top > window_height:
            self.kill()
class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)

        self.image = pygame.image.load('./graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)

        # mask
        self.mask = pygame.mask.from_surface(self.image)

        # better pos
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0,-1)
        self.speed = 600

        #sound
        self.explosion_sound= pygame.mixer.Sound("./sounds/explosion.wav")

    def meteor_collision(self):
        if pygame.sprite.spritecollide(self,meteor_group,True, pygame.sprite.collide_mask):
            self.kill()
            self.explosion_sound.play()
    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.meteor_collision()
        if self.rect.bottom < 0:
            self.kill()

class Score:
    def __init__(self):
        self.font = pygame.font.Font("./graphics/subatomic.ttf",50)

    def display(self):
        score_text = f'Score: {pygame.time.get_ticks() //1000}'
        text_surf = self.font.render(score_text,True,'white')
        text_rect = text_surf.get_rect(midbottom=(window_width/2, window_height-80))
        display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(display_surface, 'white', text_rect.inflate(30,30), width=8, border_radius=5)

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
meteor_group = pygame.sprite.Group()

# sprite creation
ship = Ship(spaceship_group)

# custom type timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 400)

#score
score = Score()

#bg music
bg_music = pygame.mixer.Sound("./sounds/music.wav")
bg_music.play()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == meteor_timer:
            Meteor(meteor_group)

    dt = clock.tick() / 1000

    # update
    spaceship_group.update()
    laser_group.update()
    meteor_group.update()

    # background
    display_surface.blit(background_surf, (0, 0))
    # graphics
    score.display()
    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)
    meteor_group.draw(display_surface)


    pygame.display.update()



