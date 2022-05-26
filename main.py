import pygame
import os

WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooters")

WHITE = (255, 255, 255)

FPS = 60
VELOCITY = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("assets", "yellow_spaceship.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("assets", "red_spaceship.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

def draw_window(yellow, red):
    WINDOW.fill(WHITE)
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))
    pygame.display.update()

def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a]: # LEFT
            yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d]: # RIGHT
            yellow.x += VELOCITY
    if keys_pressed[pygame.K_w]: # UP
            yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s]: # DOWN
            yellow.y += VELOCITY

def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT]: # LEFT
            red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT]: # RIGHT
            red.x += VELOCITY
    if keys_pressed[pygame.K_UP]: # UP
            red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN]: # DOWN
            red.y += VELOCITY

def main():
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)

        draw_window(yellow, red)

    pygame.QUIT

if __name__ == "__main__":
    main()
