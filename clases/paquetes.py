# from os.path import altsep
#
# from json.scanner import NUMBER_RE

import pyxel

# REFACTOR: Eliminar NUM_CINTAS y SEP_ENTRE_CINTAS? --> No importarlas, usarlas como atributos?
from utils.config import COLORES, esCintaPar
from clases.elemento import Elemento


class Paquetes(Elemento):
    def __init__(self, inicioX, inicioY, anchoPaq, altoPaq, color, longitudX, longitudY, config):
        """
        En este caso, los atributos heredados de Elemento indican lo siguiente:
        - posX: posicion en el eje X donde se empiezan a dibujar las cintas/paquetes
        - posY: posicion en el eje Y donde se empiezan a dibujar las cintas/paquetes
        - ancho: Anchura de las paquetes
        - alto: Altura total del conjunto de paquetes
        - color: Color de las paquetes
        """
        # altoCintas = NUM_CINTAS * SEP_ENTRE_CINTAS
        super().__init__(inicioX, inicioY, anchoPaq, altoPaq, color)
        # minY = 25
        # inicioCinta, finCinta = 60, 200
        self.longitudX = longitudX
        self.longitudY = longitudY
        self.numCintas = longitudY

        # self.anchoPaq = 7
        # self.altoPaq = 4
        self.anchoCinta = config.anchoCinta
        self.altoCinta = config.altoCinta
        self.colorCinta = COLORES["naranja"]

        self.sepEntrePaqs = (config.anchoCinta - self.ancho) / self.longitudX
        self.sepEntreCintas = config.sepEntreCintas

        # Creamos la matriz con los paquetes
        self.matriz = self.crearMatriz(longitudX, longitudY)
        # Creamos la lista de 1D con los paquetes de la cinta 0
        self.len_cinta0 = 9
        self.cinta0_x = 220 # 220
        self.crearlista0()

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

    def crearlista0(self):
        self.lista0 = []
        #for x in range(self.longitudX):
        for x in range(self.len_cinta0): #no cambi mucho la velocidad, fíjate
            self.lista0.append(0)
        # print("lista0", self.lista0)

    def actualizarLista0(self):
        # Añade paquete
        # self.lista0[-1] = 1 #Añade un paquete en la posición de indice más grande de la lista0 (a la izquierda)

        # Comprueba indices donde hay unos y los mueve hacia la izquierda
        for i in range(1, len(self.lista0)):
            if self.lista0[i] == 1:
                self.lista0[i] = 0
                self.lista0[i - 1] = 1

    def actualizarPaquetes(self):
        # Busca los paquetes (unos) dentro de la matriz y los mueve a su siguiente posición
        for y in range(self.longitudY):
            filaActual = self.matriz[y]
            # Movemos las cintas hacia la 'derecha'. Para eso, revertimos las cintas pares (se mueven hacia la izquierda)
            if esCintaPar(y, self.numCintas):
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
            if esCintaPar(y, self.numCintas):
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
            if esCintaPar(y - 1, self.numCintas):
                self.matriz[y - 1][x] = 1
            else:
                self.matriz[y - 1][0] = 1
        # else:
        #     print("=" * 10, "Paquete en la última posición, listo para entrar al camión", "=" * 10)

    # Añade un paquete al principio de las cintas
    def anadirPaqInicio(self):
        # x = self.longitudX - 1
        # y = self.longitudY - 1
        # self.matriz[y][x] = 1
        # self.actualizarLista0()
        self.lista0[-1] = 1

    def draw(self):
        # -- Dibujamos la lista 0 de paquetes --
        ## Dibujamos los paquetes de la lista 0
        x = self.cinta0_x
        ## La lista 0 debe estar a la altura de la última cinta de paquetes
        y = self.posY + (self.longitudY - 1) * self.sepEntreCintas
        for i in range(len(self.lista0)):
            paq = self.lista0[i]
            if paq == 1:
                pyxel.rect(x, y - self.alto, self.ancho, self.alto, self.color)
            x += self.sepEntrePaqs

        ## Dibujamos la cinta 0
        pyxel.rect(self.cinta0_x, y, 200, self.altoCinta, self.colorCinta)
        pyxel.rect(self.cinta0_x + 30, y - 10, 50, 10, COLORES["negro"])
        pyxel.rect(self.cinta0_x + 5, y , 40, 1, COLORES["gris"])
        pyxel.rect(self.cinta0_x - 5, y + 3, 5, 1, COLORES["marron"])



        # -- Dibujamos las cintas --
        y = self.posY
        for j in range(self.longitudY):
            pyxel.rect(self.posX, y, self.anchoCinta, self.altoCinta, self.colorCinta)
            pyxel.rect(self.posX + 5, y , self.anchoCinta -10, self.altoCinta -3, COLORES["gris"])
            pyxel.rect(self.posX - 15, y + 3, self.anchoCinta - 125, self.altoCinta - 3, COLORES["marron"])
            pyxel.rect(self.posX + 140, y + 3, self.anchoCinta - 125, self.altoCinta - 3, COLORES["marron"])

            y += self.sepEntreCintas

        # -- Dibujamos los paquetes de la matriz --
        ## Cada paquete puede estar en una posición de la matriz, de dimensiones (longitudX, longitudY)
        x = self.posX
        for i in range(self.longitudX):
            y = self.posY
            for j in range(self.longitudY):
                if self.matriz[j][i] == 1:
                    pyxel.rect(x, y - self.alto, self.ancho, self.alto, self.color)
                # else:
                #     pyxel.rectb(x, y - self.alto, self.ancho, self.alto, self.color)
                # Pasamos a dibujar el siguiente paquete (de arriba a abajo, el inferior)
                y += self.sepEntreCintas
            # Después de recorrer toda la columna, pasar a la siguiente (de izquiera a derecha)
            x += self.sepEntrePaqs

    
    def __paqsEnJuego(self):
        # Cuenta cuantos paquetes hay actualmente en juego
        sum = 0
        for y in range(self.longitudY):
            for x in range(self.longitudX):
                if self.matriz[y][x] == 1:
                    sum += 1
        return sum

    def __str__(self):
        txt = ""
        for fila in self.matriz:
            txt += str(fila) + "\n"
        return txt

    def __repr__(self):
        return f"Paquete(longitudX={self.longitudX}, longitudY={self.longitudY}, matrizPaquetes={self.matriz})"
