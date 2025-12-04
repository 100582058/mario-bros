import constantes
from avion import Avion
from enemigo import Enemigo

import pyxel

class Tablero:
    """Esta clase contiene la información neceraria para
    representar el tablero"""
    """Aunque no se han implementado las property y los setters en este 
    ejemplo, sí deberéis hacerlo para el proyecto"""

    def __init__(self, ancho: int, alto: int):
        """ Estos parámetros son el ancho y el alto del tablero"""

        # Initializamos el objeto
        self.ancho = ancho
        self.alto = alto

        # Este bloque inicializa pyxel
        # Lo primero que tenemos que hacer es crear la pantalla, ver la API
        # para más parámetros
        pyxel.init(self.ancho, self.alto, title="1942")

        # Cargamos el fichero pyxres que vamos a usar
        pyxel.load("assets/example.pyxres")
        pyxel.image(1).load(0, 0, "assets/avion.png")


        # Creamos un avión en la mitad de la pantalla en x. En y estará en la
        # posición 200
        # Notad que la imagen indicada en el init de la clase avión (en el
        # sprite), en este ejemplo es un gato
        self.avion = Avion(*constantes.AVION_INICIAL)

        self.enemigos = []
        for element in constantes.ENEMIGOS_INICIAL:
            self.enemigos.append(Enemigo(*element))

        # Ejecutamos el juego
        pyxel.run(self.update, self.draw)

    def update(self):
        """Este código se ejecuta cada frame, aquí invocamos
        los métodos que se actualizan los  diferentes objetos"""
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # Solo hacemos el movimiento horizontal del avión
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.avion.mover('derecha', self.ancho)
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.avion.mover('izquierda', self.ancho)

    def __pintarAvion(self):
        pyxel.blt(self.avion.x, self.avion.y, *self.avion.sprite, colkey=0)

    def __pintarEnemigos(self):
        for element in self.enemigos:
            pyxel.blt(element.x, element.y, *element.sprite, colkey=0)


    def draw(self):
        """Este código se ejecuta también cada frame, aquí deberías dibujar los
        objetos
        """
        pyxel.cls(0)

        """Dibujamos el avión tomando los valores del objeto avión
        Los parámetros son x, y en la pantalla  y una tupla que contiene: 
        el número del banco de imágenes, la x e y de la imagen en el banco 
        y el tamaño de la imagen"""
        self.__pintarAvion()
        self.__pintarEnemigos()


