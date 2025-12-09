import pyxel
import time

from utils.config import COLORES
from clases.elemento import Elemento
from utils.funciones import dibujar


class Personaje(Elemento):
    def __init__(self, id_personaje, posX, posY, ancho, alto, color, controles, config):
        y = posY
        # Movemos el personaje hasta la cinta 0
        y += config.sepEntreCintas * (config.numCintas - 1)

        super().__init__(posX, y, ancho, alto, color)

        self.id = id_personaje  # Nombre del Personaje
        self.controles = controles  # Tupla con 2 strings para las teclas
        self.planta = config.numCintas - 1  # Planta en la que se encuentras

        self.__timerUp = 0  # Son temporizadores para la repetición del movimiento con btn
        self.__timerDown = 0
        # El numero de fps al que baja si matienes presionado (por debajo de 3 el jugador pierde precisión)(5 está bien)
        self.__comparador = 4

        self.__estaReganado = False
        # Le regaña durante self.tiempoMaxReganado segundos
        self.__tiempoReganado = 0
        self.__tiempoMaxReganado = 1.2

        # Atributos de la configuración del nivel
        self.sepEntreCintas = config.sepEntreCintas
        self.numCintas = config.numCintas

    @property
    def controles(self):
        return self.__controles

    @controles.setter
    def controles(self, valor):
        self.__controles = valor

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        if isinstance(valor, str):
            self.__id = valor
        else:
            raise TypeError()

    @property
    def sepEntreCintas(self):
        return self.__sepEntreCintas

    @sepEntreCintas.setter
    def sepEntreCintas(self, valor):
        if isinstance(valor, int) or isinstance(valor, float):
            self.__sepEntreCintas = valor
        else:
            raise TypeError()

    @property
    def numCintas(self):
        return self.__numCintas

    @numCintas.setter
    def numCintas(self, valor):
        if isinstance(valor, int):
            self.__numCintas = valor
        else:
            raise TypeError()

    def intentarCambiarPlanta(self, direccion):
        # Se sobreescribe en los hijos (Luigi y Mario)
        return

    # Sube o baje 'mult' plantas
    def subir(self, mult=1):
        self.planta -= mult
        self.posY -= self.sepEntreCintas * mult

    def bajar(self, mult=1):
        self.planta += mult
        self.posY += self.sepEntreCintas * mult

    def mover(self):
        # self.controles[0] controla el movimiento de subida
        # self.controles[1] el de bajada
        if pyxel.btnp(self.controles[0]):
            self.intentarCambiarPlanta("arriba")
            self.__timerUp = 0  # Reset para evitar doble salto

        if pyxel.btnp(self.controles[1]):
            self.intentarCambiarPlanta("abajo")
            self.__timerDown = 0  # Reset para evitar doble salto

        # -- Mover varias plantas al mantener pulsado --
        # NOTA +(tengo que revisar que funcione)+(Me parece que podría funcionar incluso con solo 1 timer para simplificar)
        if pyxel.btn(self.controles[0]):
            self.__timerUp += 1
            if self.__timerUp > self.__comparador:
                self.intentarCambiarPlanta("arriba")
                # Es importante asignarlo fuera por si se encuentra en el extremo de la lista
                self.__timerUp = 0
        else:
            self.__timerUp = 0

        if pyxel.btn(self.controles[1]):
            self.__timerDown += 1
            if self.__timerDown > self.__comparador:
                self.intentarCambiarPlanta("abajo")
                # Es importante asignarlo fuera por si se encuentra en el extremo de la lista
                self.__timerDown = 0
        else:
            self.__timerDown = 0

    def estaEnPiso(self):
        pass

    def reganar(self):
        self.__estaReganado = True
        # Guarda el tiempo en el que se empieza a regañar
        self.__tiempoReganado = time.time()

    def draw(self):

        if not self.__estaReganado:
            pyxel.rect(self.posX, self.posY, self.ancho, self.alto, self.color)
            pyxel.text(self.posX + self.ancho / 4, self.posY + self.alto / 4, self.id, COLORES["blanco"])
        else:
            # Pintamos al personaje en otro sitio y añadimos al jefe
            if pyxel.frame_count % 16 >= 8:
                pyxel.rect(self.posX - self.ancho, self.posY - self.alto / 2,
                        self.ancho * 0.8, self.alto * 0.8, COLORES["negro"])
                # REFACTOR cambiar de lugar
                delta_t = time.time() - self.__tiempoReganado
                if delta_t >= self.__tiempoMaxReganado:
                    self.__estaReganado = False
