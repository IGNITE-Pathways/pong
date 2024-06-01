import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Load splash image
splash_image_path = os.path.join(os.path.dirname(__file__), 'pong.webp')
splash_image = pygame.image.load(splash_image_path)

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
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Capture player names
def capture_player_names(prompt, screen, width, height, font_name, color_inactive, color_active, BLACK):
    input_box = pygame.Rect(width // 4, height // 2 - 30, width // 2, 30)
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
        draw_text(screen, prompt, 32, width // 2, height // 2 - 70, WHITE)
        txt_surface = pygame.font.Font(font_name, 32).render(text, True, color)
        width_txt = max(200, txt_surface.get_width()+10)
        input_box.w = width_txt
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        pygame.time.Clock().tick(30)
    return text

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')

# Get player names
player1_name = capture_player_names("Player 1 Name:", screen, width, height, font_name, color_inactive, color_active, BLACK)
player2_name = capture_player_names("Player 2 Name:", screen, width, height, font_name, color_inactive, color_active, BLACK)

# Game constants
BALL_SIZE = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

# Score
max_score = 5
player1_score = 0
player2_score = 0

# Game variables
ball_pos = [width // 2, height // 2]
ball_vel = [3, 3]
paddle1_pos = height // 2 - PADDLE_HEIGHT // 2
paddle2_pos = height // 2 - PADDLE_HEIGHT // 2
paddle1_vel = 0
paddle2_vel = 0
paddle_speed = 6

# Main game loop
running = True
clock = pygame.time.Clock()

def announce_winner(winner_name):
    screen.fill(BLACK)
    draw_text(screen, f"{winner_name} Wins!", 64, width // 2, height // 2 - 32, WHITE)
    pygame.display.flip()
    pygame.time.wait(3000)

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
        ball_vel[0] *= 1.1  # Increase ball speed after each paddle hit
        ball_vel[1] *= 1.1

    # Score update
    if ball_pos[0] <= 0:
        player2_score += 1
        ball_pos = [width // 2, height // 2]
        ball_vel = [3, 3]  # Reset ball speed
    elif ball_pos[0] >= width:
        player1_score += 1
        ball_pos = [width // 2, height // 2]
        ball_vel = [3, 3]  # Reset ball speed

    if player1_score >= max_score:
        announce_winner(player1_name)
        running = False
    elif player2_score >= max_score:
        announce_winner(player2_name)
        running = False

    # Clear screen
    screen.fill(BLACK)

    # Draw paddles
    pygame.draw.rect(screen, WHITE, (0, paddle1_pos, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (width - PADDLE_WIDTH, paddle2_pos, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw ball
    pygame.draw.circle(screen, WHITE, ball_pos, BALL_SIZE // 2)

    # Draw player names
    draw_text(screen, player1_name, 20, width // 4, 10, WHITE)
    draw_text(screen, player2_name, 20, 3 * width // 4, 10, WHITE)

    # Draw score bars and scores
    score_bar_width = width // 4 - 20
    player1_score_width = (player1_score / max_score) * score_bar_width
    player2_score_width = (player2_score / max_score) * score_bar_width

    # Draw the outline of the score bar
    pygame.draw.rect(screen, WHITE, (width // 4 - score_bar_width // 2, 40, score_bar_width, 10), 2)
    pygame.draw.rect(screen, WHITE, (3 * width // 4 - score_bar_width // 2, 40, score_bar_width, 10), 2)

    # Draw the filled score bar
    pygame.draw.rect(screen, WHITE, (width // 4 - score_bar_width // 2, 40, player1_score_width, 10))
    pygame.draw.rect(screen, WHITE, (3 * width // 4 - score_bar_width // 2, 40, player2_score_width, 10))

    # Draw the actual scores
    draw_text(screen, str(player1_score), 20, width // 4, 60, WHITE)
    draw_text(screen, str(player2_score), 20, 3 * width // 4, 60, WHITE)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
