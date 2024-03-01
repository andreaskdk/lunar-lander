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

class Spaceship(pygame.sprite.Sprite):

    def __init__(self, fuel_tank):
        super().__init__()
        self.image = pygame.image.load("images/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 50
        self.speed_x = 0
        self.speed_y = 0
        self.fuel_tank = fuel_tank

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.speed_y += 0.1

    def turn_on_left_thruster(self):
        self.speed_x -= 0.1
        self.fuel_tank.fuel -= 1

    def turn_on_right_thruster(self):
        self.speed_x += 0.1
        self.fuel_tank.fuel -= 1

    def turn_on_main_thruster(self):
        self.speed_y -= 0.3
        self.fuel_tank.fuel -= 2

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.turn_on_left_thruster()
        if keys[pygame.K_DOWN]:
            self.turn_on_main_thruster()
        if keys[pygame.K_RIGHT]:
            self.turn_on_right_thruster()

    def landing_detection(self, cave):
        if self.rect.bottom>HEIGHT-30 and self.speed_y < 1 and self.speed_x < 1 and self.speed_x > -1:
            self.rect.y = HEIGHT-20
            return True
        else:
            return False

    def crash_detection(self, cave):
        if self.rect.bottom>HEIGHT-25 or self.rect.top<0 or self.rect.left<0 or self.rect.right>WIDTH:
            return True
        elif any([self.rect.clipline(p1, p2) for p1, p2 in cave.get_lines()]):
            return True
        else:
            return False


class Cave():

    def __init__(self):
        self.pad_width = 200
        self.pad_x = 300
        self.left = [(80, 0), (300, 300), (80, HEIGHT)]
        self.right = [(WIDTH-80, 0), (WIDTH-80, HEIGHT)]

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.pad_x, HEIGHT-20, self.pad_width, 20))
        for i in range(len(self.left)-1):
            pygame.draw.line(screen, (255, 255, 255), self.left[i], self.left[i+1], 5)
        for i in range(len(self.right)-1):
            pygame.draw.line(screen, (255, 255, 255), self.right[i], self.right[i+1], 5)

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
            pygame.display.flip()


    def game_play(self):
        font = pygame.font.Font(None, 74)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
            screen.fill((30, 30, 30))

            status = game.run()
            if status == "landed":
                text = font.render("You landed!", True, (255, 255, 255))
                screen.blit(text, (300, 300))
                pygame.display.flip()
                pygame.time.wait(2000)
                break
            if status == "out of fuel":
                text = font.render("Out of fuel!", True, (255, 255, 255))
                screen.blit(text, (300, 300))
                pygame.display.flip()
                pygame.time.wait(2000)
                break
            if status == "crashed":
                text = font.render("You crashed!", True, (255, 255, 255))
                screen.blit(text, (300, 300))
                pygame.display.flip()
                pygame.time.wait(2000)
                break
            pygame.display.flip()
            self.clock.tick(self.fps)
        self.show_splash_screen()


    def run(self):
        if self.spaceship.landing_detection(self.cave):
            return "landed"
        if self.fuel_tank.fuel <= 0:
            return "out of fuel"
        if self.spaceship.crash_detection(self.cave):
            return "crashed"

        self.spaceship.get_input()
        self.spaceship.update()
        self.cave.draw(self.screen)
        self.spaceship_group.draw(self.screen)
        self.fuel_tank.draw(self.screen)
        return ""




if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    game = Game(screen)
    game.show_splash_screen()

    pygame.quit()
    quit()