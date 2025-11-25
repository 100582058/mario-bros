import pyxel
import random
import time

from clases.personaje import Personaje
from clases.paquetes import Paquetes
from clases.camion import Camion

from utils.config import tiempoInicial

class Fabrica:
    def __init__(self, tiempo, vidas, POS_PAQ_CIN, NUM_CINTAS):
        self.fallos = 2 # Cambian en función de la dificultad. DEBUG: Vidas o fallos?
        self.tiempo = tiempo # tiempo del nivel
        # self.dificultad = dificultad # 3 tipos
        # DEBUG: En __init__() ???
        # Inicializamos los personajes
        controlesMario = (pyxel.KEY_UP, pyxel.KEY_DOWN)
        controlesLuigi = (pyxel.KEY_W, pyxel.KEY_S)
        self.luigi = Personaje("luigi", controlesLuigi, 100, 200)
        self.mario = Personaje("mario", controlesMario, 400, 200)

        self.camion = Camion(20, 30)
        self.paquetes = Paquetes(POS_PAQ_CIN, NUM_CINTAS)
        # Añade un paquete en la posición inicial
        self.paquetes.anadirPaqInicio()

    @property
    def fallos(self):
        return self.__vidas

    @fallos.setter
    def fallos(self, valor):
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
        return f"Fabrica(vidas={self.fallos}, tiempo={self.tiempo}, dificultad={self.dificultad}"

    # def start(self, POSICIONES_PAQUETES_CINTA, NUM_CINTAS):
    # MOVIDO A __init__()

    # Bucle principal del juego, controlado por la fábrica
    def run(self):
        # if pyxel.frame_count % 60 == 0:
        #     print("Running...")
        self.luigi.mover()
        self.mario.mover()

        # Mueve los paquetes
        if pyxel.frame_count % 15 == 0:
            self.paquetes.actualizarPaquetes()

        # Añade los paquetes
        if pyxel.frame_count % random.randint(120, 240) == 0:
            # print("NUEVO PAQUETE")
            self.paquetes.anadirPaqInicio()

    def draw(self, WIDTH, HEIGHT):
        # Muestra los personajes
        self.luigi.draw()
        self.mario.draw()

        # Muestra las cintas y los paquetes
        self.paquetes.draw()

        # Muestra los fallos y tiempo
        t = time.time()
        tiempo = int((t - tiempoInicial) / 1)
        pyxel.text(WIDTH - 20, 15, str(tiempo), 10)
        txt = "FALLOS: "
        txt += "X " * self.fallos
        pyxel.text(WIDTH - 100, 15, txt, 0)

    # Vidas
    # Dibujamos el banco
    # banco = 0
    # pyxel.blt(x:int, y:int, banco:int, u:int, v:int, w:int, h:int)
    # x, y, w, h: Variables del banco
    # pyxel.blt(5, 5, banco, 0, 0, 256, 256)
