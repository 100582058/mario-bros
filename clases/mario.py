import pyxel
import time
from clases.personaje import Personaje
from utils.config import COLORES

class Mario(Personaje):
    def __init__(self, id_personaje, posX, posY, ancho, alto, color, controles, config):
        super().__init__(id_personaje, posX, posY, ancho, alto, color, controles, config)

    def mover(self):
        super().mover()

    def intentarCambiarPlanta(self, direccion):
        # Los personajes solo están en la cinta 0
        # o en las pares (Luigi) o impares (Mario)
        cinta = (self.numCintas - 1) - self.planta
        if cinta == 0 and direccion == "arriba":
            self.subir()
        elif cinta == 1:
            # Sube 2 (a una cinta impar) o baja 1 (a la cinta 0)
            if direccion == "arriba":
                self.subir(2)
            elif direccion == "abajo":
                self.bajar()
        elif cinta > 1:
            # En el resto de plantas, se mueve de 2 en 2
            if direccion == "arriba" and cinta + 2 <= self.numCintas - 1:
                self.subir(2)
            elif direccion == "abajo" and cinta - 2 >= 0:
                self.bajar(2)

    def draw(self):
        super().draw()
        # # Dibujamos la plataforma del jefe
        # x = 225
        # y = 75
        # pyxel.rect(x, y, 26, 3, COLORES["marron"])
        # pyxel.rect(x + 2, y, 22, 2, COLORES["verde"])
        #
        #
        # if not self.__estaReganado:
        #     super().draw()
        # else:
        #     # Dibujamos a Mario en la plataforma
        #     pyxel.rect(x, y, self.ancho, self.alto, self.color)
        #     pyxel.text(x + self.ancho / 4, y + self.alto / 4, self.id, COLORES["blanco"])
        #
        #     delta_t = time.time() - self.__tiempoReganado
        #     if delta_t >= self.__tiempoMaxReganado:
        #         self.__estaReganado = False
