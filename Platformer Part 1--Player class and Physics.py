#!/usr/bin/env python
"""
Author: Arthur Goetzke-Coburn
This is the first part in a simple, 4 part platformer
This part gives a window with a moveable player, with it's own physics.
Class templates required: Player
"""
import pygame

# Define the colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Define the size of the screen, as well as the display window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Define the display object and set the window caption
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Platformer')

# Create a clock variable, as well as a constant for the game's speed
clock = pygame.time.Clock()
GAME_SPEED = 120

# Create two multipliers that can be used for easy (and fun) modification of the game's physics
ACCELERATION_MULTIPLIER = 1
GRAVITY_MULTIPLIER = 1

# Create a friction constant that changes how slidy the player feels
FRICTION = 0.05


# Create a player class, that inherits from pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):

    def __init__(self, color):
        super().__init__()

        width = 40
        height = 40

        # Override the image and rect attributes as is requires by pygame.sprite.Sprite
        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        self.rect = self.image.get_rect()

        # Current speed of the player
        self.speed_x = 0
        self.speed_y = 0

        # This variable will be set to 1 for going left, 2 for right, and 0 for no movement
        self.direction = 0

    def handle_keys(self):
        # The event loop for the player. Since the player is the only entity requiring inputs, I decided to put
        # the event loop as part of the player class. It could easily be put in the actual game loop if needed.
        for event in pygame.event.get():
            # Check if the user tried to quit the program, if so, kill the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Check for keypresses
            elif event.type == pygame.KEYDOWN:
                key = event.key

                # Check for specific keypresses (the ones that control the player)
                if key == pygame.K_LEFT:
                    self.direction = 1
                elif key == pygame.K_RIGHT:
                    self.direction = 2
                elif key == pygame.K_UP:
                    self.jump()

            # Check if a key is let go, if so, reset the direction
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.direction = 0

    def gravity(self):
        # Makes the player feel gravity.
        # A function isn't particularly necessary, it just helps clarify the code
        self.speed_y += 0.18 * GRAVITY_MULTIPLIER

    def jump(self):
        # Makes the player jump.
        # As with the gravity function, it is not necessary to use a function here (yet)
        self.speed_y = -7

    def update_mvm(self, accel_mult, friction) -> None:
        # Overriding of the pygame.sprite.Sprite.update function, in order to have our own movement/physics

        # Apply gravity
        self.gravity()

        # Check if the player is heading out of bounds on the Y-axis
        if (self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.speed_y > 0) or (
                self.rect.y <= 0 and self.speed_y < 0):
            self.speed_y = 0

        # Check if the player is heading out of bounds on the X-axis
        if (self.rect.x + self.rect.width >= SCREEN_WIDTH and self.speed_x > 0) or (
                self.rect.x <= 0 and self.speed_x < 0):
            self.speed_x = 0

        # Apply the acceleration (depending on which key is presses)
        if self.direction == 1:
            if self.speed_x > -4:
                self.speed_x -= 0.1 * accel_mult
        elif self.direction == 2:
            if self.speed_x < 4:
                self.speed_x += 0.1 * accel_mult

        # Apply friction to gradually slow the player down when no key is pressed (only in the X-axis)
        else:
            if self.speed_x > friction:
                self.speed_x -= friction
            elif self.speed_x < -friction:
                self.speed_x += friction
            else:
                self.speed_x = 0

        # Update the position on the X-axis with the current speed
        self.rect.x += int(self.speed_x)

        # Update the position on the Y-axis with the current speed
        self.rect.y += int(self.speed_y)

    def update(self, *args, **kwargs) -> None:
        self.update_mvm(ACCELERATION_MULTIPLIER, FRICTION)


# The actual game loop
def game():
    # Create an instance of the player class
    player = Player(BLUE)

    # Give the player a starting position that is relative to the player's size and position in order to allow resizing
    player.rect.x = (SCREEN_WIDTH // 2) - (player.rect.width // 2)
    player.rect.y = SCREEN_HEIGHT - player.rect.height

    # Add the player to the sprite group. This allows us to call the draw() method.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # An infinite while loop for when the game is running
    while True:
        # Fill the screen with a background color
        screen.fill(BLACK)

        # Call the player's event loop (using the function makes the game loop clearer and cleaner)
        player.handle_keys()

        # Call the sprite group's update method (in this instance, the player's update method), then draw the player
        all_sprites.update()
        all_sprites.draw(screen)

        # Refresh the display
        pygame.display.update()

        # Limit the framerate to limit the player's visual movement speed
        clock.tick(GAME_SPEED)


# Runs the code
if __name__ == '__main__':
    # Initialize pygame
    pygame.init()
    # Run the game
    game()
