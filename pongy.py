import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

# Speeds
PADDLE_SPEED = 5
INITIAL_BALL_SPEED_X = 4
INITIAL_BALL_SPEED_Y = 4

# Font
FONT = pygame.font.SysFont("comicsans", 50)
GAME_OVER_FONT = pygame.font.SysFont("comicsans", 30)  # Larger font for game over text

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = PADDLE_SPEED

    def draw(self, win):
        pygame.draw.rect(win, WHITE, self.rect)

    def move(self, up=True):
        if up:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def follow_ball(self, ball):
        self.rect.centery = ball.rect.centery

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Ball class
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BALL_RADIUS
        self.x_speed = INITIAL_BALL_SPEED_X * random.choice((1, -1))
        self.y_speed = INITIAL_BALL_SPEED_Y * random.choice((1, -1))
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)

    def draw(self, win):
        pygame.draw.ellipse(win, WHITE, self.rect)

    def move(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.y_speed *= -1

    def reset(self):
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT // 2
        self.x_speed = INITIAL_BALL_SPEED_X * random.choice((1, -1))
        self.y_speed = INITIAL_BALL_SPEED_Y * random.choice((1, -1))

def draw(win, paddles, ball, elapsed_time, game_over, longest_time, show_start_button, show_timer):
    win.fill(BLACK)
    for paddle in paddles:
        paddle.draw(win)

    ball.draw(win)

    if show_timer:
        timer_text = FONT.render(f"Time: {elapsed_time:.1f}", 1, WHITE)
        win.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 20))

    if game_over:
        game_over_text = GAME_OVER_FONT.render(f"Game Over! Longest Time: {longest_time:.1f} seconds", 1, WHITE)
        win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 6 - game_over_text.get_height() // 2))

    if show_start_button:
        start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)
        pygame.draw.rect(win, GREEN, start_button_rect)
        start_text = FONT.render("Start", 1, BLACK)
        win.blit(start_text, (start_button_rect.x + (start_button_rect.width - start_text.get_width()) // 2,
                              start_button_rect.y + (start_button_rect.height - start_text.get_height()) // 2))

    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    if ball.rect.colliderect(left_paddle.rect):
        ball.x_speed *= -1
    elif ball.rect.colliderect(right_paddle.rect):
        ball.x_speed *= -1

def main():
    global left_paddle, right_paddle
    run = True
    game_over = False
    game_started = False
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball(WIDTH // 2, HEIGHT // 2)

    start_time = 0
    last_speed_increase_time = 0
    longest_time = 0

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
                mouse_x, mouse_y = event.pos
                start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    game_started = True
                    start_time = pygame.time.get_ticks()
                    last_speed_increase_time = start_time
                    game_over = False

        if game_started:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        else:
            elapsed_time = 0

        if not game_started:
            draw(WIN, [left_paddle, right_paddle], ball, elapsed_time, game_over, longest_time, show_start_button=True, show_timer=False)
            continue

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.rect.top > 0:
            left_paddle.move(up=True)
        if keys[pygame.K_s] and left_paddle.rect.bottom < HEIGHT:
            left_paddle.move(up=False)

        right_paddle.follow_ball(ball)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.rect.left <= 0 or ball.rect.right >= WIDTH:
            if elapsed_time > longest_time:
                longest_time = elapsed_time
            game_over = True
            game_started = False
            print(f"Longest Time: {longest_time:.1f} seconds")
            ball.reset()
            elapsed_time = 0

        if (pygame.time.get_ticks() - last_speed_increase_time) >= 10000:
            ball.x_speed *= 1.1
            ball.y_speed *= 1.1
            last_speed_increase_time = pygame.time.get_ticks()

        draw(WIN, [left_paddle, right_paddle], ball, elapsed_time, game_over, longest_time, show_start_button=False, show_timer=True)

    pygame.quit()

if __name__ == "__main__":
    main()
