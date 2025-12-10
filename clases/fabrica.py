import pyxel
import time

from clases.mario import Mario
from clases.luigi import Luigi
from clases.paquetes import Paquetes
from clases.camion import Camion

from utils.config import esCintaPar, COLORES, WIDTH, HEIGHT


class Fabrica:
    def __init__(self, config):
        # Ahora la fábrica tiene todos los datos de la configuración del nivel
        self.config = config
        
        self.fallos = 0
        self.compFallos = 0
        self.pausa = False
        self.maxFallos = 30 # DEBUG
        self.activa = True

        self.__compMute = 1
        self.__colorMute = COLORES["gris"]

        self.__repartosHastaElimFallo = config.eliminaFallos

        self.puntos = 0
        self.puntosComp = 0

        self.tiempoInicial = time.time()
        # Guarda el momento en el que se para el tiempo en un fallo. Lo inicializamos a 'TIEMPO'
        self.tiempoPausado = time.time()

        self.ultimoSpawn = time.time()
        # Lista que especifica cuantos segundos hasta el spawn del proximo paquete
        self.intervalos = [8, 8, 12, 8, 12, 10]
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
        self.paquetes.lista0[10] = 1

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
        self.__run()
        if not self.pausa:
            # Se mueven los paquetes si el juego no está en pausa
            self.__moverPaquetes()
            self.__anadirPaquetes()
            self.paquetes.comprobarMinPaquetes(self.puntos)
        else:
            # Esperar (5 + 1) segundos hasta volver a reanudar el juego
            tiempoActual = time.time()
            tiempoPausado = tiempoActual - self.tiempoPausado
            if tiempoPausado > self.config.pausaFallo + 1:
                self.pausa = False

    def __run(self):
        # Permite mover a los personajes con las teclas
        self.luigi.mover()
        self.mario.mover()
        
        self.__comprobarRepartosCamion()

        # Mover el camión con los paquetes (si está lleno)
        self.camion.mover_y_descargar()

        # Comprueba si ha perdido la partida
        if self.fallos >= self.maxFallos:
            self.activa = False
            self.pausa = True
            self.draw()


    def __comprobarRepartosCamion(self):
        # Elimina un fallo si se hacen 'repartosHastaElimFallo' repartos
        if self.camion.numRepartos >= self.__repartosHastaElimFallo and self.fallos >= 1:
            print("Fallo eliminado", self.camion.numRepartos, self.fallos, self.__repartosHastaElimFallo)
            self.fallos -= 1
            # Reproducir el sonido de sumar una vida
            pyxel.play(1, 17)
            self.camion.numRepartos = 0

    def __reproducirFallo(self):
        pyxel.play(3, 25)

    def __moverPaquetes(self):
        # Actualizamos las cintas pares e impares por su cuenta
        velocidadInicial = 3
        velPar = velocidadInicial / self.config.velCintasPares
        velImpar = velocidadInicial / self.config.velCintasImpares
        vel0 = velocidadInicial / self.config.velCinta0

        if pyxel.frame_count % int(velPar) == 0:
            self.__checkFalloPares()
            self.paquetes.actualizarPaquetes("pares")
            
        if pyxel.frame_count % int(velImpar) == 0:
            self.__checkFalloImpares()
            self.paquetes.actualizarPaquetes("impares")

        if pyxel.frame_count % int(vel0) == 0:
            self.__checkFalloCinta0()
            self.paquetes.actualizarLista0()

    def __anadirPaquetes(self):
        ahora = time.time()  # tiempo actual, empezado a contar desde que se ejecuta
        intervalo = self.intervalos[self.indiceIntervalo]
        # print("ahora", ahora)
        # Da el valor al contador regresivo de segundos para paquete
        # + 1 #Va un poco mal, igual necesita el +1
        # -3 para ajustarlo
        self.tiempoSigPaq = (intervalo - (ahora - self.ultimoSpawn)) - 3

        if ahora - self.ultimoSpawn >= intervalo:
            self.paquetes.anadirPaqInicio()

            # reinicia el temporizador
            self.ultimoSpawn = ahora
            # pasar al siguiente intervalo
            self.indiceIntervalo += 1
            if self.indiceIntervalo == len(self.intervalos):
                self.indiceIntervalo = 0

    # Suma puntos y reproduce el sonido
    def __anadirPuntos(self, ptos):
        self.puntos += ptos
        pyxel.play(2, 16)

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

            # -- Muestra el texto superior con informacion --
            tiempo = int(time.time() - self.tiempoInicial)
            tiempoMins = tiempo // 60
            tiempoSegs = int(tiempo - tiempoMins * 60)
            x = -40  # Mover el conjunto en x
            y = -2  # Mover el conjunto en y
            z = -20  # Mover en x las letras menos mario bros
            w = 0  # Mover en x las letras

            pyxel.rect(x + 40, y+2, 253, 11, COLORES["negro"])
            # pyxel.rect(0, 119, 260, 11, COLORES["negro"]) #Le da inmersividad
            pyxel.text(x+z+220, y+w + 5, f"TIEMPO DE JUEGO: {tiempoMins:02.0f}:{tiempoSegs:02.0f}", COLORES["naranja"])

            # Muesta los puntos

            pyxel.text(x+z+120, y+w + 5,
                    f"PUNTOS: {self.puntos}", COLORES["amarillo"])

            pyxel.text(x + 49, y + w + 5, f"MARIO BROS", COLORES["blanco"])
            # Muestra los fallos
            pyxel.text(x + z + 170, y+w + 5,
                    f"FALLOS: {self.fallos}", COLORES["magenta"])
            #Muestra como mutear
            #soporte
            pyxel.rect(213, 13, 41, 4, COLORES["marron"])
            pyxel.rect(215, 15, 37, 1, COLORES["gris"])
            pyxel.rect(212, 13, 2, 4, COLORES["gris"])
            if pyxel.btnp(pyxel.KEY_M):
                self.__compMute += 1
            if self.__compMute % 2 == 0:
                self.__colorMute = COLORES["azul"]
                pyxel.rect(x + 255, y + w + 16, 37, 12, COLORES["azul"])
            else:
                self.__colorMute = COLORES["gris"]


            pyxel.rect(x + 256 , y + w + 17, 35, 10, COLORES["negro"])
            pyxel.text(x + 260, y + w + 19, f"MUTE: M", self.__colorMute)

    # Funciones para detectar fallos en cada tipo de cintas
    # Borran el paquete, llamar a la animación de borrado, etc.
    # Y suman puntos si el personaje sí está en esa cinta
    def __checkFalloPares(self):
        x = self.paquetes.longitudX - 1
        for y in range(1, self.numCintas):
            if self.paquetes.matriz[y][0] != 0 and esCintaPar(y, self.numCintas):
                if not self.luigi.estaEnPiso(y):  # luigi es el de la izda
                    print("Luigi falla", x, y)
                    self.__anadirFalloYElimPaq(0, y)
                    self.luigi.reganar()
                else:
                    self.__anadirPuntos(1)

        # Comprueba que esté Luigi en la cinta del camión
        if self.paquetes.matriz[0][0] != 0:
            if self.luigi.estaEnPiso(0):
                self.camion.carga += 1
                self.__anadirPuntos(1)
                # Controla cuando se llena el camión para pausar el juego
                if self.camion.carga >= 8:
                    self.tiempoPausado = time.time()
                    self.pausa = True
                    self.__anadirPuntos(10)
                    # Eliminamos los paquetes al final de las cintas
                    self.paquetes.eliminPaquetesBorde()
                # Eliminamos el paquete de la cinta
                self.paquetes.matriz[0][0] = 0
            else:
                self.__anadirFalloYElimPaq(0, 0)
                self.luigi.reganar()

    def __checkFalloImpares(self):
        x = self.paquetes.longitudX - 1
        for y in range(1, self.numCintas):
            if self.paquetes.matriz[y][x] != 0 and not esCintaPar(y, self.numCintas):
                if not self.mario.estaEnPiso(y):
                    # print(self.paquetes)
                    print("Mario falla",  x, y)
                    self.__anadirFalloYElimPaq(x, y)
                    # print(self.paquetes)
                    self.mario.reganar()
                else:
                    self.__anadirPuntos(1)

    def __checkFalloCinta0(self):
        # Comprueba si hay un paquete en la lista0 listo para ser añadido a la matriz
        if self.paquetes.lista0[0] != 0:
            if not self.mario.estaEnPiso(self.numCintas - 1):
                # Añadimos un fallo y eliminamos el paquete
                self.__anadirFalloYElimPaq(0)
                self.mario.reganar()
                print("Mario falla lista 0")
            else:
                # Añadimos el paquete a la matriz
                self.paquetes.matriz[-1][-1] = 1
                self.__anadirPuntos(1)
            self.paquetes.lista0[0] = 0

    # Se encarga de añadir los fallos. Llamada desde checkFallo____
    def __anadirFalloYElimPaq(self, x=None, y=None):
        self.pausa = True
        # Añade un fallo y reproduce el sonido
        self.fallos += 1
        self.__reproducirFallo()

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
