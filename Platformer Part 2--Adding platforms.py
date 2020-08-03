#!/usr/bin/env python
import pygame

# Define the colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Define the size of the screen, as well as the display window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Platformer')

clock = pygame.time.Clock()
GAME_SPEED = 120

GRAVITY_MULTIPLIER = 1
SLIDING_MULTIPLIER = 1


class Player(pygame.sprite.Sprite):

    def __init__(self, color):
        super().__init__()

        width = 40
        height = 40

        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        self.rect = self.image.get_rect()

        # Current speed of the player
        self.speed_x = 0
        self.speed_y = 0

        # This variable will be set to 1 for going left, 2 for right, and 0 for no movement
        self.direction = 0

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                key = event.key

                if key == pygame.K_LEFT:
                    self.direction = 1
                elif key == pygame.K_RIGHT:
                    self.direction = 2
                elif key == pygame.K_UP:
                    self.jump()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.direction = 0

    def gravity(self):
        self.speed_y += 0.18 * GRAVITY_MULTIPLIER

        if (self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.speed_y > 0) or (self.rect.y <= 0 and self.speed_y < 0):
            self.speed_y = 0

    def jump(self):
        self.rect.y += 2
        #touching_platform = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.y -= 2
        self.speed_y = -7

    def update(self):
        self.gravity()

        if (self.rect.x + self.rect.width >= SCREEN_WIDTH and self.speed_x > 0) or (self.rect.x <= 0 and self.speed_x < 0):
            self.speed_x = 0

        if self.direction == 1:
            if self.speed_x > -4:
                self.speed_x -= 0.1 / SLIDING_MULTIPLIER
        elif self.direction == 2:
            if self.speed_x < 4:
                self.speed_x += 0.1 / SLIDING_MULTIPLIER
        else:
            if -(0.1 / SLIDING_MULTIPLIER) < self.speed_x < 0.1 * SLIDING_MULTIPLIER:
                self.speed_x = 0
            elif self.speed_x > 0:
                self.speed_x -= 0.1 / SLIDING_MULTIPLIER
            elif self.speed_x < 0:
                self.speed_x += 0.1 / SLIDING_MULTIPLIER

        self.rect.x += int(self.speed_x)
        self.rect.y += int(self.speed_y)


class Platform(pygame.sprite.Sprite):

    def __init__(self, width, x, y):
        super().__init__()
        self.image = pygame.Surface((width, 10))
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def level(all_sprites_group, platform_group):
    platforms = []
    platforms.append(Platform(50, 450, 50))
    platforms.append(Platform(100, 350, 100))
    platforms.append(Platform(80, 200, 150))
    platforms.append(Platform(50, 100, 200))
    platforms.append(Platform(80, 320, 210))
    platforms.append(Platform(60, 130, 250))
    platforms.append(Platform(150, 0, 320))
    platforms.append(Platform(80, 260, 400))
    platforms.append(Platform(60, 420, 460))
    platforms.append(Platform(100, 620, 500))
    platforms.append(Platform(40, 800, 580))
    platforms.append(Platform(60, 600, 610))
    platforms.append(Platform(100, 650, 700))
    for platform in platforms:
        all_sprites_group.add(platform)
        platform_group.add(platform)


def game():
    player = Player(BLUE)

    player.rect.x = (SCREEN_WIDTH // 2) - 20
    player.rect.y = SCREEN_HEIGHT - player.rect.height

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    platform_group = pygame.sprite.Group()
    level(all_sprites, platform_group)

    while True:
        screen.fill(BLACK)
        player.handle_keys()
        player.update()
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(GAME_SPEED)


if __name__ == '__main__':
    pygame.init()
    game()
