import pygame

pygame.init()

screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()
FPS = 120

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(FPS)
