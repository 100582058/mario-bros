import pyxel
import random
import time

from clases.personaje import Personaje
from clases.paquetes import Paquetes
from clases.camion import Camion

from utils.config import TIEMPO, NUM_CINTAS, SEP_ENTRE_CINTAS, NUM_PAQ_CIN, NUM_CINTAS, VIDAS, cintaPar, COLORES

class Fabrica:
    def __init__(self):
        self.fallos = 0
        self.pausa = False
        # Cambian en función de la dificultad. DEBUG: Vidas o fallos?
        self.maxFallos = VIDAS
        self.puntos = 0
        self.tiempoInicial = TIEMPO # tiempo del nivel
        # Guarda el momento en el que se para el tiempo en un fallo. Lo inicializamos a 'TIEMPO'
        self.tiempoPausado = TIEMPO
        self.ultimoSpawn = time.time()
        self.intervalos = [7, 10, 13, 22]  # 7 segundos desde el spawn del ultimo paquete #Con 7 buena experiencia
        # Se le pueden poner especies de oleadas cambiando y añadiendo valores en la lista (cuando la lista se acaba se repite)
        self.indiceIntervalo = 0
        # self.dificultad = dificultad # 3 tipos
        self.tiempoSigPaq = time.time()

        # Inicializamos todos los objetos del juego
        self.crearJuego()

    def crearJuego(self):
        controlesMario = (pyxel.KEY_UP, pyxel.KEY_DOWN)
        controlesLuigi = (pyxel.KEY_W, pyxel.KEY_S)
        self.luigi = Personaje("luigi", controlesLuigi, 45, 99, COLORES["verde"])
        self.mario = Personaje("mario", controlesMario, 205, 99, COLORES["magenta"])

        self.camion = Camion(10, 30,  30, 5, COLORES["marron"])
        anchoCinta, altoCinta = 140, 4
        self.paquetes = Paquetes(
            60,
            25,
            7,
            4,
            COLORES["rosa"],
            anchoCinta,
            altoCinta,
            NUM_PAQ_CIN,
            NUM_CINTAS,
            SEP_ENTRE_CINTAS,
        )
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
        print("ahora", ahora)
        # Da el valor al contador regresivo de segundos para paquete
        self.tiempoSigPaq = intervalo - (ahora - self.ultimoSpawn) # + 1 #Va un poco mal, igual necesita el +1

        if ahora - self.ultimoSpawn >= intervalo:
            print("resta", ahora - self.ultimoSpawn)
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

        # Muesta los puntos
        pyxel.text(60, 5, f"PUNTOS: {self.puntos}", COLORES["amarillo"])

        # Muesta el tiempo para el siguiente paquete
        pyxel.text(150, 5, f"PAQUETE EN: {int(self.tiempoSigPaq)}", COLORES["azul"])

        # Muestra los fallos

        pyxel.text(105, 5, f"FALLOS: {self.fallos}", COLORES["magenta"])

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
                # REFACTOR: --> Parece que ya está mejor?  Fernando dice que son muchos condicionales y se lee mal
                # QUIZÁS: self.paquetes.paqueteEn(x, y) and cintaIzda() and not self.luigi.enPlanta(y)
                if self.paquetes.matriz[y][0] == 1 and cintaPar(y):
                    if self.luigi.planta != y:  # luigi es el de la izq
                        # Pausar juego
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
                            self.tiempoPausado = time.time()
                            self.pausa = True
                            self.puntos += 10
                        # Eliminamos el paquete de la cinta
                        self.paquetes.matriz[0][0] = 0
                    else:
                        self.anadirFallo()
                # Comprueba si hay un paquete en la lista0 listo para ser añadido a la matriz
                if self.paquetes.lista0[0] == 1:
                    if self.mario.planta != NUM_CINTAS - 1:
                        # Añadimos un fallo
                        self.anadirFallo()
                    else:
                        # Añadimos el paquete a la matriz
                        self.paquetes.matriz[-1][-1] = 1
                        self.puntos += 1
                    self.paquetes.lista0[0] = 0
