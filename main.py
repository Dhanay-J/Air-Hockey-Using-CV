import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Round Paddle Pong")

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

# Font
FONT = pygame.font.Font(None, 36)
LARGE_FONT = pygame.font.Font(None, 72)

# Game states
COUNTDOWN = 0
PLAYING = 1
SCORE_SPLASH = 2
GAME_OVER = 3

class Paddle:
    def __init__(self, x, y, color=BLUE):
        self.x = x
        self.y = y
        self.radius = PADDLE_RADIUS
        self.speed = PADDLE_SPEED
        self.color = color

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.x = max(self.radius, min(self.x, WIDTH - self.radius))
        self.y = max(self.radius, min(self.y, HEIGHT - self.radius))

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Ball:
    def __init__(self):
        self.reset()

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
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), BALL_RADIUS)

class GoalPost:
    def __init__(self, x, color=BLUE):
        self.x = x
        self.y = HEIGHT // 2
        self.width = GOAL_WIDTH
        self.height = GOAL_HEIGHT
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y - self.height // 2, self.width, self.height))

class Game:
    def __init__(self):
        self.blue_player = Paddle(50, HEIGHT // 2)
        self.red_player = Paddle(WIDTH - 50, HEIGHT // 2, RED)
        self.ball = Ball()
        self.blue_player_goal = GoalPost(0)
        self.red_player_goal = GoalPost(WIDTH - GOAL_WIDTH, RED)
        self.blue_player_score = 0
        self.red_player_score = 0
        self.state = COUNTDOWN
        self.countdown = 3
        self.countdown_timer = 0
        self.play_timer = 0
        self.game_duration = 30 * 1000  # 30 seconds in milliseconds
        self.splash_timer = 0
        self.splash_duration = 3 * 1000  # 3 seconds in milliseconds
        self.last_scorer = None

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
            keys = pygame.key.get_pressed()
            self.blue_player.move(keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w])
            self.red_player.move(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], keys[pygame.K_DOWN] - keys[pygame.K_UP])

            self.ball.move()

            for paddle in [self.blue_player, self.red_player]:
                dx = self.ball.x - paddle.x
                dy = self.ball.y - paddle.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance <= BALL_RADIUS + PADDLE_RADIUS:
                    angle = math.atan2(dy, dx)
                    self.ball.dx = BALL_SPEED * math.cos(angle)
                    self.ball.dy = BALL_SPEED * math.sin(angle)

            if self.ball.x <= GOAL_WIDTH:
                if abs(self.ball.y - HEIGHT // 2) <= GOAL_HEIGHT // 2:
                    self.red_player_score += 1
                    self.last_scorer = "Red"
                    self.state = SCORE_SPLASH
                    self.splash_timer = current_time
                else:
                    self.ball.dx = abs(self.ball.dx)

            if self.ball.x >= WIDTH - GOAL_WIDTH:
                if abs(self.ball.y - HEIGHT // 2) <= GOAL_HEIGHT // 2:
                    self.blue_player_score += 1
                    self.last_scorer = "Blue"
                    self.state = SCORE_SPLASH
                    self.splash_timer = current_time
                else:
                    self.ball.dx = -abs(self.ball.dx)

            if current_time - self.play_timer > self.game_duration:
                self.state = GAME_OVER

        elif self.state == SCORE_SPLASH:
            if current_time - self.splash_timer > self.splash_duration:
                self.state = PLAYING
                self.ball.reset()

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
            if self.blue_player_score > self.red_player_score:
                result_text = "Blue Player Wins!"
            elif self.red_player_score > self.blue_player_score:
                result_text = "Red Player Wins!"
            else:
                result_text = "It's a Draw!"

            result_surface = LARGE_FONT.render(result_text, True, WHITE)
            screen.blit(result_surface, (WIDTH // 2 - result_surface.get_width() // 2, HEIGHT // 2 - result_surface.get_height() // 2))

            restart_text = FONT.render("Click to Restart", True, GREEN)
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == GAME_OVER:
                self.__init__()  # Reset the game
        return True

def main():
    clock = pygame.time.Clock()
    game = Game()

    running = True
    while running:
        running = game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()