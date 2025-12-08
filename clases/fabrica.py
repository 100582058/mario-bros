import pyxel
import time

from clases.mario import Mario
from clases.luigi import Luigi
from clases.paquetes import Paquetes
from clases.camion import Camion

from utils.config import esCintaPar, COLORES


class Fabrica:
    def __init__(self, config):
        # Ahora la fábrica tiene todos los datos de la configuración del nivel
        self.config = config
        self.fallos = 0
        self.compFallos = 0
        self.pausa = False
        # Cambian en función de la dificultad. DEBUG: Vidas o fallos?
        self.maxFallos = 3
        self.puntos = 0
        self.puntosComp = 0

        self.tiempoInicial = time.time()
        # Guarda el momento en el que se para el tiempo en un fallo. Lo inicializamos a 'TIEMPO'
        self.tiempoPausado = time.time()

        self.ultimoSpawn = time.time()
        # 7 segundos desde el spawn del ultimo paquete
        self.intervalos = [4]
        # Se le pueden poner especies de oleadas cambiando y añadiendo valores en la lista (cuando la lista se acaba se repite)
        self.indiceIntervalo = 0
        # self.dificultad = dificultad # 3 tipos
        self.tiempoSigPaq = time.time()

        # Atributos de la configuración del nivel
        self.numCintas = self.config.numCintas

        self.crearJuego()

    def crearJuego(self):
        # Pasamos el objeto ConfigNivel a los objetos
        # para que extraigan la información necesaria de la configuración
        yInicial = 25 # Indica la altura máxima a la que llegarían los personajes
        ancho, alto = 10, 12
        yPersonajes = yInicial - alto + self.config.altoCinta
        self.luigi = Luigi(
            "L", 45, yPersonajes, ancho, alto, COLORES["azulCeleste"], self.config.controlesLuigi, self.config)
        self.mario = Mario(
            "M", 205, yPersonajes, ancho, alto, COLORES["magenta"], self.config.controlesMario, self.config)

        self.camion = Camion(10, 30,  30, 5, COLORES["marron"])

        self.paquetes = Paquetes(
            60,
            yInicial,
            self.config.anchoPaq,
            self.config.altoPaq,
            COLORES["azulMarino"],
            self.config.numPaqCinta,
            self.config.numCintas,
            self.config
        )

        # Añade un paquete al empezar
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
            # Esperar 't' segundos hasta volver a reanudar el juego REFACTOR: time.sleep(t)
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
        # Actualizamos las cintas pares e impares por su cuenta
        if pyxel.frame_count % 2 / self.config.velCintasPares == 0:
            self.checkFallo()
            self.paquetes.actualizarPaquetes("pares")
        if pyxel.frame_count % 2 / self.config.velCintasImpares == 0:
            self.checkFallo()
            self.paquetes.actualizarPaquetes("impares")

        if pyxel.frame_count % 20 / self.config.velCinta0 == 0:
            self.checkFallo()
            self.paquetes.actualizarLista0()

        # Sonido puntos (los reproducimos en el canal 2 para que no interfieran con la música)
        if self.puntosComp < self.puntos - 9:  # Puntos del camión
            self.puntosComp += 10
            pyxel.play(2, 16)
        elif self.puntosComp < self.puntos:
            self.puntosComp += 1
            pyxel.play(2, 16)

        # Sonido fallos (los reproducimos en el canal 3 para que no interfieran con la música)
        if self.compFallos < self.fallos:
            self.compFallos += 1
            pyxel.play(3, 25)

        ahora = time.time()  # tiempo actual, empezado a contar desde que se ejecuta
        intervalo = self.intervalos[self.indiceIntervalo]
        # print("ahora", ahora)
        # Da el valor al contador regresivo de segundos para paquete
        # + 1 #Va un poco mal, igual necesita el +1
        self.tiempoSigPaq = (intervalo - (ahora - self.ultimoSpawn)) -3 #-3 para ajustarlo

        if ahora - self.ultimoSpawn >= intervalo:
            # print("resta", ahora - self.ultimoSpawn)
            self.paquetes.anadirPaqInicio()

            # reinicia el temporizador
            self.ultimoSpawn = ahora
            # pasar al siguiente intervalo
            self.indiceIntervalo += 1
            if self.indiceIntervalo == len(self.intervalos):
                self.indiceIntervalo = 0

    def draw(self):
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
        tiempMin = 0

        tiempoMins = tiempo // 60
        tiempoSegs = int(tiempo - tiempoMins * 60)
        # pyxel.text(WIDTH - 20, 5, f"TIEMPO DE JUEGO: {tiempo}", COLORES["naranja"])
        x = -40  # Mover el conjunto en x
        y = -2  # Mover el conjunto en y
        z = -20  # Mover en x las letras menos mario bros
        w = 0  # Mover en x las letras

        pyxel.rect(x + 40, y+2, 260, 11, COLORES["negro"])
        # pyxel.rect(0, 119, 260, 11, COLORES["negro"]) #Le da inmersividad
        pyxel.text(x+z+220, y+w + 5,
                   f"TIEMPO DE JUEGO: {tiempoMins:02.0f}:{tiempoSegs:02.0f}", COLORES["naranja"])

        # Muesta los puntos

        pyxel.text(x+z+120, y+w + 5,
                   f"PUNTOS: {self.puntos}", COLORES["amarillo"])

        pyxel.text(x + 49, y + w + 5, f"MARIO BROS", COLORES["blanco"])
        # Muestra los fallos
        pyxel.text(x + z + 170, y+w + 5,
                   f"FALLOS: {self.fallos}", COLORES["magenta"])
        # Muesta el tiempo para el siguiente paquete
        # pyxel.text(x+z+ 145,y+w+ 5, f"PAQUETE EN: {int(self.tiempoSigPaq)}", COLORES["azul"])
        # Contador en lista0
        pyxel.text(252, 99, f"{int(self.tiempoSigPaq)}", COLORES["azul"])

    # Función para ver si se cae un paquete
    # Cuando paquete en el final de las filas pares y no está Luigi, eliminar el paquete. Lo mismo para Mario
    def checkFallo(self):
        x = self.paquetes.longitudX
        for y in range(self.numCintas):
            if y != 0:
                # Comprueba si se cae un paquete en las filas intermedias
                # REFACTOR: --> Parece que ya está mejor?  Fernando dice que son muchos condicionales y se lee mal
                # QUIZÁS: self.paquetes.paqueteEn(x, y) and cintaIzda() and not self.luigi.enPlanta(y)
                if self.paquetes.matriz[y][0] == 1 and esCintaPar(y, self.numCintas):
                    if self.luigi.planta != y:  # luigi es el de la izq
                        # Pausar juego
                        self.anadirFallo()
                        self.luigi.reganar()
                    else:
                        self.puntos += 1
                # if (paquete en el borde dcho) Y (cinta impar) Y (mario no está en esa planta)
                elif self.paquetes.matriz[y][x - 1] == 1 and not esCintaPar(y, self.numCintas):
                    if self.mario.planta != y:
                        self.anadirFallo()
                        self.mario.reganar()
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
                            # Eliminamos los paquetes al final de las cintas
                            self.paquetes.eliminPaquetesBorde()
                        # Eliminamos el paquete de la cinta
                        self.paquetes.matriz[0][0] = 0
                    else:
                        self.anadirFallo()
                # Comprueba si hay un paquete en la lista0 listo para ser añadido a la matriz
                if self.paquetes.lista0[0] == 1:
                    if self.mario.planta != self.numCintas - 1:
                        # Añadimos un fallo
                        self.anadirFallo()
                        self.mario.reganar()
                    else:
                        # Añadimos el paquete a la matriz
                        self.paquetes.matriz[-1][-1] = 1
                        self.puntos += 1
                    self.paquetes.lista0[0] = 0

    def anadirFallo(self):
        self.pausa = True
        self.fallos += 1
        self.tiempoPausado = time.time()
        # Eliminamos los paquetes cerca de los jugadores al fallar
        self.paquetes.eliminPaquetesBorde()
