#imporar bibliotecas
import random
from turtle import up

import pygame
from pygame.locals import *

pygame.init()

#soundtrack
musicadefundo = pygame.mixer.music.load('documentos/musica.mp3')
pygame.mixer.music.play(-1)

#Variaveis Padrão
WIDTH = 500
HEIGHT = 700
SPEED = 10
GAME_SPEED = 0
PIPE_WIDTH = 120
PIPE_HEIGHT = 600
PIPE_GAP = 100
score = 0
colisao = False
colidiu = False
exit = True

#Imagens
menuImg = pygame.image.load('documentos/menu1.png')
menuImg1 = pygame.image.load('documentos/menu2.png')
menuImg2 = pygame.image.load('documentos/menu3.png')
TutorialImg = pygame.image.load('documentos/instructions1.png')
gameover = pygame.image.load('documentos/gameover.png')
JBACKGROUND = pygame.image.load('documentos/space.png')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
JBACKGROUND = pygame.transform.scale(JBACKGROUND, (WIDTH, HEIGHT))

#Funcoes

#funcao menu, botoes: start, minitutorial, exit e para retornar menu
def ChangeMenu():
    mx, my = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed() == (1, 0, 0):
        if 164 <= mx and mx <= 325 and 435 <= my and my <= 500:
            return "Start"
        elif 185 <= mx and mx <= 310 and 525 <= my and my <= 585:
            return "Tutorial"
        elif 185 <= mx and mx <= 310 and 605 <= my and my <= 665:
            return "Exit"
        elif 17 <= mx and mx <= 100 and 610 <= my and my <= 680:
            return "ReturnMenu"

#menu pos morte, com restart e exit
def telaMorte():
    mx, my = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed() == (1, 0, 0):
        if 125 <= mx and mx <= 230 and 410 <= my and my <= 500:
            return "Start"
        elif 275 <= mx and mx <= 365 and 420 <= my and my <= 500:
            return "Exit"

#Abertura animada
class Opening(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('documentos/opening1.png'),pygame.image.load('documentos/opening2.png'),pygame.image.load('documentos/opening3.png'),pygame.image.load('documentos/opening4.png'),pygame.image.load('documentos/opening5.png'),pygame.image.load('documentos/opening6.png'),pygame.image.load('documentos/opening7.png'),pygame.image.load('documentos/opening8.png'),pygame.image.load('documentos/opening9.png'),pygame.image.load('documentos/opening10.png'),pygame.image.load('documentos/opening11.png'),pygame.image.load('documentos/opening12.png'),pygame.image.load('documentos/opening13.png'),pygame.image.load('documentos/opening14.png'),pygame.image.load('documentos/opening15.png'),pygame.image.load('documentos/opening16.png'),pygame.image.load('documentos/opening17.png'),pygame.image.load('documentos/opening18.png'),pygame.image.load('documentos/opening19.png'),pygame.image.load('documentos/opening20.png'),pygame.image.load('documentos/opening21.png'),pygame.image.load('documentos/opening22.png'),pygame.image.load('documentos/opening23.png'),pygame.image.load('documentos/opening24.png'),pygame.image.load('documentos/opening25.png')]

        self.current_image = 0

        self.image = pygame.image.load('documentos/opening1.png')
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = 0
        self.rect[1] = 0

    def update(self):
        self.current_image = (self.current_image + 1) % 25
        self.image = self.images[ self.current_image ]

#menu com animação de entrada
class Menu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('documentos/menu1.png'),
                       pygame.image.load('documentos/menu2.png'),
                       pygame.image.load('documentos/menu3.png')]
        
        self.current_image = 0

        self.image = pygame.image.load('documentos/menu1.png')
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = 0
        self.rect[1] = 0

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]

#nave e animação
class Nave(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('documentos/spaceship1.png'),
                       pygame.image.load('documentos/spaceship2.png'),
                       pygame.image.load('documentos/spaceship3.png')]

        self.current_image = 0

        self.image = pygame.image.load('documentos/spaceship1.png')
        self.mask = pygame.mask.from_surface(self.image)


        self.rect = self.image.get_rect()
        posicionar(self)
        

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]

    def up(self):
        self.rect[1] -= SPEED

    def down(self):
        self.rect[1] += SPEED

    def right(self):
        self.rect[0] += SPEED

    def left(self):
        self.rect[0] -= SPEED

#canos
class Pipe(pygame.sprite.Sprite):
    global GAME_SPEED

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('documentos/pipe.png').convert_alpha()
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


#funcao para aleatorizar a geração de canos
def random_pipes(xpos):
    size = random.randint(150,550)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True , xpos, HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)

#funcao que detecta quando algo esta fora da tela
def off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def off_screen_aux():
    pipe_group.remove(pipe_group.sprites()[0])
    pipe_group.remove(pipe_group.sprites()[0])
    pipes = random_pipes(WIDTH * 2)

    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

def gerar_canos():
    for i in range(2):
        pipes = random_pipes(WIDTH * i + 700)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

#funcao para resetar o game
def resetGame():
    global score, colisao, colidiu, SPEED, telaAtual
    SPEED = 10
    colidiu = False
    colisao = False
    score = 0
    telaAtual = 0
    posicionar(nave)
    pipe_group.empty()
    gerar_canos()
    pipe_group.update()
    pipe_group.draw(screen)

def posicionar(self):
    self.rect[0] = 1
    self.rect[1] = HEIGHT/2

#adiciona teclas de atalho para pular de dificuldade 
def atalho():
    global score
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_x:
                resetGame()
                score = 1000 #media
            if event.key == K_z:
                resetGame()
                score = 2500 #dificil

#funcao para mover a nave
def movernave():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        nave.up()
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        nave.down()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        nave.right()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        nave.left()

#funcao para iniciar abertura
def oppening():
    global exit, currentScreen
    opening_group.add(opening)
    opening_group.draw(screen)
    opening_group.update()
    screen.blit(texto_Opening, (100,400))
    for event in pygame.event.get():
        if event.type == QUIT:
            exit = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                currentScreen = "Menu"

#Texto
pygame.display.set_caption("Space Travel")
fonte = pygame.font.SysFont("arial", 25, False, False)
mensagemOpening = f'Pressione Espaço para continuar'
texto_Opening = fonte.render(mensagemOpening, True , (255,255,255))

#Variaveis e funcoes para o jogo funcionar
currentScreen = "Abertura" #tela padrao
opening_group = pygame.sprite.Group()
nave_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
clock = pygame.time.Clock()
menu_group = pygame.sprite.Group()
nave = Nave()
menu = Menu()
opening = Opening()

#Gerar canos
gerar_canos()

#jogo
while exit:
    if colidiu == False:
        clock.tick(25)
        mensagem = f'Score: {score}'
        texto_formatado = fonte.render(mensagem, True, (255,255,255))

        if currentScreen == "Abertura":
            oppening()

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
            movernave()
            atalho()

    for event in pygame.event.get():
        if event.type == QUIT:
            exit = False

    colisao = (pygame.sprite.groupcollide(nave_group, pipe_group, False, False, pygame.sprite.collide_mask))

    if(colisao):
        colidiu = True
           
    if(colidiu):
        if telaMorte() == "Start":
            resetGame()
        elif telaMorte() == "Exit":
            exit = False
        screen.blit(gameover, (0, 0))
        screen.blit(texto_formatado, (200, 300))
    else:
        if off_screen(pipe_group.sprites()[0]):
            off_screen_aux()

        nave_group.update()
        pipe_group.update()

        nave_group.draw(screen)
        pipe_group.draw(screen)
    
    pygame.display.update()
