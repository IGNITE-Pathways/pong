import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Paddle dimensions
paddle_width = 20
paddle_height = 150

# Ball dimensions
ball_width = 20
ball_height = 20

# Speeds
paddle_speed = 6
initial_ball_speed_x = 4
initial_ball_speed_y = 4

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Paddle positions
player_paddle = pygame.Rect(screen_width - paddle_width - 20, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)
computer_paddle = pygame.Rect(20, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)

# Ball position
ball = pygame.Rect(screen_width // 2 - ball_width // 2, screen_height // 2 - ball_height // 2, ball_width, ball_height)

# Game variables
player_score = 0
computer_score = 0
max_score = 5
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
ball_speed_x = initial_ball_speed_x
ball_speed_y = initial_ball_speed_y
start_time = time.time()
best_time = 0

# Function to draw the net
def draw_net():
    for i in range(0, screen_height, 20):
        pygame.draw.line(screen, white, (screen_width // 2, i), (screen_width // 2, i + 10))

# Function to display text
def display_text(text):
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)

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
    if ball.left <= 0:
        player_score += 1
        ball.x, ball.y = screen_width // 2 - ball_width // 2, screen_height // 2 - ball_height // 2
        ball_speed_x = initial_ball_speed_x * random.choice((-1, 1))
        ball_speed_y = initial_ball_speed_y * random.choice((-1, 1))
        elapsed_time = int(time.time() - start_time)
        if elapsed_time > best_time:
            best_time = elapsed_time
        start_time = time.time()
    if ball.right >= screen_width:
        computer_score += 1
        ball.x, ball.y = screen_width // 2 - ball_width // 2, screen_height // 2 - ball_height // 2
        ball_speed_x = initial_ball_speed_x * random.choice((-1, 1))
        ball_speed_y = initial_ball_speed_y * random.choice((-1, 1))
        elapsed_time = int(time.time() - start_time)
        if elapsed_time > best_time:
            best_time = elapsed_time
        start_time = time.time()

    # Check for winner
    if player_score == max_score:
        display_text("You Win!")
        player_score = 0
        computer_score = 0
        ball_speed_x = initial_ball_speed_x
        ball_speed_y = initial_ball_speed_y
        start_time = time.time()
    elif computer_score == max_score:
        display_text("Computer Wins!")
        player_score = 0
        computer_score = 0
        ball_speed_x = initial_ball_speed_x
        ball_speed_y = initial_ball_speed_y
        start_time = time.time()

    # Clear the screen
    screen.fill(black)

    # Draw net
    draw_net()

    # Draw paddles and ball
    pygame.draw.rect(screen, white, player_paddle)
    pygame.draw.rect(screen, white, computer_paddle)
    pygame.draw.ellipse(screen, white, ball)

    # Display scores
    player_text = font.render(str(player_score), True, white)
    screen.blit(player_text, (screen_width // 2 + 20, 10))
    computer_text = font.render(str(computer_score), True, white)
    screen.blit(computer_text, (screen_width // 2 - 40, 10))

    # Display running clock
    elapsed_time = int(time.time() - start_time)
    time_text = small_font.render(f"Time: {elapsed_time}s", True, white)
    screen.blit(time_text, (screen_width // 2 - 50, screen_height - 80))

    # Display best time
    best_time_text = small_font.render(f"Best Time: {best_time}s", True, white)
    screen.blit(best_time_text, (screen_width // 2 - 70, screen_height - 40))

    # Update the display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)

pygame.quit()
