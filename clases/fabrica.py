import pyxel

from clases.personaje import Personaje
from clases.paquetes import Paquetes
from clases.camion import Camion

class Fabrica:
    def __init__(self, tiempo, vidas):
        self.vidas = vidas # Cambian en función de la dificultad
        self.tiempo = tiempo # tiempo del nivel
        # self.dificultad = dificultad # 3 tipos

        self.personajes = []

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

    def start(self, POSICIONES_PAQUETES_CINTA, NUM_CINTAS):
        controlesMario = (pyxel.KEY_UP, pyxel.KEY_DOWN)
        controlesLuigi = (pyxel.KEY_W, pyxel.KEY_S)
        mario = Personaje("mario", controlesMario, 500, 300)
        luigi = Personaje("luigi", controlesLuigi, 100, 300)
        self.personajes = [mario, luigi]
        print(repr(mario), repr(luigi))

        camion = Camion(20, 30)
        print(repr(camion))
        paquetes = Paquetes(POSICIONES_PAQUETES_CINTA, NUM_CINTAS)
        print(repr(paquetes), "\n")
        # Añade un paquete en la posición inicial
        paquetes.anadirPaquete()
        paquetes.actualizarPaquetes()

    # Bucle principal del juego, controlado por la fábrica
    def run(self):
        # if pyxel.frame_count % 60 == 0:
        #     print("Running...")
        for personaje in self.personajes:
            personaje.mover()

    def draw(self, WIDTH, HEIGHT):
        # DEBUG: Sustituir por el banco de imagenes
        # pyxel.rectb(5, 5, WIDTH - 5 * 2, HEIGHT - 5 * 2, 1)
        pyxel.text(5, 5, f"WIDTH: {WIDTH}, HEIGHT: {HEIGHT}", 1)
        # Dibujamos el banco
        banco = 0
        # pyxel.blt(x:int, y:int, banco:int, u:int, v:int, w:int, h:int)
        # x, y, w, h: Variables del banco
        # MUESTRA A MARIO
        marioX, marioY = 100, 100
        pyxel.blt(5, 5, banco, 16, 16, marioX, marioY, scale=2)

        # Muestra los personajes
        for personaje in self.personajes:
            personaje.draw()
