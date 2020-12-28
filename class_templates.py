import pygame

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 800


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        width = None
        height = None

        self.image = None
        self.rect = None

        self.speed_x = None
        self.speed_y = None

        self.direction = 0

        self.platforms = None

    def handle_keys(self):
        pass

    def gravity(self):
        pass

    def jump(self):
        pass

    def update_mvm(self, accel_mult, friction) -> None:
        """Please note that the variables for screen height and width must be named the exact same way as in the instructions"""
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
        pass


class Platform(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()


class Game:

    def __init__(self):
        pass

    def run(self):
        pass


if __name__ == "__main__":
    pass
