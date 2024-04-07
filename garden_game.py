import pygame
import sys
import numpy as np

def game_start():
    # Initialize Pygame
    pygame.init()


    font = pygame.font.Font('freesansbold.ttf', 30)


    # Set up the display
    window_width, window_height = 800, 600
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Zen Garden Game")

    # Colors
    RED = (255, 0,0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 128)
    GREEN = (0, 255, 0)
    BLACK = (255, 255, 255)

    # Game variables
    concentration_low = False
    concentration_medium = False
    concentration_high = False
    plant_size = 5

    # concentration_level = TODO: output of the signal process




    # Main game loop
    running = True
    while running:
        #print(" PLANT SIZE: ", plant_size)
        # Handle events
        concentration_level = np.load("status.npy")
        #print(concentration_level)
        # vvvv TODO: USE BELOW TO CONNECT GAME WITH BRAIN SIGNALS\
        if plant_size <= 300:
            # Update game state
            #screen.fill(WHITE)
            if concentration_level == "low": # concentration low
                plant_size = plant_size * 1
                print("low", plant_size)
            elif concentration_level == "medium": # concentration med
                plant_size = plant_size * 1.2
                print("med", plant_size)
            elif concentration_level == "high": # concentration high
                plant_size = plant_size * 1.5
                print("high", plant_size)

            '''
            # vvvv TODO: BELOW IS FOR TESTING GAME WITH KEYBOARD
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: # concentration low
                    if plant_size >= 1:
                        plant_size = plant_size * 0.5
                    print("low", plant_size)
                elif event.key == pygame.K_2: # concentration med
                    plant_size = plant_size * 1.2
                    print("med", plant_size)
                elif event.key == pygame.K_3: # concentration high
                    plant_size = plant_size * 1.5
                    print("high", plant_size)
            '''

            # Draw the plant
            if plant_size > 0:
                pygame.draw.circle(screen, GREEN, (window_width // 2, window_height // 2), plant_size)

        else:
            pygame.draw.circle(screen, WHITE, (window_width // 2, window_height // 2), plant_size)
            final_score_text = font.render("WIN", True, RED, BLUE)
            final_score_textRect = final_score_text.get_rect()
            final_score_textRect.x = screen.get_width() / 2
            final_score_textRect.y = screen.get_width() / 2
            screen.blit(final_score_text, final_score_textRect)
        pygame.time.delay(1000)
        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()
