
import numpy as np
import pygame


WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Paddle properties
PADDLE_RADIUS = 30
PADDLE_SPEED = 12

# Ball properties
BALL_RADIUS = 10
BALL_SPEED = 15

# Goal post properties
GOAL_WIDTH = 10
GOAL_HEIGHT = 100

# Game states
COUNTDOWN = 0
PLAYING = 1
SCORE_SPLASH = 2
GAME_OVER = 3

# Color detection constants
BLUE_LOWER_BOUND = np.array([100, 150, 50])
BLUE_UPPER_BOUND = np.array([140, 255, 255])
RED_LOWER_BOUND_1 = np.array([0, 120, 70])
RED_UPPER_BOUND_1 = np.array([10, 255, 255])
RED_LOWER_BOUND_2 = np.array([170, 120, 70])
RED_UPPER_BOUND_2 = np.array([180, 255, 255])
