import time

scl = 4
WIDTH, HEIGHT = 1024 / scl, 512 / scl
# Las posiciones en las que puede estar un paquete en la cinta (columnas de la matriz)
NUM_PAQ_CIN = 50
DIFICULTAD = "facil"
NUM_CINTAS = 5  # Depende de la dificultad
# Separación entre cintas
SEP_ENTRE_CINTAS = (HEIGHT - 25) / NUM_CINTAS

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
