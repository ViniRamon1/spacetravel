from turtle import up
import pygame , random
from pygame.locals import *

WIDTH = 400
HEIGHT = 600
SPEED = 10
GAME_SPEED = 10
GROUND_WIDTH = 2*WIDTH
GROUND_HEIGHT = 100
PIPE_WIDTH = 120
PIPE_HEIGHT = 500
PIPE_GAP = 100


class Nave(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load(),
                       pygame.image.load(),
                       pygame.image.load()]

        self.current_image = 0

        self.speed = SPEED

        self.image = pygame.image.load()
        self.mask = pygame.mask.from_surface(self.image)


        self.rect = self.image.get_rect()
        self.rect[0] = WIDTH/2
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

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load().convert_alpha()
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


        

class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED

def random_pipes(xpos):
    size = random.randint(100,250)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True , xpos, HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)


def off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

BACKGROUND = pygame.image.load()
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

nave_group = pygame.sprite.Group()
nave = Nave()
nave_group.add(nave)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH*i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = random_pipes(WIDTH * i + 600)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])


clock = pygame.time.Clock()

while True:
    clock.tick(30)

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
            pygame.quit()

        

        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                nave.down()
            if event.key == K_UP:
                nave.up()
            if event.key == K_RIGHT:
                nave.right()
            if event.key == K_LEFT:
                nave.left()

    screen.blit(BACKGROUND, (0, 0))

    if off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    if off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])
        pipes = random_pipes(WIDTH * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    nave_group.update()
    ground_group.update()
    pipe_group.update()

    nave_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)
    

    if (pygame.sprite.groupcollide(nave_group, ground_group, False, False, pygame.sprite.collide_mask) or pygame.sprite.groupcollide(nave_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        break


    pygame.display.update()