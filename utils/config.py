import time

scl = 4
WIDTH, HEIGHT = 1024 / scl, 512 / scl
# Las posiciones en las que puede estar un paquete en la cinta (columnas de la matriz)
NUM_PAQ_CIN = 64
DIFICULTAD = "facil"
NUM_CINTAS = 5  # Depende de la dificultad
# Separación entre cintas
SEP_ENTRE_CINTAS = (HEIGHT - 25) / NUM_CINTAS

TIEMPO, VIDAS = time.time(), 3
# NUM_CINTAS, TIEMPO, VIDAS, VEL = asignarValores(DIFICULTAD)


def cintaPar(indice):
    # El último índice (self.longitudY - 1) siempre is impar (num = 0)
    # DEBUG: self.longitudY == NUM_CINTAS ??
    nuevoIndice = (NUM_CINTAS - 1) - indice
    return nuevoIndice % 2 == 0
