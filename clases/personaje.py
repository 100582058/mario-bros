import pyxel
import time

from utils.config import COLORES
from clases.elemento import Elemento
from utils.funciones import dibujar


class Personaje(Elemento):
    def __init__(self, id_personaje, posX, posY, ancho, alto, color, controles, config):
        # Movemos el personaje hasta la cinta 0
        y = posY + config.sepEntreCintas * (config.numCintas - 1)

        super().__init__(posX, y, ancho, alto, color)

        self.id = id_personaje  # Nombre del Personaje
        self.controles = controles  # Tupla con 2 strings para las teclas
        self.planta = config.numCintas - 1  # Planta en la que se encuentras

        self.__timerUp = 0  # Son temporizadores para la repetición del movimiento con btn
        self.__timerDown = 0
        # El numero de fps al que baja si matienes presionado (por debajo de 3 el jugador pierde precisión)(5 está bien)
        self.__comparador = 4

        # Controlan la animación del jefe regañándoles
        self.___estaSiendoReganado = False
        # Le regaña durante self.tiempoMaxReganado segundos
        self.__tiempoReganado = 0
        self.__totalAnimacion = config.pausaFallo
        self.__tiempoVisible = 0.15
        self.__tiempoInvisible = 0.1

        # Atributos de la configuración del nivel
        self.__sepEntreCintas = config.sepEntreCintas
        self.__numCintas = config.numCintas

    # --- PROPERTIES Y SETTERS ---
    @property
    def controles(self):
        return self.__controles

    @controles.setter
    def controles(self, valor):
        if isinstance(valor, tuple) and len(valor) == 2:
            self.__controles = valor
        else:
            raise TypeError("Controles no válidos")

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

    # --- MÉTODOS DE LA CLASE ---

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

    def estaEnPiso(self, piso):
        return self.planta == piso

    def reganar(self):
        self.___estaSiendoReganado = True
        # Guarda el tiempo en el que se empieza a regañar
        self.__tiempoReganado = time.time()

    def draw(self):
        # Dibujamos las plataformas del jefe
        anchoPlataforma, altoPlataforma = 26, 3
        if self.id == "M":
            x = 225
            y = 75
            pyxel.rect(x, y, anchoPlataforma, altoPlataforma, COLORES["marron"])
            pyxel.rect(x + 2, y, anchoPlataforma - 4, altoPlataforma - 1, COLORES["verde"])
        elif self.id == "L":
            x = 7
            y = 115
            pyxel.rect(x, y, anchoPlataforma, altoPlataforma, COLORES["marron"])
            pyxel.rect(x + 2, y, anchoPlataforma - 4, altoPlataforma - 1, COLORES["verde"])


        if not self.___estaSiendoReganado:
            pyxel.rect(self.posX, self.posY, self.ancho, self.alto, self.color)
            pyxel.text(self.posX + self.ancho / 4, self.posY + self.alto / 4, self.id, COLORES["blanco"])
        else:
            # Pintamos al personaje en otro sitio y añadimos al jefe
            posX = x + anchoPlataforma - self.ancho
            self.__animarJefe(posX, y)

            # Pintamos al personaje
            pyxel.rect(posX, y - self.alto, self.ancho, self.alto, self.color)
            pyxel.text(posX + self.ancho / 4, y + self.alto / 4 - self.alto, self.id, COLORES["blanco"])

            delta_t = time.time() - self.__tiempoReganado
            if delta_t >= self.__totalAnimacion:
                self.___estaSiendoReganado = False

    def __animarJefe(self, posX, y):
        tiempoTranscurrido = time.time() - self.__tiempoReganado
        if tiempoTranscurrido < self.__totalAnimacion:
            t = tiempoTranscurrido % (self.__tiempoInvisible + self.__tiempoVisible)
            if t < self.__tiempoVisible:
                # Pintamos al jefe
                anchoJefe = self.ancho * 1.2
                pyxel.rect(posX - anchoJefe - 5, y - self.alto * 1.2,
                        anchoJefe, self.alto * 1.2, COLORES["negro"])