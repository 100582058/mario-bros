import pyxel

from utils.config import cintaPar

class Paquetes:
    def __init__(self, longitudX, longitudY):
        # Creamos la matriz con los paquetes de tamaño (posiconesCinta, numCintas)
        self.longitudX = longitudX
        self.longitudY = longitudY
        self.matriz = self.crearMatriz(longitudX, longitudY)

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

    def crearMatriz(self, longitudX, longitudY):
        matriz = []
        for y in range(longitudY):
            fila = []
            for x in range(longitudX):
                fila.append(0)
            matriz.append(fila)
        return matriz

    def actualizarPaquetes(self):
        # Busca los paquetes (unos) dentro de la matriz y los mueve a su siguiente posición
        for y in range(self.longitudY):
            filaActual = self.matriz[y]
            # Movemos las cintas hacia la 'derecha'. Para eso, revertimos las cintas pares (se mueven hacia la izquierda)
            if cintaPar(y):
                # Cinta par
                filaActual.reverse()
            # Se evalúa primero el último elemento de la lista
            x = self.longitudX - 1
            if filaActual[x] == 1:
                # Subimos el paquete al lado correcto
                self.subirPaquete(x, y)
                # Eliminamos la posición actual del paquete de la variable 'filaActual'
                filaActual[x] = 0

            # Comprobamos cada posición de la fila y movemos los paquetes
            # Bucle inverso desde el penúltimo elemento hasta el primero (índice 0)
            for x in range(self.longitudX - 2, -1, -1):
                if filaActual[x] == 1:
                    filaActual = self.moverDcha(filaActual, x, y)
            # Le damos la vuelta otra vez, si es necesario
            if cintaPar(y):
                filaActual.reverse()
            self.matriz[y] = filaActual

    def moverDcha(self, fila, x, y):
        # -- Mueve un paquete a la siguiente posición --
        if x + 1 < self.longitudX:
            # Movemos la posición del paquete de (x, y) a (x + 1, y)
            fila[x] = 0
            fila[x + 1] = 1
        else:
            print("ERROR: Paquete al final, se debería haber subido")
        return fila

    def subirPaquete(self, x, y):
        if y != 0:
            self.matriz[y][x] = 0
            # Subimos el paquete al lado que corresponde (a la izquierda en las pares, a la derecha en las impares)
            if cintaPar(y - 1):
                self.matriz[y - 1][x] = 1
            else:
                self.matriz[y - 1][0] = 1
        else:
            print("=" * 10, "Paquete en la última posición, listo para entrar al camión", "=" * 10)

    # Añade un paquete al principio de las cintas
    def anadirPaqInicio(self):
        x = self.longitudX - 1
        y = self.longitudY - 1
        self.matriz[y][x] = 1

    def draw(self):
        # 130, 210, 290
        # -- Dibujamos las cintas --
        # Dibujamos las cintas de abajo a arriba
        maxY = 210
        inicioCinta, finCinta = 60, 200
        # w: finCinta - inicioCinta   /  h: Altura/Ancho de la cinta
        h = 5
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
                if self.matriz[j][i] == 1:
                    pyxel.rect(x, y, dimPaq, dimPaq * 0.85, 14)
                else:
                    pyxel.rectb(x, y, dimPaq, dimPaq * 0.85, 15)

    
    def __paqsEnJuego(self):
        # Cuenta cuantos paquetes hay actualmente en juego
        sum = 0
        for y in range(self.longitudY):
            for x in range(self.longitudX):
                if self.matriz[y][x] == 1:
                    sum += 1
        return sum

    # DEBUG
    def __str__(self):
        txt = ""
        for fila in self.matriz:
            txt += str(fila) + "\n"
        return txt

    def __repr__(self):
        return f"Paquete(longitudX={self.longitudX}, longitudY={self.longitudY}, matrizPaquetes={self.matriz})"
