import pygame
import sys

# Initialize Pygame
pygame.init()

# Load splash image
splash_image = pygame.image.load('/mnt/data/pong.webp')

# Get dimensions of the splash image
splash_rect = splash_image.get_rect()
width, height = splash_rect.size

# Set up display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong Game')

# Display the splash image
screen.blit(splash_image, (0, 0))
pygame.display.flip()

# Wait for a few seconds
pygame.time.wait(3000)

# Game constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_SIZE = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

# Game variables
ball_pos = [width // 2, height // 2]
ball_vel = [2, 2]
paddle1_pos = height // 2 - PADDLE_HEIGHT // 2
paddle2_pos = height // 2 - PADDLE_HEIGHT // 2
paddle1_vel = 0
paddle2_vel = 0
paddle_speed = 6

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                paddle1_vel = -paddle_speed
            elif event.key == pygame.K_s:
                paddle1_vel = paddle_speed
            elif event.key == pygame.K_UP:
                paddle2_vel = -paddle_speed
            elif event.key == pygame.K_DOWN:
                paddle2_vel = paddle_speed
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                paddle1_vel = 0
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                paddle2_vel = 0

    # Update paddle positions
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel

    # Ensure paddles stay on screen
    paddle1_pos = max(0, min(height - PADDLE_HEIGHT, paddle1_pos))
    paddle2_pos = max(0, min(height - PADDLE_HEIGHT, paddle2_pos))

    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Ball collision with top and bottom
    if ball_pos[1] <= BALL_SIZE // 2 or ball_pos[1] >= height - BALL_SIZE // 2:
        ball_vel[1] = -ball_vel[1]

    # Ball collision with paddles
    if (ball_pos[0] <= PADDLE_WIDTH + BALL_SIZE // 2 and
        paddle1_pos < ball_pos[1] < paddle1_pos + PADDLE_HEIGHT) or (
        ball_pos[0] >= width - PADDLE_WIDTH - BALL_SIZE // 2 and
        paddle2_pos < ball_pos[1] < paddle2_pos + PADDLE_HEIGHT):
        ball_vel[0] = -ball_vel[0]

    # Clear screen
    screen.fill(BLACK)

    # Draw paddles
    pygame.draw.rect(screen, WHITE, (0, paddle1_pos, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (width - PADDLE_WIDTH, paddle2_pos, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw ball
    pygame.draw.circle(screen, WHITE, ball_pos, BALL_SIZE // 2)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
