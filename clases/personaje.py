import pyxel

from utils.config import NUM_CINTAS, HEIGHT, SEP_ENTRE_CINTAS
from utils.funciones import dibujar

class Personaje:
    def __init__(self, id, controles, posX, posY):
        self.id = id  # Nombre del Personaje
        self.controles = controles  # Tupla con 2 strings para las teclas
        self.posicion = [posX, posY]  # x no varía una vez asignado
        self.planta = NUM_CINTAS - 1  # ?Planta en la que se encuentra
        self.timerUp = 0       #Son temporizadores para la repetición del movimiento con btn
        self.timerDown = 0
        self.comparador = 5 #El numero de fps al que baja si matienes presionado (por debajo de 3 el jugador pierde precisión)(5 está bien)

    @property
    def controles(self):
        return self.__controles

    @controles.setter
    def controles(self, valor):
        self.__controles = valor

    @property
    def posicion(self):
        return self.__posicion

    @posicion.setter
    def posicion(self, valor):
        self.__posicion = valor

    def mover(self):
        # self.controles[0] controla el movimiento de subida
        # self.controles[1] el de bajada
        if pyxel.btnp(self.controles[0]):
            # Mover hacia arriba si no está en la más alta
            if self.planta > 0:
                self.planta -= 1
                self.posicion[1] -= SEP_ENTRE_CINTAS
            self.timerUp = 0  # reset para evitar doble salto *****

        if pyxel.btnp(self.controles[1]):
            # Mover hacia abajo si no está en la inferior
            if self.planta < NUM_CINTAS - 1:
                self.planta += 1
                self.posicion[1] += SEP_ENTRE_CINTAS
            self.timerDown = 0 # reset para evitar doble salto *****

            # Repetición al mantener pulsado arriba
            #NOTA +(tengo que revisar que funcione)+(Me parece que podría funcionar incluso con solo 1 timer para simplificar)
        if pyxel.btn(self.controles[0]):
            self.timerUp += 1
            if self.timerUp > self.comparador:
                self.timerUp = 0 #Es importante asignarlo fuera por si se encuentra en el extremo de la lista
                if self.planta > 0:
                    self.planta -= 1
                    self.posicion[1] -= SEP_ENTRE_CINTAS
        else:
            self.timerUp = 0

        # Repetición al mantener pulsado abajo
        if pyxel.btn(self.controles[1]):
            self.timerDown += 1
            if self.timerDown > self.comparador:
                self.timerDown = 0 #Es importante asignarlo fuera por si se encuentra en el extremo de la lista
                if self.planta < NUM_CINTAS - 1:
                    self.planta += 1
                    self.posicion[1] += SEP_ENTRE_CINTAS
        else:
            self.timerDown = 0

    def draw(self):
        col = 11
        if self.id.lower() == "mario":
            col = 8
        pyxel.rect(self.posicion[0], self.posicion[1], 10, 12, col)

        # DEBUG: Imprime posición
        y = 8
        if self.id == "mario":
            y = 16
        txt = f"{self.id} ({int(self.posicion[0])}, {int(self.posicion[1])})  Planta: {self.planta}"
        pyxel.text(10, y, txt, 9)

        # Para dibujar al personaje DEBUG
        # dibujar(self, self.id)

    def __repr__(self):
        return f"Personaje(controles={self.controles}, posicion={self.posicion})"
