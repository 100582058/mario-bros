import pyxel
import time
import random

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
        super().__init__(inicioX, inicioY, anchoPaq, altoPaq, color)
        self.longitudX = longitudX
        self.longitudY = longitudY
        self.numCintas = longitudY

        self.anchoCinta = config.anchoCinta
        self.altoCinta = config.altoCinta
        self.colorCinta = COLORES["naranja"]

        self.sepEntrePaqs = (config.anchoCinta + self.ancho / 2) / self.longitudX
        self.sepEntreCintas = config.sepEntreCintas

        # -- Animación del paquete borrándose --
        # Guarda la posicion (x, y) del paquete
        self.paqBorrandose = []
        self.inicioAnimacion = time.time()
        self.tiempoVisible = 0.2
        self.tiemoInvisible = 0.15
        self.totalAnimacion = 2
        # Guarda la posicion x del paquete en la cinta 0
        # Mismos tiempos de animación que el resto de paquetes
        self.paqBorrandose0 = None

        # Creamos la matriz con los paquetes
        self.matriz = self.crearMatriz(longitudX, longitudY)
        # Creamos la lista de 1D con los paquetes de la cinta 0
        # REFACTOR? 9 posiciones usadas, mas 9 por si hay paquetes cerca de los personajes
        self.len_cinta0 = longitudX
        self.cinta0_x = 220  # 220
        self.crearlista0()

        #horno
        self.fuego1 = 0
        self.fuego2 = 0
        self.fuego3 = 0

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
        # Comprueba indices donde hay unos y los mueve hacia la izquierda
        for i in range(1, self.len_cinta0):
            if self.lista0[i] != 0:
                self.lista0[i] = 0
                self.lista0[i - 1] = 1
        # for i in range(1, int(self.len_cinta0 / 2)):
        #     if self.lista0[i] != 0:
        #         self.lista0[i] = 0
        #         self.lista0[i - 1] = 1
        # # Para los paquetes más lejanos, solo los actualiza si no hay paquetes cerca
        # if not self.__paqueteCercaDcha(distancia=1)[0]:
        #     for i in range(int(self.len_cinta0 / 2), self.len_cinta0):
        #         if self.lista0[i] != 0:
        #             self.lista0[i] = 0
        #             self.lista0[i - 1] = 1
        # else:
        #     print("No actualizamos, paquetes cerca personajes:",
        #           self.__paqueteCercaDcha(distancia=1))
        #     txt = ""
        #     for i in range(len(self.matriz)):
        #         txt += str(self.matriz[i])
        #         if i == self.__paqueteCercaDcha(distancia=1)[1]:
        #             txt += " <---"
        #         txt += "\n"
        #     print(txt)
        # # print(self.lista0)

    # Actualiza los paquetes del grupo de cintas seleccionado
    def actualizarPaquetes(self, grupo):
        # self.__paquetesSincronizados()
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

        # Busca los paquetes dentro de la matriz y los mueve a su siguiente posición
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
            valorActual = fila[x]
            fila[x] = 0
            fila[x + 1] = valorActual
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
        self.matriz[0][5] = 1
        #self.lista0[-1] = 1
        # # print("cerca", self.__paqueteCercaPersonaje())
        # if not self.__paqueteCercaDcha(distancia=int(self.len_cinta0 / 2))[0]:
        # #     self.lista0[9] = 1
        # # else:
        #     # print("SE AÑADE MÁS LEJOS")
        #     self.lista0[-1] = 1
        # else:
        #     print("No se añade paquete, hay uno cerca del borde")

    def __dibujarPaq(self, x, y, nivelPaquete=1):
        # Dibujamos el paquete básico
        pyxel.rect(x, y, self.ancho, self.alto, self.color)

        # Si está en otro nivel, dibujamos las botellas
        if nivelPaquete == 2:
            for i in range(0, int(self.ancho / 2), 2):
                pyxel.pset(x + i, y - 1, self.color)
        elif nivelPaquete == 3:
            for i in range(0, self.ancho, 2):
                pyxel.pset(x + i, y - 1, self.color)
        elif nivelPaquete == 4:
            for i in range(0, self.ancho, 2):
                pyxel.pset(x + i, y - 1, self.color)
                if i + 1 < self.ancho:
                    pyxel.pset(x + i + 1, y - 2, self.color)
        elif nivelPaquete == 5:
            # Forma de paquete
            w = int(self.ancho * 0.2)
            h = int(self.alto * 0.4)
            pyxel.rect(x, y + h, self.ancho, 1, COLORES["blanco"])
        elif nivelPaquete >= 6:
            # Dibujamos el paquete nivel 5
            w = int(self.ancho * 0.2)
            h = int(self.alto * 0.4)
            pyxel.rect(x, y + h, self.ancho, 1, COLORES["blanco"])
            # Y otra linea para completar el 'lazo'
            pyxel.rect(x + w, y, 1, self.alto, COLORES["blanco"])

    def draw(self):
        # -- Dibujamos la cinta 0 de paquetes --
        # Dibujamos los paquetes de la cinta 0
        x = self.cinta0_x
        # La lista 0 debe estar a la altura de la última cinta de paquetes
        y = self.posY + (self.longitudY - 1) * self.sepEntreCintas
        for i in range(len(self.lista0)):
            paq = self.lista0[i]
            if paq != 0:
                # pyxel.rect(x - 5, y - self.alto, self.ancho, self.alto, self.color)
                self.__dibujarPaq(x - 5, y - self.alto)
            x += self.sepEntrePaqs

        # Dibujamos los elementos visuales de la cinta 0
        pyxel.rect(self.cinta0_x, y, 200, self.altoCinta, self.colorCinta)
        pyxel.rect(self.cinta0_x + 5, y, 40, 1, COLORES["gris"])
        pyxel.rect(self.cinta0_x - 25, y + 3, 25, 1, COLORES["marron"])
     #   pyxel.rect(self.cinta0_x - 18, y -70, 1, 75, COLORES["azul"])
     #   pyxel.rect(self.cinta0_x - 5, y - 70, 1, 75, COLORES["azul"])
        pyxel.rect(self.cinta0_x - 18, y , 16, 3, COLORES["marron"])
        pyxel.rect(self.cinta0_x - 16, y, 12, 2, COLORES["morado"])

        #Fuego del horno
        if pyxel.frame_count % 1 == 0:  # Para no dañar epilepticos (cambia de color cada 3 frames)
            self.fuego1 = random.randint(0, 9)
            self.fuego2 = random.randint(0, 9)
            self.fuego3 = random.randint(0, 9)
            z = 30
            w = -8
            pyxel.rect(self.cinta0_x -3 + z, y - 3 + w, 9, 11, COLORES["negro"])
            pyxel.rect(self.cinta0_x -1 + z, y - 1+ w, 5, 7, COLORES["gris"])
            pyxel.rect(self.cinta0_x +z, y +w, 3, 5, random.randint(8, 10))
            pyxel.text(self.cinta0_x +z, y +w, f"{self.fuego1}", random.randint(8, 10))# del 8 al 10 son el naranja, amarillo y rojo
            pyxel.text(self.cinta0_x +z, y +w, f"{self.fuego2}", random.randint(8, 10))
            pyxel.text(self.cinta0_x +z, y +w, f"{self.fuego3}", random.randint(8, 10))
            #chimenea
            pyxel.rect(self.cinta0_x + z, y - 10 + w, 3, 7, COLORES["gris"])
            pyxel.rect(self.cinta0_x + z, y - 10 + w, 7, 3, COLORES["gris"])
            pyxel.rect(self.cinta0_x + 4 + z, y - 10 + w, 1, 3, COLORES["azulMarino"])
            pyxel.rect(self.cinta0_x + z, y - 6 + w, 3, 1, COLORES["azulMarino"])


        # -- Dibujamos las cintas --
        y = self.posY
        for j in range(self.longitudY):
            pyxel.rect(self.posX, y, self.anchoCinta,
                       self.altoCinta, self.colorCinta)
            pyxel.rect(self.posX + 5, y, self.anchoCinta - 10,
                       self.altoCinta - 3, COLORES["gris"])
            # Dibujamos las plataformas donde se apoyan los personajes REFACTOR, usar método self.__dibujarPlataforma()
            if j % 2 == 0 and j != 0:
                pyxel.rect(self.posX - 18, y + 3, self.anchoCinta -
                       122, self.altoCinta - 3, COLORES["marron"])
                pyxel.rect(self.cinta0_x - 178, y, 16, 3, COLORES["marron"])
                pyxel.rect(self.cinta0_x - 176, y, 12, 2, COLORES["azul12"])

            if j == 0:
                pyxel.rect(self.posX - 18, y + 3, self.anchoCinta -
                           122, self.altoCinta - 3, COLORES["marron"])
                pyxel.rect(self.cinta0_x - 178, y, 16, 3, COLORES["marron"])
                pyxel.rect(self.cinta0_x - 176, y, 12, 2, COLORES["morado"])

            if j % 2 == 1:
                pyxel.rect(self.posX + 140, y + 3, self.anchoCinta -
                       122, self.altoCinta - 3, COLORES["marron"])
                pyxel.rect(self.cinta0_x - 18, y, 16, 3, COLORES["marron"])
                pyxel.rect(self.cinta0_x - 16, y, 12, 2, COLORES["azul12"])

            #Soporte plataformas de castigo
            pyxel.rect(0, 117, 33, 2, COLORES["marron"])
            pyxel.rect(225, 77, 33, 2, COLORES["marron"])
            pyxel.rect(253, 0, 3, 78, COLORES["marron"])
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
                    self.__dibujarPaq(x, y - self.alto, self.matriz[j][i])
                # Pasamos a dibujar el siguiente paquete (de arriba a abajo, el inferior)
                y += self.sepEntreCintas
            # Después de recorrer toda la columna, pasar a la siguiente (de izquiera a derecha)
            x += self.sepEntrePaqs

        # Dibujamos los paquetes borrándose
        if len(self.paqBorrandose) > 0:
            self.__animacionPaqMatriz()
        # Si es distinto de None
        if self.paqBorrandose0 != None:
            self.__animacionPaqCinta0()

    # REFACTOR: fusionar con cinta0
    def __animacionPaqMatriz(self):
        i, j = self.paqBorrandose[0], self.paqBorrandose[1]
        x = self.posX + i * self.sepEntrePaqs
        y = self.posY + j * self.sepEntreCintas - self.altoCinta

        tiempoTranscurrido = time.time() - self.inicioAnimacion
        if tiempoTranscurrido < self.totalAnimacion:
            t = tiempoTranscurrido % (self.tiemoInvisible + self.tiempoVisible)
            if t < self.tiempoVisible:
                self.__dibujarPaq(x, y, self.numCintas - j)
                # print("borrandose", i, j, "-->", self.numCintas - j)
        else:
            # Se acaba la animación
            self.paqBorrandose = []
    
    def __animacionPaqCinta0(self):
        j = self.paqBorrandose0
        x = self.cinta0_x
        y = self.posY + (self.numCintas - 1) * self.sepEntreCintas - self.altoCinta

        tiempoTranscurrido = time.time() - self.inicioAnimacion
        if tiempoTranscurrido < self.totalAnimacion:
            t = tiempoTranscurrido % (self.tiemoInvisible + self.tiempoVisible)
            if t < self.tiempoVisible:
                self.__dibujarPaq(x, y)
        else:
            # Se acaba la animación
            self.paqBorrandose0 = None


    def __paqsEnJuego(self):
        # Cuenta cuantos paquetes hay actualmente en juego (no tiene en cuenta la última fila, ya que ese paquete va a desaparecer pronto)
        sum = 0
        for y in range(self.longitudY - 1):
            for x in range(self.longitudX):
                if self.matriz[y][x] != 0:
                    sum += 1
        return sum

    # Comprueba si hay algun paquete a menos de 'distancia' distancia de los personajes cuando ocurre un fallo
    # Devuelve la posición del paquete en forma de tupla (equivalente a True) o False REFACTOR -> Solo para DEBUG?
    def __paqueteCercaPersonaje(self, distancia=8):  # 2
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

    def __paqueteCercaDcha(self, distancia=3):  # 2
        # Comprobamos por la derecha
        for j in range(self.longitudY):
            for i in range(self.longitudX - distancia, self.longitudX):
                if self.matriz[j][i] != 0:
                    # print(i, j, "Paquete cerca borde dcho")
                    return (i, j)
            for i in range(distancia):
                if self.matriz[j][i] != 0:
                    # print(i, j, "Paquete cerca borde dcho")
                    return (i, j)

        # Si no, devuelve falso (en forma de tupla para seguir con el formato)
        return (False, False)

    # Comprueba si la distancia horizontal entre 2 paquetes en el borde es menor o igual que 'distEntrePaqs'

    def __paquetesSincronizados(self, distEntrePaqs=3):
        # Comprueba y elimina paquetes sincronizados cerca del borde
        # Comprobamos por la izquierda
        distAlBorde = 2
        paqX, paqY = self.__paqueteCercaPersonaje(distAlBorde)
        if paqX and paqY:
            # Izquierda
            for j in range(self.longitudY):
                for i in range(distAlBorde - distEntrePaqs, distEntrePaqs):
                    if self.matriz[j][i] != 0:
                        contadorPaquetesBorde += 1
            # Si hay varios paquetes en el borde, borramos todos
            if contadorPaquetesBorde >= 2:
                for j in range(self.longitudY):
                    self.matriz[j][0] = 0
                print("paquete sincronizado, eliminados todos izda")
                print("Por que solo izda???")

        contadorPaquetesBorde = 0
        for j in range(self.longitudY):
            for i in range(0, distEntrePaqs):
                if self.matriz[j][i] != 0:
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
        d = 3
        i, j = self.__paqueteCercaPersonaje(d)
        print("Paquetes borde:", i, j)
        if i != None and j != None:
            # Si 'i' y 'j' están definidas -> Hay que quitar un paquete de la matriz
            distDcha = i
            distIzda = self.longitudX - i
            # Eliminamos si está en el borde izquierdo en las cintas pares
            if esCintaPar(j, self.numCintas) and distDcha >= distIzda:
                print("Borrándose izda (par)", i, j)
                # Reproducimos la animacion y borramos el paquete
                self.animar(i, j)
                self.matriz[j][i] = 0
            elif not esCintaPar(j, self.numCintas) and distDcha <= distIzda:
                print("Borrándose dcha (impar)", i, j)
                # Reproducimos la animacion y borramos el paquete
                self.animar(i, j)
                self.matriz[j][i] = 0
            else:
                print("Paquete NO se borra", i, j)
        elif j == None and i != None:
            # Si 'j' no está definida pero 'i' sí -> Es la cinta 0
            print(i, "Paquete BORRÁNDOSE, cinta 0")
            # Reproducimos la animacion y borramos el paquete
            self.lista0[i] = 0
            self.animar(i)
            

    def animar(self, x, y=None):
        if y != None:
            self.paqBorrandose = [x, y]
        else:
            self.paqBorrandose0 = x
        self.inicioAnimacion = time.time()


    def __str__(self):
        txt = ""
        for fila in self.matriz:
            txt += str(fila) + "\n"
        return txt

    def __repr__(self):
        return f"Paquete(longitudX={self.longitudX}, longitudY={self.longitudY}, matrizPaquetes={self.matriz})"
