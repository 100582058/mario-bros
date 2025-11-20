class Camion:
    def __init__(self, posX, posY):
        self.posicion = [posX, posY]  # No varía una vez asignado
        # Cantidad de paquetes en el camión
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
