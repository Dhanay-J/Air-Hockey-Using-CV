from settings import *

class GoalPost:
    def __init__(self, x, screen, color=BLUE):
        self.x = x
        self.y = HEIGHT // 2
        self.width = GOAL_WIDTH
        self.height = GOAL_HEIGHT
        self.color = color
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y - self.height // 2, self.width, self.height))
