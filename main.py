import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # sets the length and height of the window
pygame.display.set_caption("The Khan Game")   #Title of the game

PURPLE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (255, 0, 0)
GREEN = (255, 255, 0)

BORDER = pygame.Rect(0, HEIGHT//2-5,WIDTH, 10)  #Puts the border line horizontal 

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets,' 'lazer.mp3' ))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets,''lazer.mp3' ))

HEALTH_FONT = pygame.font.SysFont('Times New Roman', 40)  #health font 
WINNER_FONT = pygame.font.SysFont('Times New Roman', 100)  #winner font

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 10 #shoots 10 bullets at a time
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 60  #chooses the width and the height of the spaceship

GREEN_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2

GREEN_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets,' 'spaceship_GREEN.png'))  #how I imported my green spaceship to the game
GREEN_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(  # rotation of spaceships
    GREEN_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 50)

BLUE_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets,' 'spaceship_BLUE.png'))  #how I imported my blue spaceship to the game
BLUE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    BLUE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 40)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets,' 'space.png')), (WIDTH, HEIGHT))


def draw_window(blue, green, blue_bullets, green_bullets, blue_health, green_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER) # this imports the border
    green_health_text = HEALTH_FONT.render("Health: " + str(green_health), 1, 'WHITE')
    blue_health_text = HEALTH_FONT.render("Health: " + str(blue_health), 1, 'WHITE')
                                            
    WIN.blit(blue_health_text, (WIDTH - blue_health_text.get_width() - 10, 10))
    WIN.blit(green_health_text, (10, 10))

    WIN.blit(GREEN_SPACESHIP, (green.x, green.y))
    WIN.blit(BLUE_SPACESHIP, (blue.x, blue.y))

    for bullet in blue_bullets:
        pygame.draw.rect(WIN, blue, bullet)

    for bullet in green_bullets:
        pygame.draw.rect(WIN, green, bullet)

    pygame.display.update()

#how to move
def green_handle_movement(keys_pressed, green):
    if keys_pressed[pygame.K_d] and green.x - VEL > 0:  #MOVES LEFT
        green.x -= VEL
    if keys_pressed[pygame.K_g] and green.x + VEL + green.width < BORDER. x:  #MOVES RIGHT
        green.x += VEL
    if keys_pressed[pygame.K_r] and green.y - VEL > 0:  #MOVES UP
        green.y -= VEL
    if keys_pressed[pygame.K_f] and green.y + VEL + green.height < HEIGHT - 15:  #MOVES DOWN
        green.y += VEL


def blue_handle_movement(keys_pressed,  blue):
    if keys_pressed[pygame.K_j] and blue.x - VEL > 0 :   # LEFT
        blue.x -= VEL
    if keys_pressed[pygame.K_l] and blue.x + VEL + 70 < WIDTH:  # RIGHT
        blue.x += VEL
    if keys_pressed[pygame.K_i] and blue.y + VEL > BORDER.y - 15:  # UP
        blue.y -= VEL
    if keys_pressed[pygame.K_k] and blue.y + VEL + 95 < HEIGHT:  # DOWN
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
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /  2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
   green = pygame.Rect(600, 100, 100, 100)
   blue = pygame.Rect(600, 550, 135, 80)
   
   blue_bullets = []
   green_bullets = []

   blue_health = 10    #How much lives both players start off with
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
                    if event.key == pygame.K_LCTRL and len(blue_bullets) < MAX_BULLETS:  # shoot keys for blue
                     bullet = pygame.Rect(
                        blue.x + blue.width, blue.y + blue.height//2 - 2, 10, 5)
                    blue_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(green_bullets) < MAX_BULLETS:  # shoot keys for green
                    bullet = pygame.Rect(
                        green.x, green.y + green.height//2 - 2, 10, 5)
                    green_bullets.append(bullet)
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