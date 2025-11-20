"""Crear las clases para representar los objetos necesarios para el proyecto final. Para todos ellos
crear métodos init, propiedades y setters necesarios."""

# Hay parámetros que serán asignados según la dificultad de juego elegida
num_cintas = 5
# Valor fijo: Número de posiciones en las que puede estar un paquete
posiciones_cinta = 8

# TO-DO: Añadir métodos especiales: __str__ y/o __repr__

# Añadir contador de puntos y fallos en el camión? En la máquina? O en main()?
# Hace falta añadir propiedades y setters a atributos asignados en innit?
# Hacen falta setters para valores no mutables? Hace falta validar/comprobar errores?
# Deberían ser atributos privados?
# Valores fijos en mayúsculas como constantes?


class Personaje:
    def __init__(self, controles):
        # Valor fijo: Asignamos controles (tupla con las teclas que se deben pulsar para cambiar de piso)
        self.controles = controles
        # Posición/Piso actual del personaje
        self.posicion = [x, y]

    @property
    def posicion(self):
        return self.__posicion
    
    @posicion.setter
    def posicion(self, valor):
        if not isinstance(valor, int):
            raise TypeError("La posición debe ser un entero")
        elif valor < 0 or valor > num_cintas:
            raise ValueError(f"La posición debe estar entre 0 y {num_cintas}")
        self.__posicion = valor
        
    @property
    def controles(self):
        return self.__controles
    
    # Necesario para validar el parámetro inicial
    @controles.setter
    def controles(self, valor):
        if not isinstance(valor, tuple):
            raise TypeError("Los controles deben ser asignados como una tupla")
        elif len(valor) != 2:
            raise ValueError("Se debe introducir una tupla con 2 valores")
        self.__controles = valor


class Cinta:
    def __init__(self, indice, dificultad):
        self.indice = indice
        self.vel_cinta = self.asignar_valores(dificultad)

    @property
    def indice(self):
        return self.__indice
    
    @indice.setter
    def indice(self, valor):
        if not isinstance(valor, int):
            raise TypeError("El índice debe ser un entero")
        elif valor < 0 or valor > num_cintas:
            raise ValueError(f"El índice debe estar entre 0 y {num_cintas}")
        self.__indice = valor

class Camion:
    def __init__(self):
        # Valores fijos
        self.paquetes_almacenados = 0
        self.capacidad_max = 8
        # Cambia entre repartiendo (descanso) o no
        self.repartiendo = False

    @property
    def repartiendo(self):
        return self.__repartiendo
    
    @repartiendo.setter
    def repartiendo(self, valor):
        if not isinstance(valor, bool):
            raise TypeError("El valor de repartiendo debe ser un booleano")
        self.__repartiendo = valor

class Paquete:
    def __init__(self):
        # Indice de la cinta en la que se encuentra
        self.cinta = 0
        # Posición dentro de la cinta
        self.pos = 0

    @property
    def cinta(self):
        return self.__cinta

    @cinta.setter
    def cinta(self, valor):
        if not isinstance(valor, int):
            raise TypeError("El número de la cinta debe ser un entero")
        elif valor < 0 or valor > num_cintas:
            raise ValueError(f"El número debe estar entre 0 y {num_cintas}")
        self.__cinta = valor

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, valor):
        if not isinstance(valor, int):
            raise TypeError("La posición en la cinta debe ser un entero")
        elif valor < 0 or valor > num_cintas:
            raise ValueError(
                f"La posición en la cinta debe estar entre 0 y {posiciones_cinta}"
            )
        self.__pos = valor


# Máquina encargada de fabricar los paquetes
class Maquina:
    def __init__(self, incremento_paqs_mins):
        # Número de paquetes actualmente en juego. Empieza en cero
        self.paquetes_en_juego = 0
        # Indica el número de paquetes que debe haber como mínimo en juego
        self.paquetes_mininmos = 1
        # Puntos necesarios para incrementar el número de paquetes que debe haber como mínimo
        self.puntos_min = incremento_paqs_mins

    @property
    def puntos_min(self):
        return self.__puntos_min

    @puntos_min.setter
    def puntos_min(self, valor):
        if not isinstance(valor, int):
            raise TypeError("El número de puntos necesarios para incrementar el mínimo de paquetes debe ser un entero")
        elif valor < 0:
            raise ValueError(
                "número de puntos necesarios para incrementar el mínimo de paquetes debe ser mayor que cero"
            )
        self.__puntos_min
