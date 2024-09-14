import pygame
import random
import math
from settings import *

class Ball:
    def __init__(self,screen):
        self.reset()
        self.screen = screen

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        angle = random.uniform(-math.pi/4, math.pi/4)
        self.dx = BALL_SPEED * math.cos(angle)
        self.dy = BALL_SPEED * math.sin(angle)
        if random.choice([True, False]):
            self.dx = -self.dx

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.y <= BALL_RADIUS:
            self.y = BALL_RADIUS
            self.dy = abs(self.dy)
        elif self.y >= HEIGHT - BALL_RADIUS:
            self.y = HEIGHT - BALL_RADIUS
            self.dy = -abs(self.dy)

        min_dx = 2
        if abs(self.dx) < min_dx:
            self.dx = min_dx if self.dx > 0 else -min_dx

    def draw(self):
        pygame.draw.circle(self.screen, YELLOW, (int(self.x), int(self.y)), BALL_RADIUS)
