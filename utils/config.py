import time
import pyxel
import random

from clases.configNivel import ConfigNivel

scl = 4
WIDTH, HEIGHT = 1024 / scl, 512 / scl
# Las posiciones en las que puede estar un paquete en la cinta (columnas de la matriz)

# Depende de la dificultad # DEBUG: Con números múltiplos de 5 curiosamente luigi y mario se ponen exactamente en la plataforma
# Separación entre cintas

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


def esCintaPar(indice, numCintas):
    # El último índice (self.longitudY - 1) siempre debe ser impar (num = 0)
    nuevoIndice = (numCintas - 1) - indice
    return nuevoIndice % 2 == 0

# Devuelve un objeto ConfigNivel


def asignarDificultad(dificultad: str) -> ConfigNivel:
    # Valores por defecto
    controlesMario = (pyxel.KEY_UP, pyxel.KEY_DOWN)
    controlesLuigi = (pyxel.KEY_W, pyxel.KEY_S)
    velCinta0 = 0.5
    velCintasPares = 1
    velCintasImpares = 1

    # Numero de segundos que pasan hasta que salga un paquete
    intervalos = [3.5, 3.5, 14, 7, 3.5, 7]

    if dificultad == "facil":
        numCintas = 5
        anadirPaquetesCada = 50
        eliminaFallos = 3
    elif dificultad == "normal":
        numCintas = 7
        velCintasPares = 1
        velCintasImpares = 1.5
        anadirPaquetesCada = 30
        eliminaFallos = 5
    elif dificultad == "dificil":
        numCintas = 9
        velCintasPares = 1.5
        velCintasImpares = 2
        anadirPaquetesCada = 30
        eliminaFallos = 5

        for i in range(len(intervalos)):
            intervalos[i] /= 1.5

    elif dificultad == "crazy":
        controlesMario = (pyxel.KEY_DOWN, pyxel.KEY_UP)
        controlesLuigi = (pyxel.KEY_S, pyxel.KEY_W)
        numCintas = 5
        velCintasPares = random.uniform(1, 2)
        velCintasImpares = random.uniform(1, 2)
        anadirPaquetesCada = 20
        eliminaFallos = 10000
        
        for i in range(len(intervalos)):
            intervalos[i] /= 1.5

    else:
        raise ValueError("Dificultad seleccionada no válida")

    # Añadimos parámetros independientes a la dificultad
    numPaqCinta = 30
    sepEntreCintas = (HEIGHT - 25) / numCintas
    anchoPaq, altoPaq = 7, 4

    return ConfigNivel(
        controlesMario,
        controlesLuigi,
        velCinta0,
        velCintasPares,
        velCintasImpares,
        numCintas,
        anadirPaquetesCada,
        eliminaFallos,
        numPaqCinta,
        sepEntreCintas,
        anchoPaq,
        altoPaq,
        dificultad,
        intervalos
    )

# Devuelve el menor valor


def minimo(a, b):
    if a > b:
        return b
    else:
        return a
