class Elemento:
    def __init__(self, x, y, ancho, alto, color):
        self.posX = x
        self.posY = y
        self.ancho = ancho
        self.alto = alto
        self.color = color

    @property
    def posX(self):
        return self._posX
    @posX.setter
    def posX(self, valor):
        if isinstance(valor, int) or isinstance(valor, float):
            self._posX = valor
        else:
            raise TypeError("La posX debe ser un número")

    @property
    def posY(self):
        return self._posY

    @posY.setter
    def posY(self, valor):
        if isinstance(valor, int) or isinstance(valor, float):
            self._posY = valor
        else:
            raise TypeError("La posY debe ser un número")

    @property
    def ancho(self):
        return self._ancho
    @ancho.setter
    def ancho(self, valor):
        if isinstance(valor, int):
            self._ancho = valor
        else:
            raise TypeError("El ancho debe ser un entero")

    @property
    def alto(self):
        return self._alto
    @alto.setter
    def alto(self, valor):
        if isinstance(valor, int):
            self._alto = valor
        else:
            raise TypeError("El ancho debe ser un entero")

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, valor):
        if isinstance(valor, int):
            if valor > 0 or valor < 16:
                self.__color = valor
            else:
                raise ValueError("El color debe ser un índice en la lista (0-16)")
        else:
            raise TypeError("El color debe ser un entero que representa un índice en la lista")











