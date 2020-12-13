import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

    def handle_keys(self):
        pass

    def gravity(self):
        pass

    def jump(self):
        pass

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
