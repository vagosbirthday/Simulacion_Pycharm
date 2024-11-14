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
formas = ["cuadrado", "circulo", "triangulo"]
cajaEnMano = None
contadorCajasDejadas = 0  # Inicializamos el contador de cajas dejadas

# Crear los estantes específicos para cada forma con coordenadas
estanteCuadrado = pygame.Rect(ANCHOVENTANA - 100, 50, TAMAÑOSTANTE, TAMAÑOSTANTE)
estanteCirculo = pygame.Rect(ANCHOVENTANA - 100, ALTURAVENTANA - 150, TAMAÑOSTANTE, TAMAÑOSTANTE)
estanteTriangulo = pygame.Rect(50, ALTURAVENTANA - 150, TAMAÑOSTANTE, TAMAÑOSTANTE)

# Crear múltiples cajas de cada forma en posiciones aleatorias
cajas = [{"rect": pygame.Rect(random.randint(0, ANCHOVENTANA - TAMAÑOCAJA),
                              random.randint(0, ALTURAVENTANA - TAMAÑOCAJA),
                              TAMAÑOCAJA, TAMAÑOCAJA),
          "forma": random.choice(formas)} for _ in range(5)]  # Genera 5 cajas

# Variables de movimiento
moverseIzquierda = False
moverseDerecha = False
moverseArriba = False
moverseAbajo = False
VELOCIDADMOVIMIENTO = 5

# Fuente para el contador
fuente = pygame.font.SysFont(None, 36)

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

            # Agarrar y soltar cajas
            if evento.key == ord('a') and cajaEnMano is None:
                for caja in cajas:
                    if robot.colliderect(caja["rect"]):
                        cajaEnMano = caja
                        cajas.remove(caja)
                        break
            if evento.key == ord('d') and cajaEnMano is not None:
                # Verificar si la caja en mano está en el estante correcto
                if cajaEnMano["forma"] == "cuadrado" and robot.colliderect(estanteCuadrado):
                    cajaEnMano["rect"].center = estanteCuadrado.center
                    contadorCajasDejadas += 1
                    cajaEnMano = None
                    cajas.append({"rect": pygame.Rect(random.randint(0, ANCHOVENTANA - TAMAÑOCAJA),
                                                      random.randint(0, ALTURAVENTANA - TAMAÑOCAJA),
                                                      TAMAÑOCAJA, TAMAÑOCAJA),
                                  "forma": "cuadrado"})
                elif cajaEnMano["forma"] == "circulo" and robot.colliderect(estanteCirculo):
                    cajaEnMano["rect"].center = estanteCirculo.center
                    contadorCajasDejadas += 1
                    cajaEnMano = None
                    cajas.append({"rect": pygame.Rect(random.randint(0, ANCHOVENTANA - TAMAÑOCAJA),
                                                      random.randint(0, ALTURAVENTANA - TAMAÑOCAJA),
                                                      TAMAÑOCAJA, TAMAÑOCAJA),
                                  "forma": "circulo"})
                elif cajaEnMano["forma"] == "triangulo" and robot.colliderect(estanteTriangulo):
                    cajaEnMano["rect"].center = estanteTriangulo.center
                    contadorCajasDejadas += 1
                    cajaEnMano = None
                    cajas.append({"rect": pygame.Rect(random.randint(0, ANCHOVENTANA - TAMAÑOCAJA),
                                                      random.randint(0, ALTURAVENTANA - TAMAÑOCAJA),
                                                      TAMAÑOCAJA, TAMAÑOCAJA),
                                  "forma": "triangulo"})

    if moverseIzquierda and robot.left > 0:
        robot.left -= VELOCIDADMOVIMIENTO
    if moverseDerecha and robot.right < ANCHOVENTANA:
        robot.right += VELOCIDADMOVIMIENTO
    if moverseArriba and robot.top > 0:
        robot.top -= VELOCIDADMOVIMIENTO
    if moverseAbajo and robot.bottom < ALTURAVENTANA:
        robot.bottom += VELOCIDADMOVIMIENTO

    if cajaEnMano is not None:
        cajaEnMano["rect"].center = robot.center

    superficieVentana.fill(NEGRO)

    # Dibujar estantes en las formas correspondientes
    pygame.draw.rect(superficieVentana, AZUL, estanteCuadrado)  # Estante para cuadrado
    pygame.draw.ellipse(superficieVentana, AZUL, estanteCirculo)  # Estante para círculo
    puntosTriangulo = [
        (estanteTriangulo.centerx, estanteTriangulo.top),
        (estanteTriangulo.bottomleft),
        (estanteTriangulo.bottomright)
    ]
    pygame.draw.polygon(superficieVentana, AZUL, puntosTriangulo)  # Estante para triángulo

    # Dibujar el robot
    pygame.draw.rect(superficieVentana, BLANCO, robot)

    # Dibujar las cajas
    for caja in cajas:
        if caja["forma"] == "cuadrado":
            pygame.draw.rect(superficieVentana, VERDE, caja["rect"])
        elif caja["forma"] == "circulo":
            pygame.draw.ellipse(superficieVentana, VERDE, caja["rect"])
        elif caja["forma"] == "triangulo":
            puntos = [
                (caja["rect"].centerx, caja["rect"].top),
                (caja["rect"].bottomleft),
                (caja["rect"].bottomright)
            ]
            pygame.draw.polygon(superficieVentana, VERDE, puntos)

    # Dibujar la caja en mano si existe
    if cajaEnMano is not None:
        if cajaEnMano["forma"] == "cuadrado":
            pygame.draw.rect(superficieVentana, ROJO, cajaEnMano["rect"])
        elif cajaEnMano["forma"] == "circulo":
            pygame.draw.ellipse(superficieVentana, ROJO, cajaEnMano["rect"])
        elif cajaEnMano["forma"] == "triangulo":
            puntos = [
                (cajaEnMano["rect"].centerx, cajaEnMano["rect"].top),
                (cajaEnMano["rect"].bottomleft),
                (cajaEnMano["rect"].bottomright)
            ]
            pygame.draw.polygon(superficieVentana, ROJO, puntos)

    # Mostrar el contador en pantalla
    textoContador = fuente.render(f'Cajas Colocadas: {contadorCajasDejadas}', True, BLANCO)
    superficieVentana.blit(textoContador, (10, 10))

    pygame.display.update()
    relojPrincipal.tick(40)
