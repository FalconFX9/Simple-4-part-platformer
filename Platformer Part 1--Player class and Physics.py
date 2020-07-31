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
            if -(0.1 / SLIDING_MULTIPLIER) < self.speed_x < 0.1 / SLIDING_MULTIPLIER:
                self.speed_x = 0
            elif self.speed_x > 0:
                self.speed_x -= 0.1 / SLIDING_MULTIPLIER
            elif self.speed_x < 0:
                self.speed_x += 0.1 / SLIDING_MULTIPLIER

        self.rect.x += int(self.speed_x)
        self.rect.y += int(self.speed_y)


def game():
    player = Player(BLUE)

    player.rect.x = (SCREEN_WIDTH // 2) - 20
    player.rect.y = SCREEN_HEIGHT - player.rect.height

    sprite_group = pygame.sprite.Group()
    sprite_group.add(player)

    while True:
        screen.fill(BLACK)
        player.handle_keys()
        sprite_group.update()
        sprite_group.draw(screen)

        pygame.display.flip()
        clock.tick(GAME_SPEED)


if __name__ == '__main__':
    pygame.init()
    game()
