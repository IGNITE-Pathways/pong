import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Paddle dimensions
paddle_width = 10
paddle_height = 100

# Ball dimensions
ball_width = 10
ball_height = 10

# Speeds
paddle_speed = 6
ball_speed_x = 4
ball_speed_y = 4

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Paddle positions
player_paddle = pygame.Rect(screen_width - paddle_width - 20, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)
computer_paddle = pygame.Rect(20, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)

# Ball position
ball = pygame.Rect(screen_width // 2 - ball_width // 2, screen_height // 2 - ball_height // 2, ball_width, ball_height)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle.top > 0:
        player_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and player_paddle.bottom < screen_height:
        player_paddle.y += paddle_speed

    # Computer AI
    if computer_paddle.centery < ball.centery:
        computer_paddle.y += paddle_speed
    elif computer_paddle.centery > ball.centery:
        computer_paddle.y -= paddle_speed

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with walls
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(computer_paddle):
        ball_speed_x *= -1

    # Scoring and resetting ball
    if ball.left <= 0 or ball.right >= screen_width:
        ball.x, ball.y = screen_width // 2 - ball_width // 2, screen_height // 2 - ball_height // 2
        ball_speed_x *= random.choice((-1, 1))
        ball_speed_y *= random.choice((-1, 1))

    # Clear the screen
    screen.fill(black)

    # Draw paddles and ball
    pygame.draw.rect(screen, white, player_paddle)
    pygame.draw.rect(screen, white, computer_paddle)
    pygame.draw.ellipse(screen, white, ball)

    # Update the display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)

pygame.quit()
