import pygame
from random import randrange, choice

pygame.init()
height = 500
width = 500
FPS = 60
clock = pygame.time.Clock()
pygame.display.set_caption('Road Fighter')
window = pygame.display.set_mode((width, height))
main_font = pygame.font.SysFont('comicsans', 30, bold=True)

class Background:
    text_font = pygame.font.SysFont('comicsans', 16)
    def __init__(self):
        self.road_img = pygame.transform.scale(pygame.image.load('assets/road_image.png'), (width, height))
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = -self.road_img.get_height()
        self.moving_speed = 3
        self.track = pygame.transform.scale(pygame.image.load('assets/Road_Fighter_Player.png'), (20, 20))
        self.track_y_pos = height-90

    def update(self):
        self.y1 += self.moving_speed
        self.y2 += self.moving_speed
        if self.y1 >= self.road_img.get_height():
            self.y1 = -self.road_img.get_height()
        if self.y2 >= self.road_img.get_height():
            self.y2 = -self.road_img.get_height()

    def render(self):
        window.blit(self.road_img, (self.x1, self.y1))
        window.blit(self.road_img, (self.x2, self.y2))
        window.blit(self.track, (22, self.track_y_pos))

    def finish_line(self):
        pygame.draw.line(window, (255, 0, 0), (19, height - 75), (43, height - 75))
        text_font = self.text_font.render('Start', True, (0, 255, 255))
        window.blit(text_font, (19, height - 70))
        pygame.draw.line(window, (255, 0, 0), (19, 70), (43, 70))
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player_img = pygame.transform.scale(pygame.image.load('assets/Road_Fighter_Player.png'), (50, 40))
        self.mask = pygame.mask.from_surface(self.player_img)
        self.moving_speed = 0.3

    def draw(self):
        window.blit(self.player_img, (self.x, self.y))

    def move(self):
        if self.y > 5:
            self.y -= self.moving_speed
class Enemy:
    enemy_car_map = {"green_car": pygame.transform.scale(pygame.image.load('assets/green_car.png'), (28, 42)),
                     "yellow_car": pygame.transform.scale(pygame.image.load('assets/yellow_car.png'), (25, 35)),
                     "blue_car": pygame.transform.scale(pygame.image.load('assets/blue_car.png'), (25, 35))}
    def __init__(self, x, y, img):
        enemy_speed_list = [-1.5, 1, 1.5, 2]
        self.x = x
        self.y = y
        self.img = self.enemy_car_map[img]
        self.mask = pygame.mask.from_surface(self.img)
        self.moving_speed = choice(enemy_speed_list)

    def draw(self):
        window.blit(self.img, (self.x, self.y))

    def move(self):
        self.y -= self.moving_speed
    
    def off_screen(self):
        if self.y < 0 or self.y > height:
            return True
def colllide(obj1, obj2):
    offset_x = int(obj1.x - obj2.x)
    offset_y = int(obj1.y - obj2.y)
    if obj1.mask.overlap(obj2.mask, (offset_x+20, offset_y)):
        return True
def gameover():
    gameover_img = pygame.transform.scale(pygame.image.load('assets/gameover.png'), (width, height))
    window.blit(gameover_img, (0,0))
    gameover_label = main_font.render('Click anywhere to exit the game...', True, (255, 255, 250))
    window.blit(gameover_label, ((width / 2 - gameover_label.get_width() / 2), height / 2 + 200))
    pygame.display.update()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                quit()
def win():
    win_img = pygame.transform.scale(pygame.image.load('assets/win.png'), (width, height))
    window.blit(win_img, (0, 0))
    win_label = main_font.render('Click anywhere to exit the game...', True, (255, 255, 250))
    window.blit(win_label, ((width / 2 - win_label.get_width() / 2), height / 2 + 200))
    pygame.display.update()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                quit()

bg = Background()
player = Player(240, 300)
enemy_list = []
enemy_show_point = [0, height]

def main():
    lost = False
    finish_race = False

    while not lost:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        bg.update()
        bg.render()
        player.draw()
        player.move()

        bg.finish_line()
        bg.track_y_pos -= 0.3

        if bg.track_y_pos < 70:
            pygame.draw.line(window, (255, 0, 0), (150, bg.y1), (295, bg.y1))
            if player.y <= bg.y1:
                finish_race = True

        if len(enemy_list) < 3:
            enemy = Enemy(randrange(150, 250), choice(enemy_show_point), choice(["green_car", "yellow_car", "blue_car"]))
            enemy_list.append(enemy)

        for enemy in enemy_list:
            enemy.draw()
            enemy.move()
            if enemy.off_screen():
                enemy_list.remove(enemy)
            if colllide(player, enemy):
                finish_race = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and player.x < 260:
            player.x += 5
        elif keys[pygame.K_LEFT] and player.x > 130:
            player.x -= 5
        elif keys[pygame.K_UP] and player.y > 0:
            player.y -= 5
        elif keys[pygame.K_DOWN] and player.y < height - + player.player_img.get_height():
            player.y += 5

        if finish_race == True:
            win()

        pygame.display.update()
        clock.tick(FPS)

def main_menu():
    main_menu_bk = pygame.transform.scale(pygame.image.load('assets/main_menu_bg.png'), (width, height))
    window.blit(main_menu_bk, (0, 0))
    main_label = main_font.render('Click anywhere to enter the game...', True, (255, 255, 250))
    window.blit(main_label, ((width/2 - main_label.get_width()/2), height/2+50))
    pygame.display.update()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main()



main_menu()


