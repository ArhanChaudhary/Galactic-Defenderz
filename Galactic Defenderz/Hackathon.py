import pygame, random, time
width = 750
height = 750
title = 'Galactic Defenderz'
yellow = (255,255,0)
white = (255,255,255)
pygame.font.init()
font = pygame.font.SysFont('comicsans',30)

class Game:
    def __init__(self, image_path, title, width, height):
        self.title = title
        self.width = width
        self.height = height
        self.round = 0
        self.screen = pygame.display.set_mode((width,height))
        self.direction = 0
        pygame.display.set_caption(title)
        background_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(background_image, (width,height))
    def detect_collision(self,body,other_body):
        if other_body.y_pos >= body.y_pos + body.height:
            return False
        if other_body.y_pos + other_body.height <= body.y_pos:
            return False
        if other_body.x_pos >= body.x_pos + body.width:
            return False
        if other_body.x_pos + other_body.width <= body.x_pos:
            return False
        return True
    def CreateEnemy(self):
        self.player.lives = 3
        self.playerbullets = []
        self.enemybullets = []
        if self.round == 0:
            self.enemies.append(Enemy('enemy.png',425,-50,50,50,1,2,300))
            self.enemies.append(Enemy('enemy.png',275,-50,50,50,1,2,300))
        else:
            self.amount = self.round + 3 - random.randint(1,int(self.round/2)+1)
            for i in range(self.amount):
                scaling = i % 7
                rand = random.randint(1,150)
                enemy_width = 50
                enemy_height = 50
                if rand >= 140 and self.round >= 10:
                    fn = "boss.png"
                    enemy_width = 75
                    enemy_height = 75
                    enemy_speed = 0.25
                    enemy_health = 10
                    bullet_shoot_chance = 200
                elif rand >= 120 and self.round >= 7:
                    fn = "knight.png"
                    enemy_health = 3
                    enemy_speed = 0.75
                    bullet_shoot_chance = 100
                elif rand >= 80 and self.round >= 2:
                    fn = "veteran.png"
                    enemy_health = 3
                    enemy_speed = 1
                    bullet_shoot_chance = 300
                else:
                    fn = "enemy.png"
                    enemy_health = 2
                    enemy_speed = 1
                    bullet_shoot_chance = 300
                #print(scaling,-50-(50*(self.amount//7)))
                self.enemies.append(Enemy(fn,50+100*scaling,-50-100*(i//7),enemy_width,enemy_height,enemy_speed,enemy_health,bullet_shoot_chance + random.randint(int(-bullet_shoot_chance*0.9),int(bullet_shoot_chance*1.1)))) #image_path,x,y,width,height,speed,health,bullet_shoot_chance
        self.round += 1
    def run_game_loop(self):
        self.enemies = []
        self.playerbullets = []
        self.enemybullets = []
        self.round = 7
        self.mothership_health = 5
        self.game_over = False
        self.player = Player('player.png',350,650,50,50)
        self.CreateEnemy()
        while self.mothership_health > 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            self.direction = 1
                        elif event.key == pygame.K_LEFT:
                            self.direction = -1
                        elif event.key == pygame.K_SPACE:
                            if len(self.playerbullets) < 2:
                                self.playerbullets.append(Bullet(self.player.x_pos,self.player.y_pos,self.player.width,self.player.height,4,30,15))
                    elif event.type == pygame.KEYUP:
                        if (event.key == pygame.K_RIGHT and self.direction > 0) or (event.key == pygame.K_LEFT and self.direction < 0):
                            self.direction = 0
                self.screen.blit(self.image,(0,0))
                self.screen.blit(font.render("Round: "+str(self.round),True,white),(0,0))
                self.screen.blit(font.render("Lives: "+str(self.player.lives),True,white),(0,30))
                self.screen.blit(font.render("Space station health: "+str(self.mothership_health),True,white),(0,60))
                enemy_collisions = []
                for bullet in self.playerbullets:
                    bullet.move(1)
                    if bullet.y_pos + bullet.height < 0:
                        self.playerbullets[self.playerbullets.index(bullet)] = ''
                    else:
                        pygame.draw.line(self.screen,yellow,(bullet.x_pos,bullet.y_pos),(bullet.x_pos,bullet.y_pos + bullet.height),5)
                        enemy_collisions.append([self.detect_collision(bullet,enemy) for enemy in self.enemies])
                self.playerbullets = [bullet for bullet in self.playerbullets if bullet != '']
                for bullet in self.enemybullets:
                        bullet.move(-1)
                        pygame.draw.line(self.screen,yellow,(bullet.x_pos,bullet.y_pos),(bullet.x_pos,bullet.y_pos + bullet.height),5)
                self.enemybullets = [bullet for bullet in self.enemybullets if bullet != '']
                for enemy_collision in range(len(enemy_collisions)):
                    if True in enemy_collisions[enemy_collision]:
                            del self.playerbullets[enemy_collision]
                            hit_enemy = self.enemies[enemy_collisions[enemy_collision].index(True)]
                            if hit_enemy.health > 1:
                                hit_enemy.health -= 1
                            else:
                                del self.enemies[enemy_collisions[enemy_collision].index(True)]
                                enemy_collisions[enemy_collision] = [self.detect_collision(bullet,enemy) for bullet in self.playerbullets]
                self.player.move(self.direction)
                self.player.draw(self.screen)
                for enemy in self.enemies:
                    enemy.move()
                    enemy.draw(self.screen)
                    if self.detect_collision(enemy,self.player):
                        self.player.lives -= 1
                        self.enemies[self.enemies.index(enemy)] = ''
                    if enemy.y_pos >= height:
                        self.enemies[self.enemies.index(enemy)] = ''
                        self.mothership_health -= 1
                self.enemies = [enemy for enemy in self.enemies if enemy != '']
                if len(self.enemies) == 0:
                    self.CreateEnemy()
                player_collisions = [self.detect_collision(bullet,self.player) for bullet in self.enemybullets]
                if True in player_collisions:
                    self.player.lives -= 1
                    del self.enemybullets[player_collisions.index(True)]
                if self.player.lives < 1:
                    self.mothership_health -= len(self.enemies)
                    self.enemies = []
                    self.CreateEnemy()
                pygame.display.update()
        print("GAME OVER!")
class GameObject:
    def __init__(self,image_path,x,y,width,height):
        object_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(object_image, (width,height))
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height    
    def draw(self,background):
        background.blit(self.image, (self.x_pos,self.y_pos))
class Bullet(GameObject):
    def __init__(self,body_x_pos,body_y_pos,body_width,body_height,width,height,speed):
        self.x_pos = body_x_pos + body_width / 2
        self.y_pos = body_y_pos 
        self.speed = speed
        self.width = width
        self.height = height
    def move(self,y_facing):
        self.y_pos -= self.speed*y_facing
class Enemy(GameObject):
    def __init__(self,image_path,x,y,width,height,speed,health,bullet_shoot_chance):
        super().__init__(image_path,x,y,width,height)
        self.speed = speed
        self.health = health
        self.bullet_shoot_chance = bullet_shoot_chance
    def move(self):
        self.y_pos += self.speed
        if random.randint(1,self.bullet_shoot_chance) == 1:
            new_game.enemybullets.append(Bullet(self.x_pos,self.y_pos,self.width,self.height,4,20,7))
class Player(GameObject):
    def __init__(self,image_path,x,y,width,height):
        super().__init__(image_path,x,y,width,height)
        self.speed = 4
        self.lives = 3
    def move(self, x_facing):
        if width - self.width >= self.x_pos >= 0:
            self.x_pos += self.speed*x_facing
        elif self.x_pos < 0:
            self.x_pos = 0
        else:
            self.x_pos = width - self.width
while True:
    new_game = Game('background.jpeg',title, width, height)
    new_game.run_game_loop()
