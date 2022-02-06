from sre_parse import HEXDIGITS
import pygame
import time
WIDTH = 1300
HEIGHT = 700

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

class Player(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, pos: tuple):
       super(Player, self).__init__()
       self.image = pygame.image.load("images/player.png").convert_alpha()
       self.image = pygame.transform.smoothscale(self.image, (width, height))
       self.rect = self.image.get_rect()
       self.rect.center = pos
       self.prev_time = time.time()
       self.player_speed = 1
    def update(self):
        #steering
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
        self.group.add(self.background)
        self.group.add(self.player)
        
        #run
        self.run = True
    def Run(self):
        while self.run:
            pygame.time.Clock().tick(144)
            self.group.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            self.player.update()
            pygame.display.update()
new_game = Game(WIDTH, HEIGHT)
new_game.Run()