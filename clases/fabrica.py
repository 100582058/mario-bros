import pyxel
import random

from clases.personaje import Personaje
from clases.paquetes import Paquetes
from clases.camion import Camion

class Fabrica:
    def __init__(self, tiempo, vidas, POS_PAQ_CIN, NUM_CINTAS):
        self.vidas = vidas # Cambian en función de la dificultad
        self.tiempo = tiempo # tiempo del nivel
        # self.dificultad = dificultad # 3 tipos
        # DEBUG: En __init__() ???
        # Inicializamos los personajes
        controlesMario = (pyxel.KEY_UP, pyxel.KEY_DOWN)
        controlesLuigi = (pyxel.KEY_W, pyxel.KEY_S)
        self.luigi = Personaje("luigi", controlesLuigi, 100, 200)
        self.mario = Personaje("mario", controlesMario, 400, 200)
        print(repr(self.mario), repr(self.luigi))

        self.camion = Camion(20, 30)
        print(repr(self.camion))
        self.paquetes = Paquetes(POS_PAQ_CIN, NUM_CINTAS)
        print(repr(self.paquetes), "\n")
        # Añade un paquete en la posición inicial
        self.paquetes.anadirPaquete()

    @property
    def vidas(self):
        return self.__vidas

    @vidas.setter
    def vidas(self, valor):
        self.__vidas = valor

    @property
    def tiempo(self):
        return self.__tiempo

    @tiempo.setter
    def tiempo(self, valor):
        self.__tiempo = valor

    @property
    def dificultad(self):
        return self.__dificultad

    @dificultad.setter
    def dificultad(self, valor):
        self.__dificultad = valor

    def __repr__(self):
        return f"Fabrica(vidas={self.vidas}, tiempo={self.tiempo}, dificultad={self.dificultad}"

    # def start(self, POSICIONES_PAQUETES_CINTA, NUM_CINTAS):
    # MOVIDO A __init__()

    # Bucle principal del juego, controlado por la fábrica
    def run(self):
        # if pyxel.frame_count % 60 == 0:
        #     print("Running...")
        self.luigi.mover()
        self.mario.mover()

        # Mueve los paquetes
        if pyxel.frame_count % 30 == 0:
            self.paquetes.actualizarPaquetes()

        # self.paquetes.matrizPaquetes[3][2] = 1
        # Añade los paquetes
        # if pyxel.frame_count % random.randint(20, 60):
        #     self.paquetes.anadirPaquete()

    def draw(self):
        # Muestra los personajes
        self.luigi.draw()
        self.mario.draw()

        # Muestra las cintas y los paquetes
        self.paquetes.draw()

        # Dibujamos el banco
        banco = 0
        # pyxel.blt(x:int, y:int, banco:int, u:int, v:int, w:int, h:int)
        # x, y, w, h: Variables del banco
        # pyxel.blt(5, 5, banco, 0, 0, 256, 256)
