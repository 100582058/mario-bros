import time
import pyxel
import random

scl = 4
WIDTH, HEIGHT = 1024 / scl, 512 / scl
# Las posiciones en las que puede estar un paquete en la cinta (columnas de la matriz)
NUM_PAQ_CIN = 40 # ANTES: 50 (Así va más rápido para probar cosas)
DIFICULTAD = "facil"
NUM_CINTAS = 5  # Depende de la dificultad #Con números múltiplos de 5 curiosamente luigi y mario se ponen exactamente en la plataforma
# Separación entre cintas
SEP_ENTRE_CINTAS = (HEIGHT - 25) / NUM_CINTAS
ANCHO_PAQ, ALTO_PAQ = 7, 4

TIEMPO, VIDAS = time.time(), 3
# NUM_CINTAS, TIEMPO, VIDAS, VEL = asignarValores(DIFICULTAD)

COLORES = {
    "negro": 0,
    "azulMarino": 1,
    "morado": 2,
    "azulCeleste": 3,
    "marron": 4,
    "azul": 5,
    "azulClaro": 6,
    "blanco": 7,
    "magenta": 8,
    "naranja": 9,
    "amarillo": 10,
    "verde": 11,
    "azul12": 12,
    "gris": 13,
    "rosa": 14,
    "carne": 15
}


def cintaPar(indice):
    # El último índice (self.longitudY - 1) siempre is impar (num = 0)
    # DEBUG: self.longitudY == NUM_CINTAS ??
    nuevoIndice = (NUM_CINTAS - 1) - indice
    return nuevoIndice % 2 == 0


def asignarDificultad(dificultad):
    CONTROLES_MARIO = (pyxel.KEY_UP, pyxel.KEY_DOWN)
    CONTROLES_LUIGI = (pyxel.KEY_W, pyxel.KEY_S)
    VEL_CINTA_0 = 1
    VEL_CINTAS_PARES = 1
    VEL_CINTAS_IMPARES = 1

    if dificultad == "facil":
        NUM_CINTAS = 6
        ANADIR_PAQUETES_CADA = 50
        ELIMINA_FALLOS = 3
    elif dificultad == "medio":
        NUM_CINTAS = 8
        VEL_CINTAS_PARES = 1
        VEL_CINTAS_IMPARES = 1.5
        ANADIR_PAQUETES_CADA = 30
        ELIMINA_FALLOS = 5
    elif dificultad == "extremo":
        NUM_CINTAS = 10
        VEL_CINTAS_PARES = 1.5
        VEL_CINTAS_IMPARES = 2
        ANADIR_PAQUETES_CADA = 30
        ELIMINA_FALLOS = 5
    elif dificultad == "crazy":
        CONTROLES_MARIO = (pyxel.KEY_DOWN, pyxel.KEY_UP)
        CONTROLES_LUIGI = (pyxel.KEY_S, pyxel.KEY_W)
        NUM_CINTAS = 6
        VEL_CINTAS_PARES = random.uniform(1, 2)
        VEL_CINTAS_IMPARES = random.uniform(1, 2)
        ANADIR_PAQUETES_CADA = 20
        ELIMINA_FALLOS = 10000

    return CONTROLES_MARIO, CONTROLES_LUIGI, VEL_CINTA_0, VEL_CINTAS_PARES, VEL_CINTAS_IMPARES, NUM_CINTAS,VEL_CINTAS_PARES,VEL_CINTAS_IMPARES,ANADIR_PAQUETES_CADA, ELIMINA_FALLOS


# CONTROLES_MARIO, CONTROLES_LUIGI, VEL_CINTA_0, VEL_CINTAS_PARES, VEL_CINTAS_IMPARES, NUM_CINTAS, VEL_CINTAS_PARES, VEL_CINTAS_IMPARES, ANADIR_PAQUETES_CADA, ELIMINA_FALLOS = asignarDificultad("facil")
