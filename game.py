
import pygame
import time
import random

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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, width: int, height: int):
        super(Enemy, self).__init__()
        self.image = pygame.image.load("images/enemies/chicken_1.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0] + random.randrange(0, WIDTH - self.image.get_width()), pos[1])
        self.prev_time = time.time()
        self.speed = random.SystemRandom().uniform(.25, .30)
        self.hp = 100
    def update(self):
        self.is_player_hitted()
        now = time.time()
        dt = now - self.prev_time
        self.prev_time = now
        self.moving_speed = (self.speed * dt) * 1000
        self.rect.center = (self.rect.center[0], self.rect.center[1] + self.moving_speed)
    def is_player_hitted(self):
        for id, enemy in enumerate(new_game.enemies):
            if new_game.checkCollision(enemy, new_game.player):
                if new_game.player.player_lives > 0: 
                    new_game.player.player_lives -= 1
                    new_game.enemies.remove(enemy)
                    enemy.kill()
                else:
                    print("game over")
                
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
        self.is_bullet_outside_screen()
        self.is_enemy_hitted()
        now = time.time()
        dt = now - self.prev_time
        self.prev_time = now
        shoot_speed = (self.speed * dt) * 1000
        self.rect.center = (self.rect.center[0], self.rect.center[1] - shoot_speed)
    def is_bullet_outside_screen(self):
        for id, bullet in enumerate(new_game.bullets):
            if bullet.rect.center[1] < 0:
                new_game.bullets.remove(bullet)
                new_game.player.bullet_group.remove(bullet)
    def is_enemy_hitted(self):
        for id, enemy in enumerate(new_game.enemies):
            if new_game.checkCollision(enemy, self):
                new_game.enemies.remove(enemy)
                enemy.kill()
        
class Player(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, pos: tuple):
        super(Player, self).__init__()
        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.prev_time = time.time()
        self.player_speed = 1.25
        self.player_ammunition_max = 20000
        self.player_ammunition = 20000
        self.player_lives = 10
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
        pygame.mixer.init()
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
        #images
        self.bullet_image = pygame.image.load("images/bullets/01.png").convert_alpha()
        self.hearth_image = pygame.transform.smoothscale(pygame.image.load("images/hearth.png").convert_alpha(), (int(WIDTH*.05), int(HEIGHT*.05)))
        #sounds
        self.shoot_sound = pygame.mixer.Sound("sounds/shoot_sound.wav")
    def Run(self):
        Level(5).update()
        while self.run:
            print(len(self.enemies))
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

            if self.player.player_lives > 0:
                self.screen.blit(self.hearth_image, (50, 50))
                self.screen.blit(self.font.render(""+str(self.player.player_lives), True, (255,255,255)), (100,50))
            if self.player.player_ammunition > 0:
                self.screen.blit(pygame.transform.rotate(self.bullet_image, 90), (10, -40))
                self.screen.blit(self.font.render(""+str(self.player.player_ammunition), True, (255,255,255)), (100,10))
            elif self.player.player_ammunition == 0:
                self.screen.blit(self.font.render("You have run out of ammo, press R to reload!", True, (255,255,255)), (0,0))
            pygame.display.update()
    def checkCollision(self, sprite1, sprite2):
        return pygame.sprite.collide_rect(sprite1, sprite2)
class Level():
    def __init__(self, level):
        self.level = level
    def update(self):
        for i in range(0, self.level):
            enemy = Enemy((0,0), int(WIDTH*.04), int(WIDTH*.04))
            new_game.enemies.append(enemy)
            new_game.level_group.add(enemy)


new_game = Game(WIDTH, HEIGHT)
new_game.Run()