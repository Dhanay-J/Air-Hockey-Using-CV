import os
from ultralytics import YOLO
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2
import numpy as np
import pygame
import math
from collections import deque
from settings import *
from ball import Ball
from goal_post import GoalPost
from paddle import Paddle

# Initialize Pygame
pygame.init()

# Font
FONT = pygame.font.Font(None, 36)
LARGE_FONT = pygame.font.Font(None, 72)

SCALE_FACTOR_X = 50 * WIDTH / HEIGHT
SCALE_FACTOR_Y = 50 * HEIGHT / WIDTH

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Round Paddle Pong")

class Game:
    def __init__(self, model_path="./circle_detector.pt"):
        self.blue_player = Paddle(50, HEIGHT // 2, screen)
        self.red_player = Paddle(WIDTH - 50, HEIGHT // 2, screen, RED)
        self.ball = Ball(screen)
        self.blue_player_goal = GoalPost(0, screen)
        self.red_player_goal = GoalPost(WIDTH - GOAL_WIDTH, screen, RED)
        self.blue_player_score = 0
        self.red_player_score = 0
        self.prev_blue_pos = None
        self.prev_red_pos = None
        self.prev_blue_dx = 0
        self.prev_blue_dy = 0
        self.prev_red_dx = 0
        self.prev_red_dy = 0
        self.state = COUNTDOWN
        self.countdown = 3
        self.countdown_timer = 0
        self.play_timer = 0
        self.game_duration = 30 * 1000  # 30 seconds in milliseconds
        self.splash_timer = 0
        self.splash_duration = 3 * 1000  # 3 seconds in milliseconds
        self.last_scorer = None
        self.frame_skip = 5  # Skip frames for YOLO detection to improve performance
        self.current_frame = 0
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Lower resolution for faster detection
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.model = YOLO(model_path)

    def detect_color_circle(self, frame, color):
        """Detect color circle using YOLO"""
        results = self.model.predict(source=frame, conf=0.8, verbose=False)[0]
        color_code = 1.0 if color == 'blue' else 0.0
        color_rgb = (255, 0, 0) if color == 'blue' else (0, 0, 255)
        
        for box in results.boxes.data:
            if box[-1] == color_code:
                x_min, y_min, x_max, y_max = map(int, box[:4])
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color_rgb, 2)
                return (x_min + x_max) / 2, (y_min + y_max) / 2
        
        return None

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.state == COUNTDOWN:
            if current_time - self.countdown_timer > 1000:
                self.countdown -= 1
                self.countdown_timer = current_time
                if self.countdown == 0:
                    self.state = PLAYING
                    self.play_timer = current_time

        elif self.state == PLAYING:
            # Skipping frames for YOLO detection
            self.current_frame += 1
            if self.current_frame % self.frame_skip == 0:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Failed to capture frame.")
                    return
                frame = cv2.flip(frame, 1)

                # Detect blue circle
                blue_pos = self.detect_color_circle(frame, 'blue')
                if blue_pos:
                    self.process_paddle_movement(blue_pos, self.blue_player, 'blue')

                # Detect red circle
                red_pos = self.detect_color_circle(frame, 'red')
                if red_pos:
                    self.process_paddle_movement(red_pos, self.red_player, 'red')

                # Display the frame
                cv2.imshow('Paddle Game', frame)
                cv2.waitKey(1)

            self.ball.move()
            self.check_ball_collision()

            # Check goal condition
            self.check_goal()

            # Check if time's up
            if current_time - self.play_timer > self.game_duration:
                self.state = GAME_OVER

        elif self.state == SCORE_SPLASH:
            if current_time - self.splash_timer > self.splash_duration:
                self.state = PLAYING
                self.ball.reset()

    def process_paddle_movement(self, pos, player, color):
        """Process paddle movement based on detected position"""
        if color == 'blue':
            prev_pos = self.prev_blue_pos
            prev_dx = self.prev_blue_dx
            prev_dy = self.prev_blue_dy
        else:
            prev_pos = self.prev_red_pos
            prev_dx = self.prev_red_dx
            prev_dy = self.prev_red_dy

        if prev_pos:
            dx = (pos[0] - prev_pos[0]) / WIDTH
            dy = (pos[1] - prev_pos[1]) / HEIGHT
            dx *= SCALE_FACTOR_X
            dy *= SCALE_FACTOR_Y

            if abs(dx) > 0.01 or abs(dy) > 0.01:
                smoothing_factor = 0.5
                smooth_dx = dx * smoothing_factor + prev_dx * (1 - smoothing_factor)
                smooth_dy = dy * smoothing_factor + prev_dy * (1 - smoothing_factor)

                scaling_factor = 2.0
                player.move(smooth_dx * scaling_factor, smooth_dy * scaling_factor)

                if color == 'blue':
                    self.prev_blue_dx, self.prev_blue_dy = smooth_dx, smooth_dy
                else:
                    self.prev_red_dx, self.prev_red_dy = smooth_dx, smooth_dy

        if color == 'blue':
            self.prev_blue_pos = pos
        else:
            self.prev_red_pos = pos

    def check_ball_collision(self):
        for paddle in [self.blue_player, self.red_player]:
            dx = self.ball.x - paddle.x
            dy = self.ball.y - paddle.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance <= BALL_RADIUS + PADDLE_RADIUS:
                angle = math.atan2(dy, dx)
                self.ball.dx = BALL_SPEED * math.cos(angle)
                self.ball.dy = BALL_SPEED * math.sin(angle)

    def check_goal(self):
        if self.ball.x <= GOAL_WIDTH:
            if abs(self.ball.y - HEIGHT // 2) <= GOAL_HEIGHT // 2:
                self.red_player_score += 1
                self.last_scorer = "Red"
                self.state = SCORE_SPLASH
                self.splash_timer = pygame.time.get_ticks()
            else:
                self.ball.dx = abs(self.ball.dx)

        if self.ball.x >= WIDTH - GOAL_WIDTH:
            if abs(self.ball.y - HEIGHT // 2) <= GOAL_HEIGHT // 2:
                self.blue_player_score += 1
                self.last_scorer = "Blue"
                self.state = SCORE_SPLASH
                self.splash_timer = pygame.time.get_ticks()
            else:
                self.ball.dx = -abs(self.ball.dx)

    def draw(self):
        screen.fill(BLACK)

        if self.state == COUNTDOWN:
            countdown_text = LARGE_FONT.render(str(self.countdown), True, WHITE)
            screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))

        elif self.state == PLAYING or self.state == SCORE_SPLASH:
            self.blue_player.draw()
            self.red_player.draw()
            self.ball.draw()
            self.blue_player_goal.draw()
            self.red_player_goal.draw()

            score_text = FONT.render(f"{self.blue_player_score} - {self.red_player_score}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

            time_left = max(0, (self.game_duration - (pygame.time.get_ticks() - self.play_timer)) // 1000)
            timer_text = FONT.render(f"Time: {time_left}", True, WHITE)
            screen.blit(timer_text, (WIDTH - timer_text.get_width() - 10, 10))

            if self.state == SCORE_SPLASH:
                splash_text = LARGE_FONT.render(f"{self.last_scorer} Scores!", True, WHITE)
                screen.blit(splash_text, (WIDTH // 2 - splash_text.get_width() // 2, HEIGHT // 2 - splash_text.get_height() // 2))

        elif self.state == GAME_OVER:
            game_over_text = LARGE_FONT.render("Game Over", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    Game().run()
