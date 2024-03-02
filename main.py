"""

This is a lunar lander game created with pygame. The goal of the game is to land
a small spaceship on the moon. The spaceship is affected by gravity and has three
thrusters to control its movement. The game is over when the spaceship crashes or lands
safely on the landing pad. The spaceship has limited fuel and the player must use it wisely.

The is controlled with the following keys:
- Left arrow: turn on the left thruster
- Right arrow: turn on the right thruster
- Down arrow: turn on the main thruster

"""

import pygame

HEIGHT = 800
WIDTH = 800


def point_distance(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5

def point_dot_product(p1, p2):
    return p1[0]*p2[0] + p1[1]*p2[1]

def point_subtraction(p1, p2):
    return (p1[0]-p2[0], p1[1]-p2[1])

def triangle_area(p1, p2, p3):
    return abs((p1[0]*(p2[1]-p3[1]) + p2[0]*(p3[1]-p1[1]) + p3[0]*(p1[1]-p2[1]))/2)

def circle_line_collision(p1, p2, c, r):
    max_dist = max(point_distance(p1, c), point_distance(p2, c))
    if point_dot_product(point_subtraction(c, p1), point_subtraction(p2, p1)) > 0 \
            and point_dot_product(point_subtraction(c, p2), point_subtraction(p1, p2)) > 0:
        min_dist = triangle_area(p1, p2, c)*2/point_distance(p1, p2)
    else:
        min_dist = min(point_distance(p1, c), point_distance(p2, c))
    if min_dist < r and max_dist > r:
        return True
    return False


class Spaceship(pygame.sprite.Sprite):

    def __init__(self, fuel_tank):
        super().__init__()
        self.i_float = pygame.image.load("images/float.png")
        self.i_left = pygame.image.load("images/left.png")
        self.i_right = pygame.image.load("images/right.png")
        self.i_main = pygame.image.load("images/main.png")

        self.image = self.i_float
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 50
        self.speed_x = 0
        self.speed_y = 0
        self.fuel_tank = fuel_tank

    def get_collision_circle(self):
        return (self.rect.x+59, self.rect.y+57), 53

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.speed_y += 0.1

    def turn_on_left_thruster(self):
        self.image = self.i_right
        self.speed_x -= 0.1
        self.fuel_tank.fuel -= 1

    def turn_on_right_thruster(self):
        self.image = self.i_left
        self.speed_x += 0.1
        self.fuel_tank.fuel -= 1

    def turn_on_main_thruster(self):
        self.image = self.i_main
        self.speed_y -= 0.3
        self.fuel_tank.fuel -= 2

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.turn_on_left_thruster()
        elif keys[pygame.K_DOWN]:
            self.turn_on_main_thruster()
        elif keys[pygame.K_RIGHT]:
            self.turn_on_right_thruster()
        else:
            self.image = self.i_float

    def landing_detection(self, cave):
        if self.rect.bottom>HEIGHT-30 and self.speed_y < 10 and self.speed_x < 10 and self.speed_x > -10:
            self.rect.y = HEIGHT-20
            return True
        else:
            return False

    def crash_detection(self, cave):
        c, r = self.get_collision_circle()
        if self.rect.bottom>HEIGHT-25 or self.rect.top<0 or self.rect.left<0 or self.rect.right>WIDTH:
            return True
        elif any([circle_line_collision(p1, p2, c, r) for p1, p2 in cave.get_lines()]):
            return True
        else:
            return False


class Cave():


    def __init__(self,
                 pad_width=200,
                 pad_x=300,
                 left=((80, 0), (300, 300), (80, HEIGHT-100), (300, HEIGHT)),
                 right=((WIDTH-80, 0), (WIDTH-80, HEIGHT-100), (500, HEIGHT))):
        self.pad_width = pad_width
        self.pad_x = pad_x
        self.left = left
        self.right = right
        self.i_rock = pygame.PixelArray(pygame.image.load("images/vertical_rock_face_close_up.png"))
        self.i_space_bg = pygame.PixelArray(pygame.image.load("images/outer_space_black_with_a_few_stars_dim.png"))
        img_size=self.i_rock.shape[0]
        for j in range(img_size):
            pl1 = list(filter(lambda x: x[1]/HEIGHT <= j/img_size, self.left))[-1]
            pl2 = list(filter(lambda x: x[1]/HEIGHT > j/img_size, self.left))[0]
            l = (pl1[0] + (pl2[0]-pl1[0])*(j*HEIGHT/img_size-pl1[1])/(pl2[1]-pl1[1]))*img_size/WIDTH
            pr1 = list(filter(lambda x: x[1] / HEIGHT <= j / img_size, self.right))[-1]
            pr2 = list(filter(lambda x: x[1] / HEIGHT > j / img_size, self.right))[0]
            r = (pr1[0] + (pr2[0] - pr1[0]) * (j * HEIGHT / img_size - pr1[1]) / (pr2[1] - pr1[1])) * img_size / WIDTH
            for i in range(img_size):
                if i < l or i > r:
                    self.i_space_bg[i, j] = self.i_rock[i, j]


        self.cave_img = pygame.transform.scale(self.i_space_bg.make_surface(), (WIDTH, HEIGHT))
        #print(self.i_rocks.ndim)

    def draw(self, screen):
        screen.blit(self.cave_img, (0, 0))
        line_color = (25, 25, 25)
        pygame.draw.rect(screen, (16,60,70), (self.pad_x, HEIGHT-20, self.pad_width, 20))
        for i in range(len(self.left)-1):
            pygame.draw.line(screen, line_color, self.left[i], self.left[i+1], 3)
        for i in range(len(self.right)-1):
            pygame.draw.line(screen, line_color, self.right[i], self.right[i+1], 3)

    def get_lines(self):
        lines = []
        for i in range(len(self.left)-1):
            lines.append((self.left[i], self.left[i+1]))
        for i in range(len(self.right)-1):
            lines.append((self.right[i], self.right[i+1]))
        return lines


class FuelTank():

    def __init__(self):
        self.fuel = 1000

    def draw(self, screen):
        pygame.draw.rect(screen, (25, 255, 25), (20, 20, 20, self.fuel / 10 * 2))

class Game():

    def __init__(self, screen):
        self.splash_image = pygame.transform.scale(pygame.image.load('images/splash.png'), (WIDTH,HEIGHT))
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.fuel_tank = FuelTank()
        self.spaceship = Spaceship(self.fuel_tank)
        self.spaceship_group = pygame.sprite.Group()
        self.spaceship_group.add(self.spaceship)
        self.cave = Cave()



    def reset(self):
        self.fuel_tank = FuelTank()
        self.spaceship = Spaceship(self.fuel_tank)
        self.spaceship_group = pygame.sprite.Group()
        self.spaceship_group.add(self.spaceship)
        self.cave = Cave()

    def show_splash_screen(self):
        showing_splash_screen = True
        while showing_splash_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.reset()
                self.game_play()
                break
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.splash_image, (0, 0))
            font = pygame.font.Font(None, 74)
            text = font.render("Press SPACE to play", True, (255, 255, 255))
            screen.blit(text, (WIDTH/2-text.get_width()/2, HEIGHT-50))
            pygame.display.flip()


    def game_play(self):
        font = pygame.font.Font(None, 74)
        running = True
        status=""
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
            if status == "landed":
                text = font.render("You landed!", True, (255, 255, 255))
                screen.blit(text, (WIDTH/2-text.get_width()/2, 300))
                pygame.display.flip()
                pygame.time.wait(2000)
                break
            if status == "out of fuel":
                text = font.render("Out of fuel!", True, (255, 255, 255))
                screen.blit(text, (WIDTH/2-text.get_width()/2, 300))
                pygame.display.flip()
                pygame.time.wait(2000)
                break
            if status == "crashed":
                text = font.render("You crashed!", True, (255, 255, 255))
                screen.blit(text, (WIDTH/2-text.get_width()/2, 300))
                pygame.display.flip()
                pygame.time.wait(2000)
                break

            screen.fill((30, 30, 30))
            status = game.run()
            pygame.display.flip()
            self.clock.tick(self.fps)
        self.show_splash_screen()


    def run(self):
        self.spaceship.get_input()
        self.spaceship.update()
        self.cave.draw(self.screen)
        self.spaceship_group.draw(self.screen)
        self.fuel_tank.draw(self.screen)

        if self.spaceship.landing_detection(self.cave):
            return "landed"
        if self.fuel_tank.fuel <= 0:
            return "out of fuel"
        if self.spaceship.crash_detection(self.cave):
            return "crashed"

        return ""




if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    game = Game(screen)
    game.show_splash_screen()

    pygame.quit()
    quit()