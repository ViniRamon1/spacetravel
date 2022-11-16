import random
from turtle import up

import pygame
from pygame.locals import *

WIDTH = 500
HEIGHT = 700
SPEED = 10
GAME_SPEED = 0
PIPE_WIDTH = 120
PIPE_HEIGHT = 600
PIPE_GAP = 100


class Nave(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('bluebird-upflap.png'),
                       pygame.image.load('bluebird-midflap.png'),
                       pygame.image.load('bluebird-downflap.png')]

        self.current_image = 0

        self.speed = SPEED

        self.image = pygame.image.load('bluebird-upflap.png')
        self.mask = pygame.mask.from_surface(self.image)


        self.rect = self.image.get_rect()
        self.rect[0] = 1
        self.rect[1] = HEIGHT/2
        

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]

    def up(self):
        self.rect[1] -= 10

    def down(self):
        self.rect[1] += 10

    def right(self):
        self.rect[0] += 10

    def left(self):
        self.rect[0] -= 10

class Pipe(pygame.sprite.Sprite):
    global GAME_SPEED

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED


def random_pipes(xpos):
    size = random.randint(150,550)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True , xpos, HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)


def off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def createText(msg, color, tam):
    font = pygame.font.SysFont(None, tam)
    texto1 = font.render(msg, True, color)
    return texto1

def resetGame():
    global score, colisao, colidiu
    colidiu = False
    colisao = False
    score = 0
    nave.rect[0] = 1
    nave.rect[1] = HEIGHT/2
    pipe_group.remove(pipe_group.sprites()[0])
    pipe_group.remove(pipe_group.sprites()[0])
    pipes = random_pipes(WIDTH * 2)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])
    pipe_group.update()
    pipe_group.draw(screen)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
menuImg = pygame.image.load('Menu_screen.jpg')
gameover = pygame.image.load('gameover.png')
BACKGROUND = pygame.image.load('image.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
JBACKGROUND = pygame.image.load('background-day.png')
JBACKGROUND = pygame.transform.scale(JBACKGROUND, (WIDTH, HEIGHT))
nave_group = pygame.sprite.Group()
fonte = pygame.font.SysFont("arial", 25, False, False)
pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = random_pipes(WIDTH * i + 700)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])


screen = pygame.display.set_mode((WIDTH, HEIGHT))
score = 0
colisao = False
colidiu = False
exit = True
nave = Nave()

clock = pygame.time.Clock()
pygame.display.set_caption("Star Travel")
screen.blit(menuImg, (0, 0))

while exit:
    if colidiu == False:
        clock.tick(25)
        mensagem = f'Score: {score}'
        texto_formatado = fonte.render(mensagem, True, (255,255,255))       

    if currentScreen == "Game":
        nave_group.add(nave)
        if colidiu == False:
            GAME_SPEED = 10
            score+=1
            screen.blit(JBACKGROUND, (0, 0))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                  nave.up()
            if keys[pygame.K_DOWN]:
                nave.down()
            if keys[pygame.K_RIGHT]:
                nave.right()
            if keys[pygame.K_LEFT]:
                nave.left()
        
    for event in pygame.event.get():
        if event.type == QUIT:
            exit = False
        if event.type == KEYDOWN:
            if event.key == K_r:
                resetGame()

    colisao = (pygame.sprite.groupcollide(nave_group, pipe_group, False, False, pygame.sprite.collide_mask))

    if(colisao):
        colidiu = True
           
    if(colidiu):
        if ChangeMenu() == "Start":
            resetGame()
        elif ChangeMenu() == "Exit":
            exit = False
        screen.blit(menuImg, (0, 0))
        printDeath()
    else:
        if off_screen(pipe_group.sprites()[0]):
            pipe_group.remove(pipe_group.sprites()[0])
            pipe_group.remove(pipe_group.sprites()[0])
            pipes = random_pipes(WIDTH * 2)

            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])

        nave_group.update()
        pipe_group.update()

        nave_group.draw(screen)
        pipe_group.draw(screen)
        screen.blit(texto_formatado, (0, 0))
    
    pygame.display.update()