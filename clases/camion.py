import pyxel

from utils.config import COLORES
from clases.elemento import Elemento

class Camion(Elemento):
    def __init__(self, posX, posY, ancho, alto, color, config):
        super().__init__(posX, posY  + 2, ancho, alto, color)

        self.carga = 0

        # Posición inicial, donde carga los paquetes
        self.__posicionCarga = posX
        # Posición fuera de la pantalla, donde descarga los paquetes
        self.__posicionDescarga = -40
        self.__velocidadCamion = 2
        self.__velocidadCamionRetroceso = 1
        # -1 si va hacia la izda, 0 si está quieto y 1 si va a la dcha
        self.__dirMov = 0 
        self.__compSonidoRetroceso = 0

        # Almacena el número de repartos que se han hecho desde que se eliminó un fallo
        self.numRepartos = 0

        # Atributos de la configuración del nivel
        self.__anchoPaq = config.anchoPaq
        self.__altoPaq = config.altoPaq

    def __dibujarPaquete(self, x, y):
        pyxel.rect(x, y + 1, self.__anchoPaq, self.__altoPaq, COLORES["azulMarino"])
        w = int(self.__anchoPaq * 0.2)
        h = int(self.__altoPaq * 0.4)
        pyxel.rect(x, y + h + 1, self.__anchoPaq, 1, COLORES["blanco"])
        # Y otra linea para completar el 'lazo'
        pyxel.rect(x + w, y + 1, 1, self.__altoPaq, COLORES["blanco"])


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
        # Condición inicial para que se empiece a mover
        if self.carga >= 8:
            # Añadimos un reparto
            self.numRepartos += 1
            self.__dirMov = -1
        if self.__dirMov != 0:
            if self.posX > self.__posicionDescarga and self.__dirMov == -1: #por ejemplo (tiene que estar fuera de la pantalla)
                self.posX -= self.__velocidadCamion #Izquierda. En funcion de esto irá mas o menos rápido
            elif self.posX <= self.__posicionDescarga:
                self.carga = 0
                self.__dirMov = 1

            if self.posX < self.__posicionCarga and self.__dirMov == 1:
                self.posX += self.__velocidadCamionRetroceso

                if self.__compSonidoRetroceso == 0:  #Para que el sonido se ejecute solo 1 vez
                    self.__compSonidoRetroceso += 1
                    pyxel.play(3, 15) #sonido camión retroceso (mismo canal que los fallos porque al no poder
                                    # reproducirse a la vez no se puede glichear(así ahorramos un canal))

            elif self.posX >= self.__posicionCarga:
                self.__dirMov = 0
                self.__compSonidoRetroceso == 0

    
    def draw(self):
        # -- Pinta el camión y los paquetes --
        # Camión
        pyxel.rect(self.posX, self.posY, self.ancho, self.alto, COLORES["azulMarino"])
        # Ruedas
        pyxel.rect(self.posX +1, self.posY +2, self.ancho -25, self.alto, COLORES["negro"])
        pyxel.rect(self.posX + 3, self.posY + 4, self.ancho - 29, self.alto -4, COLORES["gris"])
        pyxel.rect(self.posX+25, self.posY +2, self.ancho - 25, self.alto, COLORES["negro"])
        pyxel.rect(self.posX + 27, self.posY + 4, self.ancho - 29, self.alto -4, COLORES["gris"])
        pyxel.rect(self.posX, self.posY - 10, self.ancho - 20, self.alto+ 5, COLORES["azulMarino"])
        pyxel.rect(self.posX, self.posY - 7, self.ancho - 24, self.alto, COLORES["azulCeleste"])
        pyxel.rect(self.posX, self.posY, self.ancho, self.alto - 4, COLORES["azul"])
        pyxel.rect(self.posX + 28, self.posY - 4, self.ancho - 28, self.alto, COLORES["azul"])

        # Paquetes dentro del camión

        paqAnchoEnCamion = 8 # Uno más para que haya separación después

        for i in range(self.carga):
            fila = i // 2  # 4 niveles (entre dos porque es de dos en dos)
            columna = i % 2  # asignar la izquierda o la derecha (1 y 0)

            x = self.posX + 12 + columna * paqAnchoEnCamion # si la columna es 0 no influye
            y = self.posY - 5 - fila * self.alto

            self.__dibujarPaquete(x, y)

