import pyxel
import time

from utils.config import COLORES, esCintaPar, minimo
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
        self.len_cinta0 = 9 * 2 # REFACTOR? 9 posiciones usadas, mas 9 por si hay paquetes cerca de los personajes
        self.cinta0_x = 220  # 220
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
        
    @property
    def numCintas(self):
        return self.__numCintas
    @numCintas.setter
    def numCintas(self, valor):
        if isinstance(valor, int) and valor > 0:
            self.__numCintas = valor
        else:
            raise TypeError("El número de cintas debe ser un entero positivo")

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
        # for x in range(self.longitudX):
        for x in range(self.len_cinta0):
            self.lista0.append(0)
        # print("lista0", self.lista0)

    def actualizarLista0(self):
        # Añade paquete
        # self.lista0[-1] = 1 #Añade un paquete en la posición de indice más grande de la lista0 (a la izquierda)

        # Comprueba indices donde hay unos y los mueve hacia la izquierda
        for i in range(1, int(self.len_cinta0 / 2)):
            if self.lista0[i] != 0:
                self.lista0[i] = 0
                self.lista0[i - 1] = 1
        # Para los paquetes más lejanos, solo los actualiza si no hay paquetes cerca
        if not self.__paqueteCercaPersonaje()[0]:
            for i in range(int(self.len_cinta0 / 2), self.len_cinta0):
                if self.lista0[i] != 0:
                    self.lista0[i] = 0
                    self.lista0[i - 1] = 1
        # print(self.lista0)

    # Actualiza los paquetes del grupo de cintas seleccionado
    def actualizarPaquetes(self, grupo):
        self.__paquetesSincronizados()
        # Creamos una lista de índices por los que iterará el bucle, dependiendo del grupo seleccionado
        indices = []
        if grupo == "pares":
            for i in range(self.longitudY):
                if esCintaPar(i, self.__numCintas):
                    indices.append(i)
        elif grupo == "impares":
            for i in range(self.longitudY):
                if not esCintaPar(i, self.__numCintas):
                    indices.append(i)

        # Busca los paquetes (unos) dentro de la matriz y los mueve a su siguiente posición
        for y in indices:
            filaActual = self.matriz[y]
            # Movemos todas las cintas hacia la 'derecha'. Para eso, revertimos las cintas pares (se mueven hacia la izquierda)
            if esCintaPar(y, self.__numCintas):
                # Cinta par
                filaActual.reverse()
            # Se evalúa primero el último elemento de la lista
            x = self.longitudX - 1
            if filaActual[x] != 0:
                # Subimos el paquete al lado correcto
                self.subirPaquete(x, y)
                # Eliminamos la posición actual del paquete de la variable 'filaActual'
                filaActual[x] = 0

            # Comprobamos cada posición de la fila y movemos los paquetes
            # Bucle inverso desde el penúltimo elemento hasta el primero (índice 0)
            for x in range(self.longitudX - 2, -1, -1):
                if filaActual[x] != 0:
                    filaActual = self.moverDcha(filaActual, x)
            # Le damos la vuelta otra vez, si es necesario
            if esCintaPar(y, self.__numCintas):
                filaActual.reverse()
            self.matriz[y] = filaActual

    def moverDcha(self, fila, x):
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
            valorActual = self.matriz[y][x]
            self.matriz[y][x] = 0
            # Subimos el paquete al lado que corresponde
            # (a la izquierda en las pares, a la derecha en las impares)
            if esCintaPar(y - 1, self.__numCintas):
                self.matriz[y - 1][x] = valorActual + 1
            else:
                self.matriz[y - 1][0] = valorActual + 1

    # Añade un paquete al final de la cinta 0
    def anadirPaqInicio(self):
        # print("cerca", self.__paqueteCercaPersonaje())
        if not self.__paqueteCercaPersonaje()[0]:
            self.lista0[9] = 1
        else:
            # print("SE AÑADE MÁS LEJOS")
            self.lista0[-1] = 1

    def draw(self):
        # -- Dibujamos la lista 0 de paquetes --
        # Dibujamos los paquetes de la lista 0
        x = self.cinta0_x
        # La lista 0 debe estar a la altura de la última cinta de paquetes
        y = self.posY + (self.longitudY - 1) * self.sepEntreCintas
        for i in range(len(self.lista0)):
            paq = self.lista0[i]
            if paq == 1:
                pyxel.rect(x, y - self.alto, self.ancho, self.alto, self.color)
            x += self.sepEntrePaqs

        # Dibujamos la cinta 0
        pyxel.rect(self.cinta0_x, y, 200, self.altoCinta, self.colorCinta)
        pyxel.rect(self.cinta0_x + 30, y - 10, 50, 10, COLORES["negro"])
        pyxel.rect(self.cinta0_x + 5, y, 40, 1, COLORES["gris"])
        pyxel.rect(self.cinta0_x - 5, y + 3, 5, 1, COLORES["marron"])

        # -- Dibujamos las cintas --
        y = self.posY
        for j in range(self.longitudY):
            pyxel.rect(self.posX, y, self.anchoCinta,
                       self.altoCinta, self.colorCinta)
            pyxel.rect(self.posX + 5, y, self.anchoCinta - 10,
                       self.altoCinta - 3, COLORES["gris"])
            pyxel.rect(self.posX - 15, y + 3, self.anchoCinta -
                       125, self.altoCinta - 3, COLORES["marron"])
            pyxel.rect(self.posX + 140, y + 3, self.anchoCinta -
                       125, self.altoCinta - 3, COLORES["marron"])
            # Dibujamos una flecha indicando la direccion de la cinta
            flechasTotales = 3
            flechasX = self.posX
            flechasY = y - 7
            tamanoFlecha, color = 3, COLORES["marron"]
            for i in range(flechasTotales):
                flechasX += (self.anchoCinta / (flechasTotales + 1))
                if esCintaPar(j, self.__numCintas):
                    # Flecha hacia la derecha
                    pyxel.line(flechasX - tamanoFlecha, flechasY, flechasX,
                               flechasY + tamanoFlecha, color)
                    pyxel.line(flechasX - tamanoFlecha, flechasY, flechasX,
                               flechasY - tamanoFlecha, color)
                else:
                    # Flecha hacia la izquierda
                    pyxel.line(flechasX, flechasY, flechasX - tamanoFlecha,
                               flechasY + tamanoFlecha, color)
                    pyxel.line(flechasX, flechasY, flechasX - tamanoFlecha,
                               flechasY - tamanoFlecha, color)

            y += self.sepEntreCintas

        # -- Dibujamos los paquetes de la matriz --
        # Cada paquete puede estar en una posición de la matriz, de dimensiones (longitudX, longitudY)
        x = self.posX
        for i in range(self.longitudX):
            y = self.posY
            for j in range(self.longitudY):
                if self.matriz[j][i] != 0:
                    pyxel.rect(x, y - self.alto, self.ancho,
                               self.alto, self.color)
                # else:
                #     pyxel.rectb(x, y - self.alto, self.ancho, self.alto, self.color)
                # Pasamos a dibujar el siguiente paquete (de arriba a abajo, el inferior)
                y += self.sepEntreCintas
            # Después de recorrer toda la columna, pasar a la siguiente (de izquiera a derecha)
            x += self.sepEntrePaqs

    def __paqsEnJuego(self):
        # Cuenta cuantos paquetes hay actualmente en juego (no tiene en cuenta la última fila, ya que ese paquete va a desaparecer pronto)
        sum = 0
        for y in range(self.longitudY - 1):
            for x in range(self.longitudX):
                if self.matriz[y][x] != 0:
                    sum += 1
        return sum

    # Comprueba si hay algun paquete a menos de 'distancia' distancia de los personajes cuando ocurre un fallo
    # Devuelve la posición del paquete en forma de tupla (equivalente a True) o False REFACTOR
    def __paqueteCercaPersonaje(self, distancia=8): # 2
        # Comprobamos por la izquierda
        for j in range(self.longitudY):
            for i in range(0, distancia):
                if self.matriz[j][i] != 0:
                    # print(j, i, "paquete cerca borde izdo")
                    return (i, j)
        # Comprobamos por la derecha
        for j in range(self.longitudY):
            for i in range(self.longitudX - distancia, self.longitudX):
                if self.matriz[j][i] != 0:
                    # print(j, i, "paquete cerca borde dcho")
                    return (i, j)
        # Comprobamos en la cinta 0
        for i in range(distancia):
            if self.lista0[i] != 0:
                # print(i, "paquete cerca borde cinta 0", self.lista0)
                # Truco barato para saber que hay que eliminar un paquete de la cinta 0
                return (i, None)


        # Si no, devuelve falso (en forma de tupla para seguir con el formato)
        return (False, False)

    def __paquetesSincronizados(self):
    # Comprueba y elimina paquetes sincronizados cerca del borde
        # Comprobamos por la izquierda
        contadorPaquetesBorde = 0
        for j in range(self.longitudY):
                if self.matriz[j][0] != 0:
                    contadorPaquetesBorde += 1
        # Si hay varios paquetes en el borde, borramos todos 
        if contadorPaquetesBorde >= 2:
            for j in range(self.longitudY):
                self.matriz[j][0] = 0
            print("paquete sincronizado, eliminados todos izda")
            print("Por que solo izda???")

        # Comprobamos por la derecha
        contadorPaquetesBorde = 0
        for j in range(self.longitudY):
            if self.matriz[j][self.longitudX - 1] != 0:
                contadorPaquetesBorde += 1
                print(self)
        # Si hay varios paquetes en el borde, borramos todos
        if contadorPaquetesBorde >= 2:
            for j in range(self.longitudY):
                self.matriz[j][self.longitudX - 1] = 0
            print("paquete sincronizado, eliminados todos dcha")

    def eliminPaquetesBorde(self):
        i, j = self.__paqueteCercaPersonaje()
        if not j and i:
            # Si 'j' no está definida pero 'i' sí, es la cinta 0
            self.cinta0[i] = 0
            print(j, i, "Paquete borrado, cinta 0")
        elif i and j:
            # Si 'i' y 'j' están definidas -> Hay que quitar un paquete de la matriz
            print(j, i, "Paquete borrado matriz, estaba cerca del borde")
            self.matriz[j][i] = 0


    def __str__(self):
        txt = ""
        for fila in self.matriz:
            txt += str(fila) + "\n"
        return txt

    def __repr__(self):
        return f"Paquete(longitudX={self.longitudX}, longitudY={self.longitudY}, matrizPaquetes={self.matriz})"
