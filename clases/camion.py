import pyxel

from utils.config import NUM_CINTAS, COLORES

class Camion:
    def __init__(self, posX, posY):
        self.posicion = [posX, posY]  # Y no varía una vez asignado
        self.carga = 0
        self.posicionDescarga = -40
        self.posicionCarga = 10
        self.velocidadCamion = 2
        # -1 si va hacia la izda, 0 si está quieto y 1 si va a la dcha
        self.dirMov = 0

    @property
    def posicion(self):
        return self.__posicion
    @posicion.setter
    def posicion(self, valor):
        if isinstance(valor, list):
            self.__posicion = valor
        else:
            raise TypeError("La posición debe ser una array con 2 números")

    @property
    def carga(self):
        return self.__carga
    @carga.setter
    def carga(self, valor):
        if isinstance(valor, int) and valor >= 0:
            self.__carga = valor
        else:
            raise TypeError("La carga debe ser un entero positivo")

    def __repr__(self):
        return f"Camion(posicion={self.posicion}, carga={self.carga})"


    def mover_y_descargar(self):
        # Condición inicial para que se empieze a mover
        if self.carga >= 8:
            self.dirMov = -1
        if self.dirMov != 0:
            if self.posicion[0] > self.posicionDescarga and self.dirMov == -1: #por ejemplo (tiene que estar fuera de la pantalla)
                self.posicion[0] -= self.velocidadCamion #Izquierda. En funcion de esto irá mas o menos rápido
                print("hacia la izquierda")
            elif self.posicion[0] <= self.posicionDescarga:
                self.carga = 0
                print("vacia camion, ahora se movería hacia la derecha")
                self.dirMov = 1

            if self.posicion[0] < self.posicionCarga and self.dirMov == 1:
                self.posicion[0] += self.velocidadCamion
                print("hacia derecha")
            elif self.posicion[0] >= self.posicionCarga:
                self.dirMov = 0
                print("Ahora se movería hacia la izda")


    
    def draw(self):
        # Pinta el camión y los paquetes
        # Por ejemplo:
        longitudCamion = 30
        pyxel.rect(self.posicion[0], self.posicion[1], longitudCamion, 5, COLORES["marron"])
        pyxel.rect(self.posicion[0] +1, self.posicion[1] +2, longitudCamion -25, 5, COLORES["negro"])
        pyxel.rect(self.posicion[0]+25, self.posicion[1] +2, longitudCamion - 25, 5, COLORES["negro"])
        # Paquetes
        pyxel.rect(self.posicion[0], self.posicion[1] - 5, longitudCamion * (self.carga / 8), 5, COLORES["rosa"])
