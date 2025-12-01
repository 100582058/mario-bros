import pyxel
import random
import time

from clases.personaje import Personaje
from clases.paquetes import Paquetes
from clases.camion import Camion

from utils.config import TIEMPO, NUM_CINTAS, cintaPar, COLORES

class Fabrica:
    def __init__(self, vidas, POS_PAQ_CIN, NUM_CINTAS):
        self.fallos = 0 
        # Cambian en función de la dificultad. DEBUG: Vidas o fallos?
        self.maxFallos = vidas
        self.puntos = 0
        self.tiempoInicial = TIEMPO # tiempo del nivel
        # self.dificultad = dificultad # 3 tipos
        # DEBUG: En __init__() ???

        # Inicializamos los personajes
        controlesMario = (pyxel.KEY_UP, pyxel.KEY_DOWN)
        controlesLuigi = (pyxel.KEY_W, pyxel.KEY_S)
        self.luigi = Personaje("luigi", controlesLuigi, 45, 100)
        self.mario = Personaje("mario", controlesMario, 205, 100)

        self.camion = Camion(10, 30)
        self.paquetes = Paquetes(POS_PAQ_CIN, NUM_CINTAS)
        # Añade un paquete en la posición inicial
        self.paquetes.anadirPaqInicio()

    @property
    def fallos(self):
        return self.__vidas

    @fallos.setter
    def fallos(self, valor):
        self.__vidas = valor

    # @property
    # def tiempoInicial(self):
    #     return self.__tiempoInicial

    # @tiempoInicial.setter
    # def tiempoInicial(self, valor):
    #     if isinstance(valor, int):
    #         self.__tiempoInicial = valor
    #     else:
    #         raise TypeError("El tiempo no es un entero")

    @property
    def dificultad(self):
        return self.__dificultad

    @dificultad.setter
    def dificultad(self, valor):
        self.__dificultad = valor

    def __repr__(self):
        return f"Fabrica(vidas={self.fallos}, tiempo={self.tiempoInicial}, dificultad={self.dificultad}"

    # Bucle principal del juego, controlado por la fábrica
    def run(self):
        # Permite mover a los personajes con las teclas
        self.luigi.mover()
        self.mario.mover()

        # Mueve los paquetes
        if pyxel.frame_count % 4 == 0:
            self.checkFallo()
            self.paquetes.actualizarPaquetes()

        # Añade los paquetes
        if pyxel.frame_count % random.randint(120, 240) == 0:
            self.paquetes.anadirPaqInicio()

        # Mover el camión con los paquetes, solo si se llama desde self.fallo()

    def draw(self, WIDTH, HEIGHT):
        # Muestra los personajes
        self.luigi.draw()
        self.mario.draw()

        # Muestra las cintas y los paquetes
        self.paquetes.draw()

        # Muestra el camión
        self.camion.draw()

        # Muestra el tiempo
        t = time.time()
        tiempo = int((t - self.tiempoInicial) / 1)
        pyxel.text(WIDTH - 20, 15, str(tiempo), 10)
        txt = "FALLOS: "
        txt += "X" * self.fallos
        pyxel.text(WIDTH - 100, 15, txt, 0)

    # Función para ver si se cae un paquete
    # matriz[y][x] = 0/1

    # Cuando paquete en el final de las filas pares y no está Luigi, eliminar el paquete. Lo mismo para Mario
    def checkFallo(self):
        x = self.paquetes.longitudX
        for y in range(NUM_CINTAS):
            # if (paquete en el borde izquierdo) Y (cinta par) Y (luigi no está en esa planta)
            # Plantas intermedias

            if y != 0:
                if (
                    self.paquetes.matriz[y][0] == 1 and cintaPar(y) and self.luigi.planta != y):  # luigi es el de la izq
                    # stop matriz paquetes (tenemos que ver como va)
                    # pausar juego
                    self.paquetes.matriz[y][0] = 0
                    self.fallos += 1
                # if (paquete en el borde dcho) Y (cinta impar) Y (mario no está en esa planta)
                elif self.paquetes.matriz[y][x -1] == 1 and not cintaPar(y):
                    if self.mario.planta != y:
                        self.paquetes.matriz[y][x - 1] = 0
                        self.anadirFallo()
                    else:
                        self.puntos += 1

                # Comprueba que esté Luigi en la cinta del camión
                if self.paquetes.matriz[0][0] == 1:
                    if self.luigi.planta == 0:
                            print("Paquete añadido al camión")
                            self.camion.carga += 1
                            # Controla cuando se llena el camión para pausar el juego
                            if self.camion.carga >= 8:
                                self.pausa = True
                                self.tiempoPausado = time.time()
                                self.puntos += 10
                    else:
                        self.anadirFallo()
