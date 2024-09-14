from settings import *

class Paddle:
    def __init__(self, x, y, screen,color=BLUE):
        self.x = x
        self.y = y
        self.radius = PADDLE_RADIUS
        self.speed = PADDLE_SPEED
        self.color = color
        self.screen = screen

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.x = max(self.radius, min(self.x, WIDTH - self.radius))
        self.y = max(self.radius, min(self.y, HEIGHT - self.radius))

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)
