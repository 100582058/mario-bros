# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 12:48:02 2019

@author: Angel Garcia Olaya PLG-UC3M
@author: Traducido al español por Ana Blanco Benito
@version: 1.0
Example of using graphics in pyxel
"""

import pyxel


# Para usar pyxel necesitamos definir dos funciones, una hará todos
# los cálculos necesarios para cada frame , y la otra pintará los objetos en
# la pantalla. Pueden tener cualquier nombre, pero lo estándar es update and
# draw
def update():
    ''' Esta función se ejecuta cada frame. Ahora solo comprueba si
    la tecla Escape o Q se presionan para finalizar el programa'''
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()


def draw():
    ''' Esta función dibuja gráficos del banco de imágenes'''
    pyxel.cls(3)
    # Carga las imágenes del banco de imágenes 0
    # Pone una imagen de gato en la mitad de la pantalla
    pyxel.blt(WIDTH // 2, HEIGHT // 2, 0, 0, 0, 16, 16)
    # Dibuja una nave espacial
    pyxel.blt(25, 20, 1, 17, 0, 16, 16)
    # Dibuja una nave espacial, podemos usar un parámetro adicional para
    # especificar cuál es el color de fondo de la imagen (nota la diferencia
    # con la previa)
    pyxel.blt(55, 20, 1, 17, 0, 16, 16, colkey=0)


################## main program ##################

# Creamos constantes, así es más fácil modificar valores
# El máximo ancho y alto son 256
WIDTH = 160
HEIGHT = 120
CAPTION = "Este es un ejemplo de imágenes en pyxel"

# Lo primero que hay que hacer es crear la pantalla, puedes ver la API de
# pyxel si deseas ver más parámetros
pyxel.init(WIDTH, HEIGHT, title=CAPTION)
# Cargamos el fichero de la imagen, es un gato de 16x16 en el punto (0,
# 0) en el banco 0
pyxel.load("assets/example.pyxres")
# Cargamos una nave espacial de 16x16 en banco 1 en el punto (17,0)
pyxel.image(1).load(17, 0, "assets/player.png")
# Para iniciar el juego invocamos el método run con las funciones update y draw
pyxel.run(update, draw)
