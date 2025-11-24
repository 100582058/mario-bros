import pyxel


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
        # Para no mover paquetes ya movidos en esta iteración, se itera dentro de una matriz nueva
        matrizNueva = self.matrizPaquetes.copy()
        for x in range(self.longitudX):
            # Recorremos la fila de dcha-izda para las cintas pares
            # y de izda-dcha para las impares
            # Así, conseguimos que un paquete no se mueva 2 veces en la misma 'actualización'
            for y in range(self.longitudY):
                paquete = self.matrizPaquetes[y][x]
                if paquete == 1:
                    matrizNueva = self.moverPaquete(x, y, matrizNueva)

        self.matrizPaquetes = matrizNueva.copy()

    # Añade un paquete al principio de las cintas
    def anadirPaquete(self):
        iX = self.longitudX - 1
        iY = self.longitudY - 1
        self.matrizPaquetes[iY][iX] = 1

    def moverPaquete(self, x, y, matrizNueva):
        # -- Mueve un paquete a la siguiente posición --
        # Determina si el paquete está en una cinta par o impar
        # REVERTIR LA FILA Y SALTARSE EL INDICE DEL QUE SE MUEVE
        cintaPar = False
        if y % 2 == 0:
            cintaPar = True
        # print("par?", cintaPar, f"({x}, {y})", self.longitudX)
        # print(self)
        if cintaPar:
            # Subir o mover a la izquierda
            if x == 0:
                self.subirPaquete(x, y, matrizNueva)
                # print("Subida desde cinta PAR")
            else:
                # Movemos la posición del paquete de (x, y) a (x - 1, y)
                # self.matrizPaquetes[y][x] = 0
                # self.matrizPaquetes[y][x - 1] = 1
                matrizNueva[y][x] = 0
                matrizNueva[y][x - 1] = 1
                # print("Movido a la izquierda")
        else:
            # Subir o mover a la derecha
            if x == self.longitudX - 1:
                self.subirPaquete(x, y, matrizNueva)
                # print("Subiendo desde cinta IMPAR")
            else:
                # Movemos la posición del paquete de (x, y) a (x + 1, y)
                # self.matrizPaquetes[y][x] = 0
                # self.matrizPaquetes[y][x + 1] = 1
                matrizNueva[y][x] = 0
                matrizNueva[y][x + 1] = 1
                # print("Movido a la derecha")
        # print("Después de mover los paquetes:", self)
        print()
        return matrizNueva

    def subirPaquete(self, x, y, matrizNueva):
        if y != 0:
            # self.matrizPaquetes[y][x] = 0
            # self.matrizPaquetes[y - 1][x] = 1
            matrizNueva[y][x] = 0
            matrizNueva[y - 1][x] = 1
        else:
            print("=" * 10, "Paquete en la última altura/cinta", "=" * 10)
        return matrizNueva

    def draw(self):
        # 130, 210, 290
        # -- Dibujamos las cintas --
        # Dibujamos las cintas de abajo a arriba
        maxY = 210
        inicioCinta, finCinta = 130, 390
        # w: finCinta - inicioCinta   /  h: Altura/Ancho de la cinta
        h = 10
        # Separación vertical entre las cintas   /   Separación horizontal entre los paquetes
        sepCintas, sepPaquetes = 40, 32.5
        rad = h * 0.3
        for cinta in range(self.longitudY):
            y = maxY - cinta * sepCintas
            pyxel.rect(inicioCinta, y, finCinta - inicioCinta, h, 9)
            # Dibujamos los 'ejes de giro' de las cintas
            # Izquierda
            pyxel.circ(inicioCinta + rad * 1.75, y + h / 2, rad, 7)
            pyxel.circ(inicioCinta + rad * 1.75, y + h / 2, 1, 0)
            # Derecha
            pyxel.circ(finCinta - (rad * 1.75), y + h / 2, rad, 7)
            pyxel.circ(finCinta - (rad * 1.75), y + h / 2, 1, 0)
        # -- Dibujamos los paquetes --
        # Cada paquete puede estar en una posición de la matriz, de dimensiones (longitudX, longitudY)
        dimPaq = 12  # Dimensiones del paquete
        # minY -> La altura a la que se empiezan a dibujar los paquertes (de arriba a abajo)
        minY = maxY - (self.longitudY - 1) * sepCintas
        for i in range(self.longitudX):
            for j in range(self.longitudY):
                x = inicioCinta + i * sepPaquetes
                # y = maxY - j * sepCintas - dimPaq
                y = minY + j * sepCintas - dimPaq
                # NOTA: SIEMPRE [y][x] o [j][i]!!! Es el orden inverso de las componentes (x, y)
                # # Se dibujan empezando de arriba a abajo, siguiendo el orden indiceJ -> [4, 3, 2, 1, 0] REFACTOR?
                # indiceJ = (self.longitudY - 1) - j
                if self.matrizPaquetes[j][i] == 1:
                    pyxel.rect(x, y, dimPaq, dimPaq * 0.85, 14)
                else:
                    pyxel.rectb(x, y, dimPaq, dimPaq * 0.85, 15)

        for i in range(self.longitudX):
            for j in range(self.longitudY):
                col = 15
                if self.matrizPaquetes[j][i] == 1:
                    col = 0
                pyxel.rect(20 + i * 10, 20 + j * 10, 5, 5, col)

    # DEBUG
    def __str__(self):
        txt = "\n"
        for fila in self.matrizPaquetes:
            txt += str(fila) + "\n"
        return txt

    def __repr__(self):
        return f"Paquete(longitudX={self.longitudX}, longitudY={self.longitudY}, matrizPaquetes={self.matrizPaquetes})"
