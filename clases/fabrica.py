import pyxel
import random
import time

from clases.personaje import Personaje
from clases.paquetes import Paquetes
from clases.camion import Camion

from utils.config import TIEMPO, NUM_CINTAS, SEP_ENTRE_CINTAS, cintaPar, COLORES

class Fabrica:
    def __init__(self, vidas, POS_PAQ_CIN, NUM_CINTAS):
        self.fallos = 0
        self.pausa = False
        # Cambian en función de la dificultad. DEBUG: Vidas o fallos?
        self.maxFallos = vidas
        self.puntos = 0
        self.tiempoInicial = TIEMPO # tiempo del nivel
        # Guarda el momento en el que se para el tiempo en un fallo. Lo inicializamos a 'TIEMPO'
        self.tiempoPausado = TIEMPO
        self.ultimoSpawn = time.time()
        self.intervalos = [2]  # 7 segundos desde el spawn del ultimo paquete #Con 7 buena experiencia
        # Se le pueden poner especies de oleadas cambiando y añadiendo valores en la lista (cuando la lista se acaba se repite)
        self.indiceIntervalo = 0
        # self.dificultad = dificultad # 3 tipos
        # DEBUG: En __init__() ???

        # Inicializamos los personajes
        controlesMario = (pyxel.KEY_UP, pyxel.KEY_DOWN)
        controlesLuigi = (pyxel.KEY_W, pyxel.KEY_S)
        self.luigi = Personaje("luigi", controlesLuigi, 45, 100, COLORES["verde"])
        self.mario = Personaje("mario", controlesMario, 205, 100, COLORES["magenta"])

        self.camion = Camion(10, 30,  30, 5, COLORES["marron"])
        # self.paquetes = Paquetes(60, 25, COLORES["naranja"], 140, POS_PAQ_CIN, NUM_CINTAS)
        # self.paquetes = Paquetes(60, 25, 7,4, COLORES["naranja"], POS_PAQ_CIN, NUM_CINTAS)
        # (self, inicioX, inicioY, anchoPaq, altoPaq, color, anchoCinta, altoCinta, longitudX, longitudY, SEP_ENTRE_CINTAS)
        anchoCinta, altoCinta = 140, 4
        self.paquetes = Paquetes(60, 25, 7,4, COLORES["rosa"], anchoCinta, altoCinta, POS_PAQ_CIN, NUM_CINTAS, SEP_ENTRE_CINTAS)
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

    # Bucle principal del juego
    def juegoRun(self):
        # Mueve todos los objetos (menos los paquetes)
        self.run()
        if not self.pausa:
            # Se mueven los paquetes si el juego no está en pausa
            self.moverPaquetes()
        else:
            # Esperar 't' segundos hasta volver a reanudar el juego
            t = 2
            tiempoActual = time.time()
            tiempoPausado = tiempoActual - self.tiempoPausado
            if tiempoPausado > t:
                self.pausa = False

    def run(self):
        # Permite mover a los personajes con las teclas
        self.luigi.mover()
        self.mario.mover()

        # Mover el camión con los paquetes (si está lleno)
        self.camion.mover_y_descargar()

    def moverPaquetes(self):
        if pyxel.frame_count % 4 == 0:
            self.checkFallo()
            self.paquetes.actualizarPaquetes()

        # tiempo actual
        ahora = time.time() #tiempo actual, empezado a contar desde que se ejecuta
        intervalo = self.intervalos[self.indiceIntervalo]
        # ¿Ha pasado el tiempo necesario?
        if ahora - self.ultimoSpawn >= intervalo:
            self.paquetes.anadirPaqInicio()

            # reinicia el temporizador
            self.ultimoSpawn = ahora
            # pasar al siguiente intervalo
            self.indiceIntervalo += 1
            if self.indiceIntervalo == len(self.intervalos):
                self.indiceIntervalo = 0

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
        pyxel.text(WIDTH - 20, 5, str(tiempo), COLORES["naranja"])

        # Muestra los fallos
        pyxel.text(WIDTH - 110, 5, f"FALLOS: {self.fallos}", COLORES["amarillo"])

        # Muesta los puntos
        pyxel.text(60, 5, f"PUNTOS: {self.puntos}", COLORES["amarillo"])

    def anadirFallo(self):
        self.pausa = True
        self.fallos += 1
        self.tiempoPausado = time.time()

    # Función para ver si se cae un paquete
    # Cuando paquete en el final de las filas pares y no está Luigi, eliminar el paquete. Lo mismo para Mario
    def checkFallo(self):
        x = self.paquetes.longitudX
        for y in range(NUM_CINTAS):
            if y != 0:
                # Comprueba si se cae un paquete en las filas intermedias
                # REFACTOR: Fernando dice que son muchos condicionales y se lee mal
                # QUIZÁS: self.paquetes.paqueteEn(x, y) and cintaIzda() and not self.luigi.enPlanta(y)
                if self.paquetes.matriz[y][0] == 1 and cintaPar(y):
                    if self.luigi.planta != y:  # luigi es el de la izq
                        # pausar juego
                        self.anadirFallo()
                        self.paquetes.matriz[y][0] = 0
                    else:
                        self.puntos += 1
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
                            self.camion.carga += 1
                            # Controla cuando se llena el camión para pausar el juego
                            if self.camion.carga >= 8:
                                self.pausa = True
                                self.tiempoPausado = time.time()
                                self.puntos += 10
                            # Eliminamos el paquete de la cinta
                            self.paquetes.matriz[0][0] = 0
                    else:
                        self.anadirFallo()
