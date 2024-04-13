import pygame
import random

pygame.init()

try:
    pygame.mixer.init()
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(-1)  # Play the music indefinitely
except pygame.error as e:
    print(f"An error occurred while loading the music: {e}")
    print("Skipping music loading.")

WINDOW_WIDTH = 512
WINDOW_HEIGHT = 512
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Infinite Doomer v1.0")

background_image = pygame.image.load("background.png").convert()
background_rect = background_image.get_rect()
background_rect2 = background_rect.copy()
background_rect2.y = -background_rect.height

player_image = pygame.image.load("player.png")
player_rect = player_image.get_rect()
player_rect.centerx = WINDOW_WIDTH // 2
player_rect.bottom = WINDOW_HEIGHT - 10

obstacle_images = [pygame.image.load(f'ship ({x}).png').convert_alpha() for x in range(1, 17)]
print(f"Loaded {len(obstacle_images)} obstacle images.")

font = pygame.font.SysFont("comicsansms", 48)

obstacles = []
spawn_counter = 0
clock = pygame.time.Clock()
score = 0
game_over = False
obstacle_spawn_rate = 60  
obstacle_speed = 5  

while not game_over:
    clock.tick(60)  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    if not game_over:

        if pygame.mouse.get_pressed()[0]:  
            player_rect.centerx = pygame.mouse.get_pos()[0]

        score += 1

        if score % 120 == 0:  
            obstacle_spawn_rate -= 2  
            obstacle_speed += 1  

        spawn_counter += 1
        if spawn_counter >= obstacle_spawn_rate:
            spawn_counter = 0
            obstacle_image = random.choice(obstacle_images)
            obstacle_rect = obstacle_image.get_rect()
            obstacle_rect.x = random.randint(0, WINDOW_WIDTH - obstacle_rect.width)
            obstacle_rect.y = -obstacle_rect.height
            obstacles.append((obstacle_image, obstacle_rect))

        if obstacles:
            for obstacle_image, obstacle_rect in obstacles:
                obstacle_rect.y += obstacle_speed

        if obstacles:
            for obstacle_image, obstacle_rect in obstacles:
                if player_rect.colliderect(obstacle_rect):
                    game_over = True

        obstacles = [(image, rect) for image, rect in obstacles if rect.y < WINDOW_HEIGHT]

        background_rect.y += obstacle_speed
        background_rect2.y += obstacle_speed

        if background_rect.y >= WINDOW_HEIGHT:
            background_rect.y = -background_rect.height

        if background_rect2.y >= WINDOW_HEIGHT:
            background_rect2.y = -background_rect2.height

    window.blit(background_image, background_rect)
    window.blit(background_image, background_rect2)

    window.blit(player_image, player_rect)

    if obstacles:
        for obstacle_image, obstacle_rect in obstacles:
            window.blit(obstacle_image, obstacle_rect)

    score_text = font.render(f"Score: {score//60}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))

    pygame.display.flip()

game_over_text = font.render("Game Over", True, (255, 0, 0))
game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
window.blit(game_over_text, game_over_rect)

pygame.display.flip()

pygame.time.delay(2000)

pygame.quit()