import pygame
import os
pygame.font.init()
pygame.mixer.init()

# WINDOW PROPERTIES
WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
pygame.display.set_caption("Space Shooters")
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)
COLLISION_SOUND = pygame.mixer.Sound(os.path.join("assets", "collision.mp3"))
BLASTER_SOUND = pygame.mixer.Sound(os.path.join("assets", "blaster.mp3"))

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (4, 212, 251)
RED = (251, 85, 87)

# SPACESHIP VARIABLES
FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
BLUE_COLLIDE = pygame.USEREVENT + 1
RED_COLLIDE = pygame.USEREVENT + 2

# LOADING IMAGES
BLUE_SPACESHIP_IMAGE = pygame.image.load(os.path.join("assets", "blue_spaceship.png"))
BLUE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(BLUE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("assets", "red_spaceship.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space.jpg")), (WIDTH, HEIGHT))

# GAME FUNCTIONS
def draw_window(blue, red, blue_bullets, red_bullets, red_health, blue_health):

    WINDOW.blit(SPACE, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    blue_health_text = HEALTH_FONT.render("Health: " + str(blue_health), 1, WHITE)
    WINDOW.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WINDOW.blit(blue_health_text, (10, 10))

    WINDOW.blit(BLUE_SPACESHIP, (blue.x, blue.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in blue_bullets:
        pygame.draw.rect(WINDOW, BLUE, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    pygame.display.update()

def blue_movement(keys_pressed, blue):

    if keys_pressed[pygame.K_a] and blue.x - VELOCITY > 0: # LEFT
        blue.x -= VELOCITY
    if keys_pressed[pygame.K_d] and blue.x + VELOCITY + blue.width < BORDER.x: # RIGHT
        blue.x += VELOCITY
    if keys_pressed[pygame.K_w] and blue.y - VELOCITY > 0: # UP
        blue.y -= VELOCITY
    if keys_pressed[pygame.K_s] and blue.y + VELOCITY + blue.height < HEIGHT - 15: # DOWN
        blue.y += VELOCITY

def red_movement(keys_pressed, red):

    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width: # LEFT
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH: # RIGHT
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0: # UP
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT - 15: # DOWN
        red.y += VELOCITY

def handle_bullets(blue_bullets, red_bullets, blue, red):

    for bullet in blue_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_COLLIDE))
            blue_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            blue_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_COLLIDE))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)

# MAIN FUNCTION
def main():
    blue = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    blue_bullets = []
    red_bullets = []

    blue_health = 10
    red_health = 10

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue.x + blue.width, blue.y + blue.height//2 - 2, 10, 5)
                    blue_bullets.append(bullet)
                    BLASTER_SOUND.play()
                if event.key == pygame.K_SLASH and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BLASTER_SOUND.play()
        
            if event.type == RED_COLLIDE:
                red_health -= 1
                COLLISION_SOUND.play()

            if event.type == BLUE_COLLIDE:
                blue_health -= 1
                COLLISION_SOUND.play()
        
        winner_text = ""
        if red_health <= 0:
            winner_text = "Blue Wins!"

        if blue_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        blue_movement(keys_pressed, blue)
        red_movement(keys_pressed, red)
        handle_bullets(blue_bullets, red_bullets, blue, red)
        draw_window(blue, red, blue_bullets, red_bullets, red_health, blue_health)

    main()

if __name__ == "__main__":
    main()
