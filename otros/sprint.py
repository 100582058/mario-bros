"""Sprint 1.A: Objetos e interfaz gráfica (13/11)
● Crear una clase para cada elemento principal del juego: Personajes, Cinta, Camión,
Paquete, etc
● Toda la lógica de comportamiento de cada entidad debe estar contenida en su clase
correspondiente. Se debe evitar incluir lógica del juego en el programa principal"""
# Para controlar el !movimiento de Personaje
import pyxel

class Personaje:
    def __init__(self, id, controles, posX, posY):
        self.id = id # Nombre del Personaje
        self.controles = controles # Tupla con 2 strings para las teclas
        self.posicion = [posX, posY] #x no varía una vez asignado
        self.planta = 0 # ?Planta en la que se encuentra



    @property
    def controles(self):
        return self.__controles

    @controles.setter
    def controles(self, valor):
        self.__controles = valor

    @property
    def posicion(self):
        return self.__posicion

    @posicion.setter
    def posicion(self, valor):
        self.__posicion = valor

    def mover(self):
        # self.controles[0] controla el movimiento de subida
        # self.controles[1] el de bajada
        if pyxel.btnp(self.controles[0]):
            # Mover hacia arriba si no está en la más alta
            if self.planta < NUM_CINTAS:
                self.planta += 1
        if pyxel.btnp(self.controles[1]):
            # Mover hacia abajo si no está en la inferior
            if self.planta > 0:
                self.planta -= 1

    def draw(self):
        col = 11
        if self.id.lower() == "mario":
            col = 8
        pyxel.rect(self.posicion[0], self.posicion[1], 10, 10, col)

    def __repr__(self):
        return f"Personaje(controles={self.controles}, posicion={self.posicion})"

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
            print("="*10, "Paquete en la última altura/cinta", "="*10)

    # DEBUG
    def __str__(self):
        txt = "\n"
        for fila in self.matrizPaquetes:
            txt += str(fila) + "\n"
        return txt

    def __repr__(self):
        return f"Paquete(longitudX={self.longitudX}, longitudY={self.longitudY}, matrizPaquetes={self.matrizPaquetes})"

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

class Fabrica:
    def __init__(self, tiempo, vidas):
        self.vidas = vidas # Cambian en función de la dificultad
        self.tiempo = tiempo # tiempo del nivel
        # self.dificultad = dificultad # 3 tipos

    @property
    def vidas(self):
        return self.__vidas

    @vidas.setter
    def vidas(self, valor):
        self.__vidas = valor

    @property
    def tiempo(self):
        return self.__tiempo

    @tiempo.setter
    def tiempo(self, valor):
        self.__tiempo = valor

    @property
    def dificultad(self):
        return self.__dificultad

    @dificultad.setter
    def dificultad(self, valor):
        self.__dificultad = valor

    def __repr__(self):
        return f"Fabrica(vidas={self.vidas}, tiempo={self.tiempo}, dificultad={self.dificultad}"

# Las posiciones en las que puede estar un paquete en la cinta (columnas de la matriz)
POSICIONES_PAQUETE_CINTA = 8
DIFICULTAD = "facil"
NUM_CINTAS = 5 # Depende de la dificultad
# NUM_CINTAS = asignarValores(DIFICULTAD)

# Variables de test
# mario = Personaje("mario", (pyxel.KEY_UP, pyxel.KEY_DOWN), 10, 20)
# print(repr(mario))
# camion = Camion(20, 30)
# print(repr(camion))
# paquetes = Paquetes(POSCIONES_PAQUETES_CINTA, NUM_CINTAS)
# print(repr(paquetes), "\n")
# # Añade un paquete en la posición inicial
# paquetes.anadirPaquete()
# paquetes.actualizarPaquetes()

# mario.reganado()