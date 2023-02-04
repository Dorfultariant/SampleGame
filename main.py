import pygame
import os

pygame.font.init()

WIDTH, HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First Game")

WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

HEALTH_FONT = pygame.font.SysFont('comicsans', 50)

ROUND_HIT = pygame.USEREVENT + 1
SQUARE_HIT = pygame.USEREVENT + 2

FPS = 60
VELOCITY = 20

BORDER = pygame.Rect(WIDTH//2, 0, 10, HEIGHT)
BULLET_VEL = 16
MAX_BULLETS = 3

FACE_W, FACE_H = 100, 100

ROUNDFACE = pygame.image.load(os.path.join('Assets', 'happysad.png'))
ROUNDFACE = pygame.transform.scale(ROUNDFACE, (FACE_W,FACE_H))

SQUAREFACE = pygame.image.load(os.path.join('Assets', 'square.png'))
SQUAREFACE = pygame.transform.scale(SQUAREFACE, (FACE_W,FACE_H))

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'BackGround.png')), (WIDTH,HEIGHT))


def draw_window(round, square, round_bullets, square_bullets, round_health, square_health):
    WIN.blit(BACKGROUND,(0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    round_health_text = HEALTH_FONT.render("Health: " + str(round_health), 1, WHITE)

    square_health_text = HEALTH_FONT.render("Health: " + str(square_health), 1, WHITE)

    WIN.blit(round_health_text, (WIDTH - round_health_text.get_width() - 10, 10))
    WIN.blit(square_health_text, (10,10))
    WIN.blit(ROUNDFACE, (round.x,round.y))
    WIN.blit(SQUAREFACE, (square.x,square.y))
    
    for bullet in round_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in square_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


def roundMovement(keys_pressed, round):
    if keys_pressed[pygame.K_a] and round.x - VELOCITY > 0:
        round.x -= VELOCITY
    if keys_pressed[pygame.K_d] and round.x + VELOCITY + round.width < BORDER.x:
        round.x += VELOCITY
    if keys_pressed[pygame.K_w] and round.y - VELOCITY > 0:
        round.y -= VELOCITY
    if keys_pressed[pygame.K_s] and round.y + VELOCITY + round.height < HEIGHT - 60:
        round.y += VELOCITY



def squareMovement(keys_pressed, square):
    if keys_pressed[pygame.K_LEFT] and square.x - VELOCITY > BORDER.x + BORDER.width:
        square.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and square.x + VELOCITY + square.width < WIDTH:
        square.x += VELOCITY
    if keys_pressed[pygame.K_UP] and square.y - VELOCITY > 0:
        square.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and square.y + VELOCITY + square.height < HEIGHT - 60:
        square.y += VELOCITY


def handle_bullets(round_bullets, square_bullets, round, square):
    for bullet in round_bullets:
        bullet.x += BULLET_VEL
        if square.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SQUARE_HIT))
            round_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            round_bullets.remove(bullet)

    for bullet in square_bullets:
        bullet.x -= BULLET_VEL
        if round.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ROUND_HIT))
            square_bullets.remove(bullet)
        elif bullet.x < 0:
            square_bullets.remove(bullet)


def main():
    round = pygame.Rect(300,100,FACE_W, FACE_H)
    square = pygame.Rect(1300,100,FACE_W, FACE_H)

    bullets = []
    round_bullets = []
    square_bullets = []

    round_health = 10
    square_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(round_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        round.x + round.width, round.y + round.height//2 - 2, 10, 5)
                    round_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(square_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        square.x, square.y + square.height//2 - 2, 10, 5)
                    square_bullets.append(bullet)

            if event.type == SQUARE_HIT:
                round_health -= 1
            
            if event.type == ROUND_HIT:
                square_health -= 1
        
        winner_text = ""
        if round_health <= 0:
            winner_text = "Square wins"

        if square_health <= 0:
            winner_text = "Round wins"

        if winner_text != "":
            pass


        keys_pressed = pygame.key.get_pressed()
        roundMovement(keys_pressed, round)
        squareMovement(keys_pressed, square)

        handle_bullets(round_bullets,square_bullets, round, square)

        draw_window(round, square, round_bullets, square_bullets, round_health, square_health)

    pygame.quit()

if __name__ == "__main__":
    main()
