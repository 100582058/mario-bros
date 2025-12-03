import pyxel

from utils.config import NUM_CINTAS, COLORES
from clases.elemento import Elemento

class Camion(Elemento):
    def __init__(self, posX, posY, ancho, alto, color):
        super().__init__(posX, posY, ancho, alto, color)
        self.carga = 0
        # Posición inicial, donde carga los paquetes
        self.posicionCarga = posX
        # Posición fuera de la pantalla, donde descarga los paquetes
        self.posicionDescarga = -40
        self.velocidadCamion = 3
        self.velocidadCamionRetroceso = 1.5
        # -1 si va hacia la izda, 0 si está quieto y 1 si va a la dcha
        self.dirMov = 0
    @property
    def carga(self):
        return self.__carga
    @carga.setter
    def carga(self, valor):
        if isinstance(valor, int) and valor >= 0:
            self.__carga = valor
        else:
            raise TypeError("La carga debe ser un entero positivo")


    def mover_y_descargar(self):
        # Condición inicial para que se empieze a mover
        if self.carga >= 8:
            self.dirMov = -1
        if self.dirMov != 0:
            if self.posX > self.posicionDescarga and self.dirMov == -1: #por ejemplo (tiene que estar fuera de la pantalla)
                self.posX -= self.velocidadCamion #Izquierda. En funcion de esto irá mas o menos rápido
            elif self.posX <= self.posicionDescarga:
                self.carga = 0
                self.dirMov = 1

            if self.posX < self.posicionCarga and self.dirMov == 1:
                self.posX += self.velocidadCamionRetroceso
            elif self.posX >= self.posicionCarga:
                self.dirMov = 0


    
    def draw(self):
        # -- Pinta el camión y los paquetes --
        # Camión
        pyxel.rect(self.posX, self.posY, self.ancho, self.alto, self.color)
        # Ruedas
        pyxel.rect(self.posX +1, self.posY +2, self.ancho -25, self.alto, COLORES["negro"])
        pyxel.rect(self.posX + 3, self.posY + 4, self.ancho - 29, self.alto -4, COLORES["gris"])
        pyxel.rect(self.posX+25, self.posY +2, self.ancho - 25, self.alto, COLORES["negro"])
        pyxel.rect(self.posX + 27, self.posY + 4, self.ancho - 29, self.alto -4, COLORES["gris"])
        # Paquetes dentro del camión
        pyxel.rect(self.posX, self.posY - 5, self.ancho * (self.carga / 8), self.alto, COLORES["rosa"])
