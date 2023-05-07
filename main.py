import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Khan Game")   #Title of the game

PURPLE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(0, HEIGHT//2-5,WIDTH, 10)

#BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
#BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('Times New Roman', 40)
WINNER_FONT = pygame.font.SysFont('Times New Roman', 100) 

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 100

GREEN_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2

GREEN_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets,' 'spaceship_GREEN.png'))
GREEN_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    GREEN_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

BLUE_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets,' 'spaceship_BLUE.png'))
BLUE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    BLUE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets,' 'space.png')), (WIDTH, HEIGHT))


def draw_window(blue, green, blue_bullets, green_bullets, blue_health, green_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    blue_health_text = HEALTH_FONT.render(
        "Health: " + str(blue_health), 1, PURPLE)
    green_health_text = HEALTH_FONT.render(
        "Health: " + str(green_health), 1, PURPLE)
    WIN.blit(blue_health_text, (WIDTH - blue_health_text.get_width() - 10, 10))
    WIN.blit(green_health_text, (10, 10))

    WIN.blit(GREEN_SPACESHIP, (green.x, green.y))
    WIN.blit(BLUE_SPACESHIP, (blue.x, blue.y))

    for bullet in blue_bullets:
        pygame.draw.rect(WIN, blue, bullet)

    for bullet in green_bullets:
        pygame.draw.rect(WIN, green, bullet)

    pygame.display.update()


def green_handle_movement(keys_pressed, green):
    if keys_pressed[pygame.K_q] and green.x - VEL > 0:  
        green.x -= VEL
    if keys_pressed[pygame.K_e] and green.x + VEL + green.width < BORDER. x:  
        green.x += VEL
    if keys_pressed[pygame.K_2] and green.y - VEL > 0:  
        green.y -= VEL
    if keys_pressed[pygame.K_w] and green.y + VEL + green.height < HEIGHT - 15:  
        green.y += VEL


def blue_handle_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_j] and blue.x - VEL > BORDER.x: 
        blue.x -= VEL
    if keys_pressed[pygame.K_l] and blue.x + VEL + blue.width < WIDTH:  
        blue.x += VEL
    if keys_pressed[pygame.K_i] and blue.y - VEL > 0: 
        blue.y -= VEL
    if keys_pressed[pygame.K_k] and blue.y + VEL > BORDER.x:
        blue.y += VEL

def handle_bullets(green_bullets, blue_bullets, green, blue):
    for bullet in green_bullets:
        bullet.x += BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            green_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            green_bullets.remove(bullet)

    for bullet in blue_bullets:
        bullet.x -= BULLET_VEL
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x < 0:
            blue_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, PURPLE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    blue = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    green = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    blue_bullets = []
    green_bullets = []

    blue_health = 10
    green_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(green_bullets) < MAX_BULLETS:  #Use left shift to shoot as green
                    bullet = pygame.Rect(
                        green.x + green.width, green.y + green.height//2 - 2, 10, 5)
                    green_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_LCTRL and len(blue_bullets) < MAX_BULLETS:  #Use right shift to shoot as blue
                    bullet = pygame.Rect(
                        blue.x, blue.y + blue.height//2 - 2, 10, 5)
                    blue_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()

            if event.type == BLUE_HIT:
                blue_health -= 1
                #BULLET_HIT_SOUND.play()

            if event.type == GREEN_HIT:
                green_health -= 1
                #BULLET_HIT_SOUND.play()

        winner_text = ""
        if blue_health <= 0:
            winner_text = "Green Wins!"  # prints this when green wins

        if green_health <= 0:
            winner_text = "Blue Wins!"   # prints this when blue wins

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        green_handle_movement(keys_pressed, green)
        blue_handle_movement(keys_pressed, blue)

        handle_bullets(green_bullets, blue_bullets, green, blue)

        draw_window(blue, green, blue_bullets, green_bullets,
                    blue_health, green_health)

    main()


if __name__ == "__main__":
    main()