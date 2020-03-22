import pygame
import random
import configuration as cg
import ball
import pygame.sprite
from functions import sort_and_sweep

pygame.init()

done = False

bolinhas = [ball.Ball() for i in range(100)]
(random.choice(bolinhas)).infected = True

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    cg.screen.fill(pygame.Color('#dddddd'))
    for bola in bolinhas:
        bola.update()
    sort_and_sweep(bolinhas)
    pygame.display.flip()
