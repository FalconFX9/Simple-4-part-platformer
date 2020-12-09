#!/usr/bin/env python
"""
Author: Arthur Goetzke-Coburn
This is the fourth and final part in the 4-part platformer.
In this part, we add a victory/reset screen for when the player beats the level we made, as well as adding some
multipliers for the user to play with.
"""
import pygame
from PIL import ImageColor

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

# Create three multipliers that can be used for easy (and fun) modification of the game's physics
ACCELERATION_MULTIPLIER = 5
GRAVITY_MULTIPLIER = 1
JUMP_MULTIPLIER = 1

# Create a friction constant that changes how slidy the player feels
FRICTION = 0.1

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

        # Create the prev_rect variable that will be used to store the position from the previous update cycle
        self.prev_rect = self.rect

        # Current speed of the player
        self.speed_x = 0
        self.speed_y = 0

        # This variable will be set to 1 for going left, 2 for right, and 0 for no movement
        self.direction = 0

        # Create a variable that will hold the platform group
        self.platforms = None

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
        # Now that jumping is more complex, a function makes more sense

        # Move the player down 2 pixels in order to make sure that the platform detection is accurate
        self.rect.y += 2
        # Check if the player is touching any platforms
        touching_platform = pygame.sprite.spritecollide(self, self.platforms, False)
        # Move the player back up to it's original position after collisions have been checked
        self.rect.y -= 2
        # Only allow jumping if the player is touching a platform or is on the bottom of the window
        if len(touching_platform) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y = -(7 * JUMP_MULTIPLIER)

    def update(self):
        # Overriding of the pygame.sprite.Sprite.update function, in order to have our own movement/physics

        # Apply gravity
        self.gravity()

        # Check if the player is heading out of bounds on the Y-axis
        if (self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.speed_y > 0) or (self.rect.y <= 0 and self.speed_y < 0):
            self.speed_y = 0

        # Check if the player is heading out of bounds on the X-axis
        if (self.rect.x + self.rect.width >= SCREEN_WIDTH and self.speed_x > 0) or (self.rect.x <= 0 and self.speed_x < 0):
            self.speed_x = 0

        # Apply the acceleration (depending on which key is presses)
        if self.direction == 1:
            if self.speed_x > -4:
                self.speed_x -= 0.1 * ACCELERATION_MULTIPLIER
        elif self.direction == 2:
            if self.speed_x < 4:
                self.speed_x += 0.1 * ACCELERATION_MULTIPLIER

        # Apply friction to gradually slow the player down when no key is pressed (only in the X-axis)
        else:
            if self.speed_x > FRICTION:
                self.speed_x -= FRICTION
            elif self.speed_x < -FRICTION:
                self.speed_x += FRICTION
            else:
                self.speed_x = 0


        # Update the position on the X-axis with the current speed
        self.rect.x += int(self.speed_x)

        # Check for collisions with platforms
        # This first check happens after the X-axis position was updated, and as such, it checks for collisions
        # between the side of the platforms and the sides of the player

        # Check for collisions with the spritecollide function
        collided_platforms = pygame.sprite.spritecollide(self, self.platforms, False)
        # For every platform hit, checks if the player was going right or left, and set the position of the player
        # (right or left side) to the right or left side of the hit platform, as well as reset the horizontal speed to 0
        for platform in collided_platforms:
            if self.speed_x > 0:
                self.rect.right = platform.rect.left
            elif self.speed_x < 0:
                self.rect.left = platform.rect.right

            self.speed_x = 0

        # Update the position on the Y-axis with the current speed
        self.rect.y += int(self.speed_y)

        # Check for collisions with platforms
        # This first check happens after the Y-axis position was updated, and as such, it checks for collisions
        # between the top and bottom of the platforms and the player.

        # Check for collisions with the spritecollide function
        collided_platforms = pygame.sprite.spritecollide(self, self.platforms, False)
        # For every platform hit, checks if the player was going up or down, and set the position of the player
        # (top or bottom side) to the top or bottom of the hit platform, as well as reset the vertical speed to 0
        for platform in collided_platforms:
            if self.speed_y > 0:
                self.rect.bottom = platform.rect.top
            elif self.speed_y < 0:
                self.rect.top = platform.rect.bottom

            self.speed_y = 0


# Create the platform class, also based on pygame.sprite.Sprite
class Platform(pygame.sprite.Sprite):

    def __init__(self, width, x, y, color=RED):
        super().__init__()

        # Override the image attribute
        self.image = pygame.Surface((width, 10))
        self.image.fill(color)

        # Override the rect attribute
        self.rect = self.image.get_rect()

        # Set the position to the coordinates given as arguments
        self.rect.centerx = x
        self.rect.centery = y


class Level:

    def __init__(self):
        self.file = None
        self.platforms = []

    def file_to_data(self, file):
        pl_tag = 'platform'
        loaded_file = open(file, 'r').read()
        lines = loaded_file.splitlines()
        while lines:
            line = lines.pop(0)
            parts = line.split()
            if pl_tag == parts[0]:
                parts.pop(0)
                self.platforms.append(Platform(int(parts[2]), int(parts[0]), int(parts[1]), ImageColor.getcolor(parts[3], 'RGB')))


# Create a level function, which will contain all the platform creation
# It takes two sprite groups, which are used for drawing and collisions of the platforms
def level_dp(all_sprites_group, platform_group):
    # Create an empty list called platforms
    platforms = []

    # Create all the platforms -- these values give a playable level, but they are essentially completely arbitrary
    platforms.append(Platform(50, 450, 50))
    platforms.append(Platform(100, 350, 100))
    platforms.append(Platform(80, 200, 150))
    platforms.append(Platform(50, 100, 200))
    platforms.append(Platform(80, 320, 210))
    platforms.append(Platform(60, 190, 250))
    platforms.append(Platform(150, 0, 320))
    platforms.append(Platform(80, 260, 400))
    platforms.append(Platform(60, 420, 460))
    platforms.append(Platform(100, 620, 500))
    platforms.append(Platform(40, 800, 580))
    platforms.append(Platform(60, 600, 610))
    platforms.append(Platform(100, 650, 700))

    # Add all the platforms in the list to both sprite groups
    for platform in platforms:
        all_sprites_group.add(platform)
        platform_group.add(platform)

    return platforms


def gen_level(level: Level, asg, pg):
    for platform in level.platforms:
        asg.add(platform)
        pg.add(platform)


# Create a function that checks for and handles beating the level
def victory(player):
    # Create a font object, to display the victory text.
    font = pygame.font.SysFont('comicsansms', 40)
    # Checks if the player reaches a certain position (jumping onto the last platform)
    if player.rect.bottom <= 50 and player.rect.left <= 500 and player.rect.right >= 450:
        # If the player reaches it, runs an infinite loop
        while True:
            # This victory screen has it's own event loop
            for event in pygame.event.get():
                # Checks if the user wants to quit the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                # Checks if the player presses R, our chosen restart key. If it is pressed, relaunch the game.
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game()

            # Sets the black background
            screen.fill(BLACK)

            # Displays the victory message on screen
            text = font.render('Press R to restart', True, BLUE)
            screen.blit(text, (SCREEN_WIDTH // 2 - (text.get_rect()[2]//2), SCREEN_HEIGHT // 2 - (text.get_rect()[3]//2)))

            # Updates the entire display (since it is a static screen, there is no need for any optimization)
            pygame.display.flip()

            # Limits the FPS for performance/bandwidth reasons
            clock.tick(GAME_SPEED)


# Create the game function
def game():
    lvl = Level()
    lvl.file_to_data('level0.dat')
    # Create an instance of the player class
    player = Player(BLUE)

    # Give the player a starting position that is relative to the player's size and position in order to allow resizing
    player.rect.x = (SCREEN_WIDTH // 2) - 20
    player.rect.y = SCREEN_HEIGHT - player.rect.height

    # Add the player to the sprite group. This allows us to call the draw() method.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Create a group for the platforms and call the level function
    platform_group = pygame.sprite.Group()
    gen_level(lvl, all_sprites, platform_group)
    # Assigns the player's platform variable to be equal to the platform sprite group (for use in collisions)
    player.platforms = platform_group

    # Update all the sprites and draw the entire screen once, since during gameplay, it will only update the part
    # where the player is
    screen.fill(BLACK)
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()

    # An infinite while loop for when the game is running
    while True:
        # Fill the screen with a background color
        screen.fill(BLACK)

        # Call the player's event loop (using the function makes the game loop clearer and cleaner)
        player.handle_keys()

        # Call the victory function, to check if the player has reached the last platform
        victory(player)

        # Call the sprite group's update method (in this instance, the player's update method), then draw the player
        all_sprites.update()
        all_sprites.draw(screen)

        # Refresh the display
        # Updating only the section of the display where the player was, and where the player is provides a
        # very significant performance boost on repl.it (not visible if running python on the desktop).
        # On the desktop, it does cause the player rectangle to have some deformations (not the case on repl.it)
        pygame.display.update()

        # Limit the framerate to limit the player's visual movement speed
        clock.tick(GAME_SPEED)


# Runs the code if the file run is this one (python convention)
if __name__ == '__main__':
    # Initialize pygame
    pygame.init()
    # Run the game
    game()
