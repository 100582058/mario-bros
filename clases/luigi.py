from clases.personaje import Personaje

class Luigi(Personaje):
    def __init__(self, id_personaje, posX, posY, ancho, alto, color, controles, config):
        super().__init__(id_personaje, posX, posY, ancho, alto, color, controles, "pares", config)

    def mover(self):
        super().mover()

    def intentarCambiarPlanta(self, direccion):
            # Los personajes solo están en la cinta 0
            # o en las pares (Luigi) o impares (Mario)
        cinta = (self.numCintas - 1) - self.planta
        print("Pares (Luigi)", self.planta, cinta, direccion)
        # if cinta == 0 and direccion == "arriba":
        #     self.subir(2)
        # elif cinta == 2 and direccion == "abajo":
        #     self.bajar(2)
        # elif cinta >= 1:
        # En el resto de plantas, se mueve de 2 en 2
        if direccion == "arriba" and cinta + 2 <= self.numCintas - 1:
            self.subir(2)
        elif direccion == "abajo" and cinta - 2 >= 0:
            self.bajar(2)
        print("Nueva:", self.planta, cinta)

    def estaEnPiso(self):
        pass

    def draw(self):
        super().draw()
