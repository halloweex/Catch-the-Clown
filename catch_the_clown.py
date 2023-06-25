import pygame
import random

# Initialize Pygame
pygame.init()

# Set display surface
WINDOW_WIDTH, WINDOW_HEIGTH = 945, 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGTH))
pygame.display.set_caption("Catch the clown!")

# Set colors
BLUE = (1, 175, 209)
YELLOW = (248, 231, 28)
CRYSTAL = (246,190,0,255)

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game values
PLAYER_STARTING_LIVES = 5
CLOWN_STARTING_VELOCITY = 3
CLOWN_ACCELERATION = .5

score = 0
player_lives = PLAYER_STARTING_LIVES

clown_velocity = CLOWN_STARTING_VELOCITY
clown_dx = random.choice([-1, 1])
clown_dy = random.choice([-1, 1])

# Set fonts
font = pygame.font.Font('Franxurter.ttf', 32)
font2 = pygame.font.Font('Franxurter.ttf', 64)


# Define text
title_text = font.render("catch the clown!", True, BLUE)
title_rect = title_text.get_rect()
title_rect.topleft = (10, 10)

lives_text = font.render("LIVES: " + str(player_lives), True, YELLOW)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10, 10)

score_text = font.render("SCORE: " + str(score), True, YELLOW)
score_rect = score_text.get_rect()
score_rect.topright = (WINDOW_WIDTH - 10, 50)

game_over_text = font2.render('GAMEOVER', True, BLUE, YELLOW)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGTH // 2)

continue_text = font2.render("Click anywhere to play again", True, YELLOW, BLUE)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGTH // 2 + 60)

# Set sounds and music
click_sound = pygame.mixer.Sound('sounds/click_sound.wav')
miss_sound = pygame.mixer.Sound('sounds/miss_sound.wav')
miss_sound.set_volume(.1)
pygame.mixer.music.load('sounds/ctc_background_music.wav')

# Set images
clown_image = pygame.image.load("img/clown.png")
clown_rect = clown_image.get_rect()
clown_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGTH // 2)

back_img = pygame.image.load("img/background.png")
back_rect = back_img.get_rect()
back_rect.topleft = (0, 0)

# The main game loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    # Check to see if user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]

            # The clown was clicked
            if clown_rect.collidepoint(mouse_x, mouse_y):
                click_sound.play()
                score += 1
                clown_velocity += CLOWN_ACCELERATION

                # Move the clown in a new direction
                previous_dx = clown_dx
                previous_dy = clown_dy
                while(previous_dx == clown_dx and previous_dy == clown_dy):
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])
            # We missed the clown
            else:
                miss_sound.play()
                player_lives -= 1

    # Move the clown
    clown_rect.x += clown_dx*clown_velocity
    clown_rect.y += clown_dy*clown_velocity

    # Bounce the clown off the edges of the display
    if clown_rect.left <= 0 or clown_rect.right >= WINDOW_WIDTH:
        clown_dx = -1*clown_dx
    if clown_rect.top <= 0 or clown_rect.bottom >= WINDOW_HEIGTH:
        clown_dy = -1*clown_dy

    # Update HUD
    score_text = font.render("Score: " + str(score), True, YELLOW)
    lives_text = font.render("Lives: " + str(player_lives), True, YELLOW)

    # Gameover check
    if player_lives < 0:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        # Pause the game until the player clicks then reset the game
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                # The player wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                # The player wants to play again
                if event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    pygame.mixer.music.play(-1, 0.0)
                    player_lives = PLAYER_STARTING_LIVES

                    clown_velocity = CLOWN_STARTING_VELOCITY
                    clown_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGTH // 2)
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])
                    is_paused = False

    # Blit the backgrounds
    display_surface.blit(back_img, back_rect)

    # Blit HUD
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(lives_text, lives_rect)

    # Blit assets
    display_surface.blit(clown_image, clown_rect)

    # Update display and tick clock
    pygame.display.update()
    clock.tick(FPS)

# End the game
pygame.quit()
