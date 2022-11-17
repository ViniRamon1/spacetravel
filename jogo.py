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


def printDeath():
    global score
    screen.blit(gameover, (WIDTH/2, HEIGHT/2))
    mensagem1 = f'Score: {score}'
    scorePrint = fonte.render(mensagem1, (255,255,255) , 30)
    screen.blit(scorePrint, (200, 300))
    
def ChangeMenu():
    mx, my = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed() == (1, 0, 0):
        if 85 <= mx and mx <= 210 and 400 <= my and my <= 520:
            return "Start"
        elif 160 <= mx and mx <= 285 and 545 <= my and my <= 670:
            return "Exit"
        elif 255 <= mx and mx <= 388 and 400 <= my and my <= 525:
            return "Tutorial"
        elif 17 <= mx and mx <= 100 and 610 <= my and my <= 680:
            return "ReturnMenu"

def telaMorte():
    mx, my = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed() == (1, 0, 0):
        if 85 <= mx and mx <= 210 and 400 <= my and my <= 520:
            return "Start"
        elif 160 <= mx and mx <= 285 and 545 <= my and my <= 670:
            return "Exit"

class Opening(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('opening1.png'),pygame.image.load('opening2.png'),pygame.image.load('opening3.png'),pygame.image.load('opening4.png'),pygame.image.load('opening5.png'),pygame.image.load('opening6.png'),pygame.image.load('opening7.png'),pygame.image.load('opening8.png'),pygame.image.load('opening9.png'),pygame.image.load('opening10.png'),pygame.image.load('opening11.png'),pygame.image.load('opening12.png'),pygame.image.load('opening13.png'),pygame.image.load('opening14.png'),pygame.image.load('opening15.png'),pygame.image.load('opening16.png'),pygame.image.load('opening17.png'),pygame.image.load('opening18.png'),pygame.image.load('opening19.png'),pygame.image.load('opening20.png'),pygame.image.load('opening21.png'),pygame.image.load('opening22.png'),pygame.image.load('opening23.png'),pygame.image.load('opening24.png'),pygame.image.load('opening25.png')]

        self.current_image = 0

        self.image = pygame.image.load('opening1.png')
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = 0
        self.rect[1] = 0

    def update(self):
        self.current_image = (self.current_image + 1) % 25
        self.image = self.images[ self.current_image ]

class Menu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('menu1.png'),
                       pygame.image.load('menu2.png'),
                       pygame.image.load('menu3.png')]
        
        self.current_image = 0

        self.image = pygame.image.load('menu1.png')
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = 0
        self.rect[1] = 0

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]

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
    global score, colisao, colidiu, SPEED, telaAtual
    SPEED = 10
    colidiu = False
    colisao = False
    score = 0
    telaAtual = 0
    nave.rect[0] = 1
    nave.rect[1] = HEIGHT/2
    pipe_group.empty()
    for i in range(2):
        pipes = random_pipes(WIDTH * i + 700)
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
currentScreen = "Abertura"
clock = pygame.time.Clock()
pygame.display.set_caption("Star Travel")
screen.blit(menuImg, (0, 0))

while exit:
    if colidiu == False:
        clock.tick(25)
        mensagem = f'Score: {score}'
        texto_formatado = fonte.render(mensagem, True, (255,255,255))

        if currentScreen == "Abertura":
            opening_group.add(opening)
            opening_group.draw(screen)
            opening_group.update()
            screen.blit(texto_Opening, (100,400))
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        currentScreen = "Menu"

        if currentScreen == "Menu":
            menu_group.add(menu)
            menu_group.draw(screen)
            menu_group.update()

        if ChangeMenu() == "Exit" and currentScreen == "Menu":
            exit = False
        elif ChangeMenu() == "Start" and currentScreen == "Menu":
            currentScreen = "Game"
        elif ChangeMenu() == "Tutorial" and currentScreen == "Menu":
            currentScreen = "Tutorial"
            screen.blit(TutorialImg, (0, 0))
        elif ChangeMenu() == "ReturnMenu" and currentScreen == "Tutorial":
            currentScreen = "Menu"
            screen.blit(menuImg, (0, 0))

    if currentScreen == "Game":
        nave_group.add(nave)
        if colidiu == False:
            GAME_SPEED = 10
            if score >= 1000:
                SPEED = 15
                GAME_SPEED = 15
            if score >= 2500:
                SPEED = 20
                GAME_SPEED = 20
            score+=1
            screen.blit(JBACKGROUND, (0, 0))
            screen.blit(texto_formatado, (0, 0))
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
            if event.key == K_x:
                resetGame()
                score = 1000
            if event.key == K_z:
                resetGame()
                score = 2500

    colisao = (pygame.sprite.groupcollide(nave_group, pipe_group, False, False, pygame.sprite.collide_mask))

    if(colisao):
        #tela de morte
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