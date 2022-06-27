from tkinter import CENTER
import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        player_run_1 = pygame.image.load('image/luna1.png').convert_alpha()
        player_run_2 = pygame.image.load('image/luna2.png').convert_alpha()
        player_run_3 = pygame.image.load('image/luna3.png').convert_alpha()
        player_run_4 = pygame.image.load('image/luna4.png').convert_alpha()
        self.player_run = [player_run_1, player_run_2, player_run_3, player_run_4]
        self.player_index = 0
        self.player_jump = pygame.image.load('image/lunajump1.png').convert_alpha()

        self.image = self.player_run[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.wav')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_run): self.player_index = 0
            self.image = self.player_run[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'raven':
            raven_1 = pygame.image.load('image/raven1.png').convert_alpha()
            raven_2 = pygame.image.load('image/raven2.png').convert_alpha()
            raven_3 = pygame.image.load('image/raven3.png').convert_alpha()
            raven_4 = pygame.image.load('image/raven4.png').convert_alpha()
            self.frames = [raven_1, raven_2, raven_3, raven_4]
            y_pos = 210
        else:
            spider_1 = pygame.image.load('image/spider1.png').convert_alpha()
            spider_2 = pygame.image.load('image/spider2.png').convert_alpha()
            spider_3 = pygame.image.load('image/spider3.png').convert_alpha()
            spider_4 = pygame.image.load('image/spider4.png').convert_alpha()
            self.frames = [spider_1, spider_2, spider_3, spider_4]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score = game_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score.get_rect(center = (700, 50))
    screen.blit(score, score_rect)
    return current_time

def obstacle_move(obstacle_list):
    if obstacle_list:
        for obstacle in obstacle_list:
            obstacle.x -= 5

            if obstacle.bottom == 300:
                screen.blit(spider, obstacle)
            else:
                screen.blit(raven, obstacle)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]  # obstacle kill point
        return obstacle_list
    else: return []

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_run): 
            player_index = 0
        player_surf = player_run[int(player_index)]


# initialize pygame
pygame.init()
# create a display surface
screen = pygame.display.set_mode((800, 400))
# set caption
pygame.display.set_caption('MissGuided - Endless Runner')
# set icon
icon = pygame.image.load('image/luna1.png').convert_alpha()
pygame.display.set_icon(icon)
# clock object for setting framerate
clock = pygame.time.Clock()
# text font
game_font = pygame.font.Font('font/Minecraft.ttf', 40)
# game state
game_active = False
start_time = 0
score = 0

background_music = pygame.mixer.Sound('audio/MissGuided.wav')
background_music.play(loops = -1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

###             SURFACE
# background
title_text = game_font.render('MissGuided', False, 'Black')
sky = pygame.image.load('image/sky.png').convert()
ground = pygame.image.load('image/ground.png').convert()

# enemies
spider_1 = pygame.image.load('image/spider1.png').convert_alpha()
spider_2 = pygame.image.load('image/spider2.png').convert_alpha()
spider_3 = pygame.image.load('image/spider3.png').convert_alpha()
spider_4 = pygame.image.load('image/spider4.png').convert_alpha()
spider_frames = [spider_1, spider_2, spider_3, spider_4]
spider_frame_index = 0
spider = spider_frames[spider_frame_index]

raven_1 = pygame.image.load('image/raven1.png').convert_alpha()
raven_2 = pygame.image.load('image/raven2.png').convert_alpha()
raven_3 = pygame.image.load('image/raven3.png').convert_alpha()
raven_4 = pygame.image.load('image/raven4.png').convert_alpha()
raven_frames = [raven_1, raven_2, raven_3, raven_4]
raven_frame_index = 0
raven = raven_frames[raven_frame_index]

# player
player_run_1 = pygame.image.load('image/luna1.png').convert_alpha()
player_run_2 = pygame.image.load('image/luna2.png').convert_alpha()
player_run_3 = pygame.image.load('image/luna3.png').convert_alpha()
player_run_4 = pygame.image.load('image/luna4.png').convert_alpha()
player_run = [player_run_1, player_run_2, player_run_3, player_run_4]
player_index = 0

player_jump = pygame.image.load('image/lunajump1.png').convert_alpha()
#player_jump_2 = pygame.image.load('image/lunajump2.png').convert_alpha()
#player_jump = [player_jump_1, player_jump_2]

player_surf = player_run[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300))
gravity = 0

# game over screen
player_stand = pygame.image.load('image/luna1.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)  # source, rotation, scale
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = game_font.render('MissGuided', False,(111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = game_font.render('Press Space to Run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 320))

obstacle_list = []

#   Timer / Custom events
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)


spider_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(spider_animation_timer, 500)

raven_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(raven_animation_timer, 200)


while True:
    # check if user closes the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            # detect mouseclick
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    gravity = -20
            # detect spacebar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:     # K_SPACE = spacebar
                    gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True 
                start_time = int(pygame.time.get_ticks() / 1000)

        # custom events (timers)
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['raven', 'spider', 'spider', 'spider'])))
                

            if event.type == spider_animation_timer:
                if spider_frame_index == 0: spider_frame_index = 1
                elif spider_frame_index == 1: spider_frame_index = 2
                elif spider_frame_index == 2: spider_frame_index = 3
                else: spider_frame_index = 0
                spider = spider_frames[spider_frame_index]

            if event.type == raven_animation_timer:
                if raven_frame_index == 0: raven_frame_index = 1
                elif raven_frame_index == 1: raven_frame_index = 2
                elif raven_frame_index == 2: raven_frame_index = 3
                else: raven_frame_index = 0
                raven = raven_frames[raven_frame_index]

    if game_active:
        # block image transfer (to display surface)
        screen.blit(sky, (0,0))
        screen.blit(ground, (0,300))
        screen.blit(title_text,(50,50))
        #pygame.draw.rect(screen, 'Pink', score_rect)
        #screen.blit(score, score_rect)
        score = display_score()

        #spider_rect.x -= 7
        #if spider_rect.right <= 0: spider_rect.left = 800
        #screen.blit(spider, spider_rect)

        # player
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # obstacle movement
        #obstacle_list = obstacle_move(obstacle_list)

        # collisions
        game_active = collision_sprite()

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_list.clear()
        player_rect.midbottom = (80,300)
        gravity = 0
        
        screen.blit(game_name, game_name_rect)
        score_message = game_font.render(f'Your score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))

        if score > 0:
            screen.blit(score_message, score_message_rect)
        else:
            screen.blit(game_message, game_message_rect)
        
        


    # keep updating everything
    pygame.display.update()
    clock.tick(60)  # -> set maximum framerate to 60 fps
