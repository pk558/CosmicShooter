from sre_parse import HEXDIGITS
import pygame
import time
import random
import threading 
WIDTH = 800
HEIGHT = 600

class Background(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, pos: tuple):
        super(Background, self).__init__()
        self.image = pygame.image.load("images/background.jpg").convert()
        self.image = pygame.transform.smoothscale(self.image, (width, height))
        self.image.set_alpha(245)
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def update(self):
        pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, width: int, height: int, level: str):
        super(Enemy, self).__init__()
        self.image = pygame.image.load("images/enemies/chicken_1.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0] + random.randrange(0, WIDTH - self.image.get_width()), pos[1])
        self.prev_time = time.time()
        self.speed = random.SystemRandom().uniform(.25, .5)
        self.hp = 100
    def update(self):
        now = time.time()
        dt = now - self.prev_time
        self.prev_time = now
        self.moving_speed = (self.speed * dt) * 1000
        self.rect.center = (self.rect.center[0], self.rect.center[1] + self.moving_speed)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, pos: tuple):
        super(Bullet, self).__init__()
        self.image = pygame.image.load("images/bullets/01.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (width, height))
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.prev_time = time.time()
        self.speed = 2.5
    def update(self):
        now = time.time()
        dt = now - self.prev_time
        self.prev_time = now
        shoot_speed = (self.speed * dt) * 1000
        self.rect.center = (self.rect.center[0], self.rect.center[1] - shoot_speed)
class Player(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, pos: tuple):
        super(Player, self).__init__()
        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.prev_time = time.time()
        self.player_speed = 1
        self.player_ammunition_max = 50
        self.player_ammunition = 50
        self.bullet_group = pygame.sprite.RenderPlain()
    def update(self):
        keys = pygame.key.get_pressed()
        now = time.time()
        dt = (now - self.prev_time)*1000
        self.prev_time = now
        playerMove = self.player_speed * dt
        if keys[pygame.K_w]:
            if self.rect.y > 0+self.rect.height//2:
                self.rect.center = (self.rect.center[0], self.rect.center[1] - playerMove)
        if keys[pygame.K_s]:
            if self.rect.y < HEIGHT-self.rect.height:
                self.rect.center = (self.rect.center[0], self.rect.center[1] + playerMove)
        if keys[pygame.K_a]:
            if self.rect.x > 0:
                self.rect.center = (self.rect.center[0] - playerMove, self.rect.center[1]) 
        if keys[pygame.K_d]:
            if self.rect.x < WIDTH-self.rect.width:
                self.rect.center = (self.rect.center[0] + playerMove, self.rect.center[1])
        
        if keys[pygame.K_SPACE]:
            if self.player_ammunition > 0:
                bullet = Bullet(100, 100, (self.rect.center[0], self.rect.y))
                new_game.bullets.append(bullet)
                self.bullet_group.add(bullet)
                self.player_ammunition -= 1
        if keys[pygame.K_r]:
            self.player_ammunition = self.player_ammunition_max
        self.bullet_group.draw(new_game.screen)
        self.bullet_group.update()
        
        #----


class Game():
    def __init__(self, WIDTH, HEIGHT):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        #time/deltatime
        self.prev_time = time.time()
        self.dt = 0
        #sprites init
        self.background = Background(WIDTH, HEIGHT, (WIDTH//2,HEIGHT//2))
        self.player = Player(WIDTH//12, HEIGHT//8, (WIDTH//2,HEIGHT-HEIGHT//8))
        #sprites
        self.group = pygame.sprite.RenderPlain()
        self.ammo_group = pygame.sprite.RenderPlain()
        self.level_group = pygame.sprite.RenderPlain()
        self.group.add(self.background)
        self.group.add(self.player)
        #font
        self.font = pygame.font.SysFont("Comic Sans", 45)
        #player
        self.bullets = []
        self.enemies = []
        #run
        self.run = True
    def Run(self):
        Level(5).update()
        while self.run:
            #print(self.bullets)
            keys = pygame.key.get_pressed()
            pygame.time.Clock().tick(144)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            self.group.draw(self.screen)
            self.group.update()
            #print(self.level_group)
            self.level_group.draw(self.screen)
            self.level_group.update()
            

            if keys[pygame.K_q]:
                Level(random.randrange(1, 15)).update()
            if self.player.player_ammunition > 0:
                self.screen.blit(pygame.transform.rotate(pygame.image.load("images/bullets/01.png"), 90), (10, -40))
                self.screen.blit(self.font.render(""+str(self.player.player_ammunition), True, (255,255,255)), (100,10))
            elif self.player.player_ammunition == 0:
                self.screen.blit(self.font.render("You have run out of ammo, press R to reload!", True, (255,255,255)), (0,0))
            pygame.display.update()
    def checkCollision(self, sprite1, sprite2):
        col = pygame.sprite.collide_rect(sprite1, sprite2)
        if col == True:
            print("trafiono")
class Level():
    def __init__(self, level):
        self.level = level
    def update(self):
        for i in range(0, self.level):
            enemy = Enemy((0,0), int(WIDTH*.05), int(HEIGHT*.05), str(self.level))
            new_game.enemies.append(enemy)
            new_game.level_group.add(enemy)


new_game = Game(WIDTH, HEIGHT)
new_game.Run()