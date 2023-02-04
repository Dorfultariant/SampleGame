import pygame
import os

WIDTH, HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First Game")

WHITE = (255,255,255)
BLACK = (0, 0, 0)

FPS = 60
VELOCITY = 20

BORDER = pygame.Rect(WIDTH/2, 0, 10, HEIGHT)

FACE_W, FACE_H = 100, 100

ROUNDFACE = pygame.image.load(os.path.join('Assets', 'happysad.png'))
ROUNDFACE = pygame.transform.scale(ROUNDFACE, (FACE_W,FACE_H))

SQUAREFACE = pygame.image.load(os.path.join('Assets', 'square.png'))
SQUAREFACE = pygame.transform.scale(SQUAREFACE, (FACE_W,FACE_H))


def draw_window(round, square):
    WIN.fill(WHITE)
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(ROUNDFACE, (round.x,round.y))
    WIN.blit(SQUAREFACE, (square.x,square.y))
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



def main():
    round = pygame.Rect(300,100,FACE_W, FACE_H)
    square = pygame.Rect(1300,100,FACE_W, FACE_H)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys_pressed = pygame.key.get_pressed()
        roundMovement(keys_pressed, round)
        squareMovement(keys_pressed, square)

        draw_window(round, square)

    pygame.quit()

if __name__ == "__main__":
    main()
