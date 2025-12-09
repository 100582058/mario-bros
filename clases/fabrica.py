import pyxel
import time

from clases.mario import Mario
from clases.luigi import Luigi
from clases.paquetes import Paquetes
from clases.camion import Camion
from clases.pantallaInicio import PantallaInicio

from utils.config import esCintaPar, COLORES, WIDTH, HEIGHT


class Fabrica:
    def __init__(self, config):
        # Ahora la fábrica tiene todos los datos de la configuración del nivel
        self.config = config
        
        self.fallos = 0
        self.compFallos = 0
        self.compMute = 1
        self.colorMute = COLORES["gris"]
        self.pausa = False
        self.maxFallos = 30 # DEBUG
        self.activa = True

        self.__repartosHastaElimFallo = config.eliminaFallos

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
        yInicial = 25  # Indica la altura máxima a la que llegarían los personajes
        ancho, alto = 10, 11
        yPersonajes = yInicial - alto + self.config.altoCinta - 2
        self.luigi = Luigi(
            "L", 45, yPersonajes, ancho, alto, COLORES["azulCeleste"], self.config.controlesLuigi, self.config)
        self.mario = Mario(
            "M", 205, yPersonajes, ancho, alto, COLORES["magenta"], self.config.controlesMario, self.config)

        anchoCamion = (self.config.anchoPaq + 1) * 4
        self.camion = Camion(10, 30, anchoCamion - 2, 5, COLORES["marron"], self.config)

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

        # Comprueba si ha perdido la partida
        if self.fallos >= self.maxFallos:
            self.activa = False
            self.pausa = True
            self.draw()

        # Elimina un fallo si se hacen 'repartosHastaElimFallo' repartos
        if self.camion.numRepartos == self.__repartosHastaElimFallo and self.fallos >= 1:
            if self.compFallos+1 > self.fallos:
                self.compFallos -= 1
                pyxel.play(3, 17)
            self.fallos -= 1
            self.camion.numRepartos = 0


    def moverPaquetes(self):
        # Actualizamos las cintas pares e impares por su cuenta
        velocidadInicial = 4
        velPar = velocidadInicial / self.config.velCintasPares
        velImpar = velocidadInicial / self.config.velCintasImpares
        vel0 = velocidadInicial / self.config.velCinta0
        # REFACTOR: En que posición va?

        if pyxel.frame_count % int(velPar) == 0:
            # self.checkFallo()
            self.paquetes.actualizarPaquetes("pares")
        if pyxel.frame_count % int(velImpar) == 0:
            # self.checkFallo()
            self.paquetes.actualizarPaquetes("impares")

        if pyxel.frame_count % int(vel0) == 0:
            # self.checkFallo()
            self.paquetes.actualizarLista0()

        self.checkFallo()


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
        # -3 para ajustarlo
        self.tiempoSigPaq = (intervalo - (ahora - self.ultimoSpawn)) - 3

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
        if not self.activa:
            pyxel.cls(COLORES["negro"])
            tiempo = int(time.time() - self.tiempoInicial)
            tiempoMins = tiempo // 60
            tiempoSegs = int(tiempo - tiempoMins * 60)
            txtFin = f"------ GAME OVER ------\n\nDIFICULTAD JUGADA: {self.config.dificultad.upper()}\n\nPUNTOS CONSEGUIDOS: {self.puntos}\n\nTIEMPO JUGADO: {tiempoMins:02.0f}:{tiempoSegs:02.0f}"
            pyxel.text(80, 40, txtFin, COLORES["magenta"])
            pyxel.stop()

        else:
            # Muestra las cintas y los paquetes
            self.paquetes.draw()

            # Muestra los personajes
            self.luigi.draw()
            self.mario.draw()

            # Muestra el camión
            self.camion.draw()



            # -- Muestra el texto superior con informacion
            tiempo = int(time.time() - self.tiempoInicial)
            tiempoMins = tiempo // 60
            tiempoSegs = int(tiempo - tiempoMins * 60)
            # pyxel.text(WIDTH - 20, 5, f"TIEMPO DE JUEGO: {tiempo}", COLORES["naranja"])
            x = -40  # Mover el conjunto en x
            y = -2  # Mover el conjunto en y
            z = -20  # Mover en x las letras menos mario bros
            w = 0  # Mover en x las letras

            pyxel.rect(x + 40, y+2, 253, 11, COLORES["negro"])
            # pyxel.rect(0, 119, 260, 11, COLORES["negro"]) #Le da inmersividad
            pyxel.text(x+z+220, y+w + 5, f"TIEMPO DE JUEGO: {tiempoMins:02.0f}:{tiempoSegs:02.0f}", COLORES["naranja"])


                    #f"TIEMPO DE JUEGO: {tiempoMins:02.0f}:{tiempoSegs:02.0f}", COLORES["naranja"])

            # Muesta los puntos

            pyxel.text(x+z+120, y+w + 5,
                    f"PUNTOS: {self.puntos}", COLORES["amarillo"])

            pyxel.text(x + 49, y + w + 5, f"MARIO BROS", COLORES["blanco"])
            # Muestra los fallos
            pyxel.text(x + z + 170, y+w + 5,
                    f"FALLOS: {self.fallos}", COLORES["magenta"])
            #Muestra como mutear
            if pyxel.btnp(pyxel.KEY_M):
                self.compMute += 1
            if self.compMute % 2 == 0:
                self.colorMute = COLORES["azul"]
                pyxel.rect(x + 254, y + w + 14, 37, 12, COLORES["azul"])
            else:
                self.colorMute = COLORES["gris"]


            pyxel.rect(x + 255 , y + w + 15, 35, 10, COLORES["negro"])
            pyxel.text(x + 259, y + w + 17, f"MUTE: M", self.colorMute)

            # Muesta el tiempo para el siguiente paquete
            # pyxel.text(x+z+ 145,y+w+ 5, f"PAQUETE EN: {int(self.tiempoSigPaq)}", COLORES["azul"])
            # Contador en lista0
            #pyxel.text(252, 99, f"{int(self.tiempoSigPaq)}", COLORES["azul"])

    # Función para ver si se cae un paquete
    # Cuando paquete en el final de las filas pares y no está Luigi, eliminar el paquete. Lo mismo para Mario
    def checkFallo(self):
        # print("-"*10, "FALLO", "-"*10)
        x = self.paquetes.longitudX - 1
        # Comprueba si se cae un paquete en las filas intermedias
        for y in range(1, self.numCintas):
            # REFACTOR: --> Parece que ya está mejor?  Fernando dice que son muchos condicionales y se lee mal
            # QUIZÁS: self.paquetes.paqueteEn(x, y) and cintaIzda() and not self.luigi.enPlanta(y)
            if self.paquetes.matriz[y][0] != 0 and esCintaPar(y, self.numCintas):
                if not self.luigi.estaEnPiso(y):  # luigi es el de la izda
                    # print(self.paquetes)
                    print("Luigi falla", x, y)
                    self.anadirFalloYElimPaq(0, y)
                    # print(self.paquetes)
                    self.luigi.reganar()
                else:
                    self.puntos += 1
            # if (paquete en el borde dcho) Y (cinta impar) Y (mario no está en esa planta)
            if self.paquetes.matriz[y][x] != 0 and not esCintaPar(y, self.numCintas):
                if not self.mario.estaEnPiso(y):
                    # print(self.paquetes)
                    print("Mario falla",  x, y)
                    self.anadirFalloYElimPaq(x, y)
                    # print(self.paquetes)
                    self.mario.reganar()
                else:
                    self.puntos += 1

        # Comprueba que esté Luigi en la cinta del camión
        if self.paquetes.matriz[0][0] != 0:
            if self.luigi.estaEnPiso(0):
                self.camion.carga += 1
                self.puntos += 1
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
                self.anadirFalloYElimPaq(0, 0)
        # Comprueba si hay un paquete en la lista0 listo para ser añadido a la matriz
        if self.paquetes.lista0[0] != 0:
            if not self.mario.estaEnPiso(self.numCintas - 1):
                # Añadimos un fallo y eliminamos el paquete
                self.anadirFalloYElimPaq(0)
                self.mario.reganar()
                print("Mario falla lista 0")
            else:
                # Añadimos el paquete a la matriz
                self.paquetes.matriz[-1][-1] = 1
                self.puntos += 1
            self.paquetes.lista0[0] = 0

    def anadirFalloYElimPaq(self, x=None, y=None):
        self.pausa = True
        self.fallos += 1
        self.tiempoPausado = time.time()
        # Eliminamos el paquete de la matriz
        if x != None and y != None:
            self.paquetes.matriz[y][x] = 0
            self.paquetes.animar(x, y)
        else:
            # Eliminamos el paquete de la lista 0
            self.paquetes.lista0[x] = 0
            self.paquetes.animar(x)
        # Eliminamos los paquetes cerca de los jugadores al fallar
        self.paquetes.eliminPaquetesBorde()
