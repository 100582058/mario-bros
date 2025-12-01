import pyxel

from utils.config import NUM_CINTAS, COLORES

class Camion:
    def __init__(self, posX, posY):
        self.posicion = [posX, posY]  # Y no varía una vez asignado
        self.camionLista = []
        self.carga = 0
        self.posicionDescarga = -10
        self.posicionCarga = 20
        self.velocidadCamion = 1

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


#NUEVA FUNCIÓN (revisar en prog)#
    def mover_y_descargar(self):
        while self.posicion[0] > self.posicionDescarga: #por ejemplo (tiene que estar fuera de la pantalla)
            self.posicion[0] -= self.velocidadCamion #Izquierda. En funcion de esto irá mas o menos rápido
        if self.posicion[0] == self.posicionDescarga:
            while self.camionLista != []:
                del self.camionLista[0]
        while self.posicion[0] != self.posicionCarga:
            self.posicion[0] += self.velocidadCamion


        # return (pintar un rectangulo donde en la lista camionLista haya un 1)
        self.draw()
    
    def draw(self):
        # Pinta el camión y los paquetes
        # Por ejemplo:
        pyxel.rect(self.posicion[0], self.posicion[1], 40, 15, COLORES["marron"])
