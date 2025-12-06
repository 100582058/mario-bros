from clases.personaje import Personaje

class Luigi(Personaje):
    def __init__(self, id_personaje, posX, posY, ancho, alto, color, controles, config):
        super().__init__(id_personaje, posX, posY, ancho, alto, color, controles, config)

    def mover(self):
        super().mover()

    def estaEnPiso(self):
        pass

    def draw(self):
        super().draw()
