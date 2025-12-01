import pyxel

from utils.config import NUM_CINTAS, COLORES

class Camion:
    def __init__(self, posX, posY):
        self.posicion = [posX, posY]  # No varía una vez asignado
        self.camionLista = []
        self.carga = 0

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



    def mover(self):
        #if fabrica.paquetes.matriz[0][0] == 1 and fabrica.luigi.planta == NUM_CINTAS - 1:
            # Eliminamos el paquete de la matriz de paquetes
            #print("Paquete tiene que eliminarse desde paquete.py, si Luigi está en esa posición")
            # fabrica.paquetes.matriz[0][0] = 0
            #self.camionLista.append(1) #creo que se dibuja solo con lo de que se dibuja un paquete en los 1 que implementaste
        # else: 
            # Si no, no hace nada, no?
            # Si no está Luigi, pierde una vida
            # pop paquete(0, 0)
        
        while len(self.camionLista) == 8:
            # stop paquetes de la matriz e igual a los personajes #tengo que ver como se implementa
            # posX es una variable ajena a Camion, mejor usar self.posX (self.posicion[0], según el código de __init__)
            self.posicion[0] -= pyxel.frame_count % 30
            tal = -20
            x_inicial = 100
            if self.posicion[0] == tal: #cuando salga de la pantalla
                # Eliminamos todos los paquetes del camión
                self.camionLista = []
                while self.posicion[0] != x_inicial: 
                    self.posicion[0] += pyxel.frame_count % 30
        
        # No, así no se pinta un rectángulo
        # return (pintar un rectangulo donde en la lista camionLista haya un 1)
        self.draw()
    
    def draw(self):
        # Pinta el camión y los paquetes
        # Por ejemplo:
        pyxel.rect(self.posicion[0], self.posicion[1], 40, 15, COLORES["marron"])
