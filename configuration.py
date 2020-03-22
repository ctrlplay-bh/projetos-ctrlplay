import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 700
SCREEN_HEIGTH = 500
BALL_SIZE = 4
VELOCIDADE = 0.2
BALL_COLOR = (180, 30, 220)

FPS = 120

relogio = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
