import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Load splash image
splash_image = pygame.image.load('/mnt/data/pong.webp')

# Original dimensions of the splash image
original_width, original_height = splash_image.get_rect().size

# Desired height
height = 600

# Calculate new width to maintain aspect ratio
aspect_ratio = original_width / original_height
width = int(height * aspect_ratio)

# Scale splash image to new dimensions
splash_image = pygame.transform.scale(splash_image, (width, height))

# Set up display with new dimensions
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong Game')

# Display the splash image
screen.blit(splash_image, (0, 0))
pygame.display.flip()

# Wait for a few seconds
pygame.time.wait(3000)

# Fonts
font_name = pygame.font.match_font('arial')  # Replace 'arial' with the font name used in the image if available

# Function to draw text on the screen
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Capture player names
def capture_player_names():
    input_box = pygame.Rect(width // 4, height // 2 - 30, width // 2, 30)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(BLACK)
        txt_surface = pygame.font.Font(font_name, 32).render(text, True, color)
        width_txt = max(200, txt_surface.get_width()+10)
        input_box.w = width_txt
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        pygame.time.Clock().tick(30)
    return text

player1_name = capture_player_names()
player2_name = capture_player_names()

# Game constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_SIZE = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

# Score
max_score = 10
player1_score = 0
player2_score = 0

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

    # Score update
    if ball_pos[0] <= 0:
        player2_score += 1
        ball_pos = [width // 2, height // 2]
    elif ball_pos[0] >= width:
        player1_score += 1
        ball_pos = [width // 2, height // 2]

    # Clear screen
    screen.fill(BLACK)

    # Draw paddles
    pygame.draw.rect(screen, WHITE, (0, paddle1_pos, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (width - PADDLE_WIDTH, paddle2_pos, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw ball
    pygame.draw.circle(screen, WHITE, ball_pos, BALL_SIZE // 2)

    # Draw player names
    draw_text(screen, player1_name, 20, width // 4, 10)
    draw_text(screen, player2_name, 20, 3 * width // 4, 10)

    # Draw score bars
    player1_score_height = (player1_score / max_score) * height
    player2_score_height = (player2_score / max_score) * height
    pygame.draw.rect(screen, WHITE, (width // 4 - 10, height - player1_score_height, 20, player1_score_height))
    pygame.draw.rect(screen, WHITE, (3 * width // 4 - 10, height - player2_score_height, 20, player2_score_height))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
