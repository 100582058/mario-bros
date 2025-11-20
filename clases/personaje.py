import pyxel

# ERROR: Circular import
from utils.config import NUM_CINTAS

class Personaje:
    def __init__(self, id, controles, posX, posY):
        self.id = id  # Nombre del Personaje
        self.controles = controles  # Tupla con 2 strings para las teclas
        self.posicion = [posX, posY]  # x no varía una vez asignado
        self.planta = 0  # ?Planta en la que se encuentra

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
            if self.planta < NUM_CINTAS - 1:
                self.planta += 1
                self.posicion[1] -= 40
        if pyxel.btnp(self.controles[1]):
            # Mover hacia abajo si no está en la inferior
            if self.planta > 0:
                self.planta -= 1
                self.posicion[1] += 40

    def draw(self):
        col = 11
        if self.id.lower() == "mario":
            col = 8
        pyxel.rect(self.posicion[0], self.posicion[1], 20, 25, col)

        # DEBUG: Imprime posición
        y = 10
        if self.id == "mario":
            y = 20
        txt = f"{self.id} ({int(self.posicion[0])}, {int(self.posicion[1])})  Planta: {self.planta}"
        pyxel.text(250, y, txt, 9)

    def __repr__(self):
        return f"Personaje(controles={self.controles}, posicion={self.posicion})"
