class Paquetes:
    def __init__(self, longitudX, longitudY):
        # Creamos la matriz con los paquetes de tamaño (posiconesCinta, numCintas)
        self.longitudX = longitudX
        self.longitudY = longitudY
        self.matrizPaquetes = self.inicializarPaquetes(longitudX, longitudY)

    @property
    def longitudX(self):
        return self.__longitudX

    @longitudX.setter
    def longitudX(self, valor):
        if isinstance(valor, int) and valor > 0:
            self.__longitudX = valor
        else:
            raise TypeError("LongitudX debe ser un entero positivo")

    @property
    def longitudY(self):
        return self.__longitudY

    @longitudY.setter
    def longitudY(self, valor):
        if isinstance(valor, int) and valor > 0:
            self.__longitudY = valor
        else:
            raise TypeError("LongitudY debe ser un entero positivo")

    def inicializarPaquetes(self, longitudX, longitudY):
        matriz = []
        for y in range(longitudY):
            fila = []
            for x in range(longitudX):
                fila.append(0)
            matriz.append(fila)
        return matriz

    def actualizarPaquetes(self):
        # Busca los paquetes (1s) dentro de la matriz y los mueve a su siguiente posición
        for x in range(self.longitudX):
            for y in range(self.longitudY):
                paquete = self.matrizPaquetes[y][x]
                if paquete == 1:
                    self.moverPaquete(x, y)

    # Añade un paquete al principio de las cintas
    def anadirPaquete(self):
        iX = self.longitudX - 1
        iY = self.longitudY - 1
        self.matrizPaquetes[iY][iX] = 1

    def moverPaquete(self, x, y):
        # -- Mueve un paquete a la siguiente posición --
        # Determina si el paquete está en una cinta par o impar
        cintaPar = False
        if y % 2 == 0:
            cintaPar = True
        if cintaPar:
            # Probar a mover izda
            if x == 0:
                self.subirPaquete(x, y)
            else:
                # Movemos la posición del paquete de (x, y) a (x - 1, y)
                self.matrizPaquetes[y][x] = 0
                self.matrizPaquetes[y][x - 1] = 1
        else:
            # Mover dcha
            if x == self.longitudX - 1:
                self.subirPaquete(x, y)
            else:
                # Movemos la posición del paquete de (x, y) a (x + 1, y)
                self.matrizPaquetes[y][x] = 0
                self.matrizPaquetes[y][x + 1] = 1
        print("Matriz después de mover los paquetes", self)

    def subirPaquete(self, x, y):
        if y != 0:
            self.matrizPaquetes[y][x] = 0
            self.matrizPaquetes[y - 1][x] = 1
        else:
            print("=" * 10, "Paquete en la última altura/cinta", "=" * 10)

    # DEBUG
    def __str__(self):
        txt = "\n"
        for fila in self.matrizPaquetes:
            txt += str(fila) + "\n"
        return txt

    def __repr__(self):
        return f"Paquete(longitudX={self.longitudX}, longitudY={self.longitudY}, matrizPaquetes={self.matrizPaquetes})"
