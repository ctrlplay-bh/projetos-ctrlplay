import random
import pygame
from pygame import gfxdraw
from pygame.sprite import Sprite

import configuration as cg


class Ball(Sprite):

    ball_grid_options = [(x, y) for x in range(cg.BALL_SIZE,
                                               cg.SCREEN_WIDTH-cg.BALL_SIZE,
                                               cg.BALL_SIZE*4)
                         for y in range(cg.BALL_SIZE,
                                        cg.SCREEN_HEIGTH-cg.BALL_SIZE,
                                        cg.BALL_SIZE*4)]

    def __init__(self):
        Sprite.__init__(self)

        self.infected = False
        # Posição inicial da bolinha
        self.ball_color = cg.BALL_COLOR
        self._position = self.posiciona_bolinha()
        self._x_start = self._position[0]-cg.BALL_SIZE
        self._x_end = self._position[0]+cg.BALL_SIZE

        self._draw_position_x = self._position[0]
        self._draw_position_y = self._position[1]
        # Velocidade de deslocamento da bolinha
        self._speed = pygame.math.Vector2((random.uniform(-1, 1),
                                          random.uniform(-1, 1)))
        self._speed.normalize_ip()

        # Bolinha se movimenta ou não
        self._move = False

    def move(self):

        self._position[0] += self._speed[0]*cg.VELOCIDADE
        self._position[1] += self._speed[1]*cg.VELOCIDADE

        self._x_start = self._position[0] - cg.BALL_SIZE
        self._x_end = self._position[0] + cg.BALL_SIZE

        self._draw_position_x = int(self._position[0])
        self._draw_position_y = int(self._position[1])

        if (self._position[0] >= cg.SCREEN_WIDTH - cg.BALL_SIZE):
            self._speed[0] *= -1
            self._position[0] -= 1

        if (self._position[0] <= cg.BALL_SIZE):
            self._speed[0] *= -1
            self._position[0] += 1

        if (self._position[1] > cg.SCREEN_HEIGTH - cg.BALL_SIZE):
            self._speed[1] *= -1
            self._position[1] -= 1

        if self._position[1] <= cg.BALL_SIZE:
            self._speed[1] *= -1
            self._position[1] += 1

    def draw(self):

        if self.infected:
            self.ball_color = (255, 50, 50)

        gfxdraw.aacircle(cg.screen,
                         self._draw_position_x,
                         self._draw_position_y,
                         cg.BALL_SIZE,
                         self.ball_color)
        gfxdraw.filled_circle(cg.screen,
                              self._draw_position_x,
                              self._draw_position_y,
                              cg.BALL_SIZE,
                              self.ball_color)

    def update(self):
        self.move()
        self.draw()

    def collision(self, ball):
        # Para detectar uma colisão entre círculos devemos traçar uma reta
        # do centro do primeiro círculo para o centro do segundo círculo.
        # Se essa reta for menor que 2*raio os círculos estarão em colisão

        # Velocidade relativa
        velocidade_relativa = ball._speed - self._speed
        distancia_relativa = ball._position - self._position

        if (self._position.distance_to(ball._position) <= 2*cg.BALL_SIZE
           and velocidade_relativa.dot(distancia_relativa) < 0):
            self.calcula_nova_rota(ball)
            if(self.infected or ball.infected):
                self.infected, ball.infected = (True, True)

        elif self._position.distance_to(ball._position) <= 2*cg.BALL_SIZE:
            self._speed *= -1
            if(self.infected or ball.infected):
                self.infected, ball.infected = (True, True)

    def calcula_nova_rota(self, ball):
        # Calcula nova rota das bolas que colidiram

        normal_vector = pygame.math.Vector2(self._position[0] -
                                            ball._position[0],
                                            self._position[1] -
                                            ball._position[1])

        unit_normal_vector = normal_vector.normalize()
        unit_tangent_vector = pygame.math.Vector2(-unit_normal_vector[1],
                                                  unit_normal_vector[0])
        v1n = unit_normal_vector.dot(self._speed)
        v1t = unit_tangent_vector.dot(self._speed)
        v2n = unit_normal_vector.dot(ball._speed)
        v2t = unit_tangent_vector.dot(ball._speed)

        v1n_depois = unit_normal_vector*v2n
        v2n_depois = unit_normal_vector*v1n
        v1t_depois = unit_tangent_vector*v1t
        v2t_depois = unit_tangent_vector*v2t

        self._speed = (v1n_depois + v1t_depois).normalize()
        ball._speed = (v2n_depois + v2t_depois).normalize()
        # self.move()
        # ball.move()

    def posiciona_bolinha(self):

        posicao_bolinha = random.choice(Ball.ball_grid_options)
        Ball.ball_grid_options.remove(posicao_bolinha)
        return pygame.math.Vector2(posicao_bolinha[0], posicao_bolinha[1])