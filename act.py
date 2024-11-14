import pygame, sys, random
from pygame.locals import *

# Inicializar Pygame
pygame.init()
relojPrincipal = pygame.time.Clock()

ANCHOVENTANA = 600
ALTURAVENTANA = 400
superficieVentana = pygame.display.set_mode((ANCHOVENTANA, ALTURAVENTANA), 0, 32)
pygame.display.set_caption('Simulación de Almacén')

NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)

TAMAÑOROBOT = 40
TAMAÑOCAJA = 20
TAMAÑOSTANTE = 80

robot = pygame.Rect(50, 50, TAMAÑOROBOT, TAMAÑOROBOT)
cajas = [pygame.Rect(random.randint(0, ANCHOVENTANA - TAMAÑOCAJA),
                     random.randint(0, ALTURAVENTANA - TAMAÑOCAJA),
                     TAMAÑOCAJA, TAMAÑOCAJA) for _ in range(20)]
estante1 = pygame.Rect(ANCHOVENTANA - 100, 50, TAMAÑOSTANTE, TAMAÑOSTANTE)
estante2 = pygame.Rect(ANCHOVENTANA - 100, ALTURAVENTANA - 150, TAMAÑOSTANTE, TAMAÑOSTANTE)

moverseIzquierda = False
moverseDerecha = False
moverseArriba = False
moverseAbajo = False
VELOCIDADMOVIMIENTO = 5

cajaEnMano = None

# Bucle principal del juego
while True:
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == KEYDOWN:
            if evento.key == K_LEFT:
                moverseIzquierda = True
            if evento.key == K_RIGHT:
                moverseDerecha = True
            if evento.key == K_UP:
                moverseArriba = True
            if evento.key == K_DOWN:
                moverseAbajo = True
        if evento.type == KEYUP:
            if evento.key == K_LEFT:
                moverseIzquierda = False
            if evento.key == K_RIGHT:
                moverseDerecha = False
            if evento.key == K_UP:
                moverseArriba = False
            if evento.key == K_DOWN:
                moverseAbajo = False

            #Agarrar y soltar cajas
            if evento.key == ord('p') and cajaEnMano is None:
                for caja in cajas:
                    if robot.colliderect(caja):
                        cajaEnMano = caja
                        cajas.remove(caja)
                        break
            if evento.key == ord('d') and cajaEnMano is not None:
                
                if robot.colliderect(estante1) or robot.colliderect(estante2):
                    cajaEnMano = None

    if moverseIzquierda and robot.left > 0:
        robot.left -= VELOCIDADMOVIMIENTO
    if moverseDerecha and robot.right < ANCHOVENTANA:
        robot.right += VELOCIDADMOVIMIENTO
    if moverseArriba and robot.top > 0:
        robot.top -= VELOCIDADMOVIMIENTO
    if moverseAbajo and robot.bottom < ALTURAVENTANA:
        robot.bottom += VELOCIDADMOVIMIENTO

    if cajaEnMano is not None:
        cajaEnMano.center = robot.center

    superficieVentana.fill(NEGRO)

    pygame.draw.rect(superficieVentana, BLANCO, robot)

    for caja in cajas:
        pygame.draw.rect(superficieVentana, VERDE, caja)

    if cajaEnMano is not None:
        pygame.draw.rect(superficieVentana, ROJO, cajaEnMano)

    pygame.draw.rect(superficieVentana, AZUL, estante1)
    pygame.draw.rect(superficieVentana, AZUL, estante2)

    pygame.display.update()
    relojPrincipal.tick(40)
