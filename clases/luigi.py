from clases.personaje import Personaje

class Luigi(Personaje):
    def __init__(self, id_personaje, posX, posY, color, controles):
        super().__init__(id_personaje, posX, posY, color, controles)

    def mover(self):
        super().mover()

    def estaEnPiso(self):
        pass

    def draw(self):
        super().draw()
