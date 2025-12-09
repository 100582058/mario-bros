import pyxel

from utils.config import COLORES
from clases.elemento import Elemento

class Camion(Elemento):
    def __init__(self, posX, posY, ancho, alto, color, config):
        super().__init__(posX, posY, ancho, alto, color)

        self.carga = 0

        # Matriz para dibujar los paquetes
        self.matrizPaqs = []
        self.__anadirPaqsMatriz()

        # Posición inicial, donde carga los paquetes
        self.posicionCarga = posX
        # Posición fuera de la pantalla, donde descarga los paquetes
        self.posicionDescarga = -40
        self.velocidadCamion = 3
        self.velocidadCamionRetroceso = 1
        # -1 si va hacia la izda, 0 si está quieto y 1 si va a la dcha
        self.dirMov = 0 
        self.compSonidoRetroceso = 0

        # Atributos de la configuración del nivel
        self.config = config


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

                if self.compSonidoRetroceso == 0:  #Para que el sonido se ejecute solo 1 vez
                    self.compSonidoRetroceso += 1
                    pyxel.play(3, 15) #sonido camión retroceso (mismo canal que los fallos porque al no poder
                                    # reproducirse a la vez no se puede glichear(así ahorramos un canal))

            elif self.posX >= self.posicionCarga:
                self.dirMov = 0
                self.compSonidoRetroceso == 0

        # Añade los paquetes a la matriz para que se dibujen correctamente
        self.__anadirPaqsMatriz()

    def __anadirPaqsMatriz(self):
        # Inicializamos la matriz vacía
        self.matrizPaqs = []
        for i in range(2):
            self.matrizPaqs.append([0, 0, 0, 0])
        # Añadimos cada paquete por orden a la matriz
        for paq in range(self.carga):
            print(paq)

        print(self.matrizPaqs)


    
    def draw(self):
        # -- Pinta el camión y los paquetes --
        # Camión
        pyxel.rect(self.posX, self.posY, self.ancho, self.alto, self.color)
        # Ruedas
        pyxel.rect(self.posX +1, self.posY +2, self.ancho -25, self.alto, COLORES["negro"])
        pyxel.rect(self.posX + 3, self.posY + 4, self.ancho - 29, self.alto -4, COLORES["gris"])
        pyxel.rect(self.posX+25, self.posY +2, self.ancho - 25, self.alto, COLORES["negro"])
        pyxel.rect(self.posX + 27, self.posY + 4, self.ancho - 29, self.alto -4, COLORES["gris"])

        # Dibujamos los paquetes
        x, y = self.posX, self.posY



    # Dibujamos los paquete (nivel 5) en el camión
    def __dibujarPaquete(self, x, y):
        w = int(self.config.anchoPaq * 0.2)
        h = int(self.config.altoPaq * 0.4)
        pyxel.rect(x, y + h, self.ancho, 1, COLORES["blanco"])
        # Y otra linea para completar el 'lazo'
        pyxel.rect(x + w, y, 1, self.alto, COLORES["blanco"])

