import pyxel
import time

from utils.config import COLORES
from clases.elemento import Elemento
from utils.funciones import dibujar

class Personaje(Elemento):
    def __init__(self, id_personaje, posX, posY, color, controles, config):
        super().__init__(posX, posY, 10, 12, color)
        self.id = id_personaje  # Nombre del Personaje
        self.controles = controles  # Tupla con 2 strings para las teclas
        self.planta = config.numCintas - 1  # Planta en la que se encuentra
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

    def mover(self):
        # self.controles[0] controla el movimiento de subida
        # self.controles[1] el de bajada
        if pyxel.btnp(self.controles[0]):
            # Mover hacia arriba si no está en la más alta
            if self.planta > 0:
                self.planta -= 1
                self.posY -= self.sepEntreCintas
            self.timerUp = 0  # reset para evitar doble salto *****

        if pyxel.btnp(self.controles[1]):
            # Mover hacia abajo si no está en la inferior
            if self.planta < self.numCintas - 1:
                self.planta += 1
                self.posY += self.sepEntreCintas
            self.timerDown = 0 # reset para evitar doble salto *****

            # Repetición al mantener pulsado arriba
            #NOTA +(tengo que revisar que funcione)+(Me parece que podría funcionar incluso con solo 1 timer para simplificar)
        if pyxel.btn(self.controles[0]):
            self.timerUp += 1
            if self.timerUp > self.comparador:
                self.timerUp = 0 #Es importante asignarlo fuera por si se encuentra en el extremo de la lista
                if self.planta > 0:
                    self.planta -= 1
                    self.posY -= self.sepEntreCintas
        else:
            self.timerUp = 0

        # Repetición al mantener pulsado abajo
        if pyxel.btn(self.controles[1]):
            self.timerDown += 1
            if self.timerDown > self.comparador:
                self.timerDown = 0 #Es importante asignarlo fuera por si se encuentra en el extremo de la lista
                if self.planta < self.numCintas - 1:
                    self.planta += 1
                    self.posY += self.sepEntreCintas
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
