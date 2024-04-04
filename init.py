import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
window_width, window_height = 800, 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Zen Garden Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Game variables
concentration_low = False
concentration_medium = False
concentration_high = False
plant_size = 0

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Placeholder for concentration level inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                concentration_low = True
            elif event.key == pygame.K_2:
                concentration_medium = True
            elif event.key == pygame.K_3:
                concentration_high = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                concentration_low = False
            elif event.key == pygame.K_2:
                concentration_medium = False
            elif event.key == pygame.K_3:
                concentration_high = False

    # Update game state
    screen.fill(WHITE)

    # Game logic for plant growth based on concentration levels
    if concentration_low and plant_size < 20:
        plant_size += 1
    elif concentration_medium and 20 <= plant_size < 50:
        plant_size += 1
    elif concentration_high and 50 <= plant_size < 100:
        plant_size += 1

    # Draw the plant
    if plant_size > 0:
        pygame.draw.circle(screen, GREEN, (window_width // 2, window_height // 2), plant_size)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
