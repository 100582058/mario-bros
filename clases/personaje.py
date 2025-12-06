import pyxel
import time

from utils.config import COLORES
from clases.elemento import Elemento
from utils.funciones import dibujar

class Personaje(Elemento):
    def __init__(self, id_personaje, posX, posY, ancho, alto, color, controles, plantasPosibles, config):
        y = posY
        # Movemos el personaje hasta la cinta 0
        y += config.sepEntreCintas * (config.numCintas - 1)

        super().__init__(posX, y, ancho, alto, color)

        self.id = id_personaje  # Nombre del Personaje
        self.controles = controles  # Tupla con 2 strings para las teclas
        self.planta = config.numCintas - 1  # Planta en la que se encuentras
        self.plantasPosibles = plantasPosibles # "pares" o "impares"

        self.timerUp = 0       #Son temporizadores para la repetición del movimiento con btn
        self.timerDown = 0
        self.comparador = 4 #El numero de fps al que baja si matienes presionado (por debajo de 3 el jugador pierde precisión)(5 está bien)

        self.estaReganado = False
        # Le regaña durante self.tiempoMaxReganado segundos
        self.tiempoReganado = 0
        self.tiempoMaxReganado = 1.2

        # Atributos de la configuración del nivel
        self.sepEntreCintas = config.sepEntreCintas
        self.numCintas = config.numCintas

    @property
    def controles(self):
        return self.__controles

    @controles.setter
    def controles(self, valor):
        self.__controles = valor

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
            self.timerUp = 0  # Reset para evitar doble salto

        if pyxel.btnp(self.controles[1]):
            self.intentarCambiarPlanta("abajo")
            self.timerDown = 0 # Reset para evitar doble salto

        # -- Mover varias plantas al mantener pulsado --
        # NOTA +(tengo que revisar que funcione)+(Me parece que podría funcionar incluso con solo 1 timer para simplificar)
        if pyxel.btn(self.controles[0]):
            self.timerUp += 1
            if self.timerUp > self.comparador:
                self.intentarCambiarPlanta("arriba")
                self.timerUp = 0 # Es importante asignarlo fuera por si se encuentra en el extremo de la lista
        else:
            self.timerUp = 0

        if pyxel.btn(self.controles[1]):
            self.timerDown += 1
            if self.timerDown > self.comparador:
                self.intentarCambiarPlanta("abajo")
                self.timerDown = 0 # Es importante asignarlo fuera por si se encuentra en el extremo de la lista
        else:
            self.timerDown = 0

    def estaEnPiso(self):
        pass

    def reganar(self):
        self.estaReganado = True
        # Guarda el tiempo en el que se empieza a regañar
        self.tiempoReganado = time.time()

    def draw(self):
        pyxel.rect(self.posX, self.posY, self.ancho, self.alto, self.color)
        pyxel.text(self.posX + self.ancho / 4, self.posY + self.alto / 4, self.id, COLORES["blanco"])

        # Pintamos el jefe
        # >Parece que cambiando los números del frame count se consigue una animacion más chula
        # De momento lo dejo así, casi va sincronizado con el sonido de regañar
        if self.estaReganado and pyxel.frame_count % 16 >= 8:
            pyxel.rect(self.posX - self.ancho, self.posY - self.alto / 2, self.ancho * 0.8, self.alto * 0.8, COLORES["negro"])
            # REFACTOR cambiar de lugar
            delta_t = time.time() - self.tiempoReganado
            if delta_t >= self.tiempoMaxReganado:
                self.estaReganado = False



        # tamanoImg, banco = 16, 0
        # pyxel.blt(self.posX + 20, self.posY, banco, 0, 0, tamanoImg, tamanoImg, scale=1)

        # y = 18
        # if self.id == "M":
        #     y = 26
        # txt = f"{self.id} ({int(self.posX)}, {int(self.posY)})  Planta: {self.planta}"
        # pyxel.text(10, y, txt, 9)

        # Para dibujar al personaje DEBUG
        # dibujar(self, self.id)
