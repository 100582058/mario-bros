# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 20:31:32 2019

@author: Angel Garcia Olaya PLG-UC3M
@Author: Traducido al español por Ana Blanco Benito
@version: 1.0
Este programa mueve objetos en pyxel
"""

import pyxel

# Creamos una lista con las coordenadas que usaremos dentro de las funciones
# Es un modo de cambiar las posiciones en update() y draw()
position = [10, 10]


def move(x, y):
    ''' Esta fucnión comprueba si se presionan las teclas de las flechas y
     actualiza las coordenads x e y de acuerdo con ello'''
    # Puedes ver todas las teclas en:
    # https://github.com/kitao/pyxel/blob/master/pyxel/__init__.py
    # Si las teclas se presionan se actualizan las teclas
    if pyxel.btn(pyxel.KEY_RIGHT):
        x = x + 1
    elif pyxel.btn(pyxel.KEY_LEFT):
        x = x - 1
    elif pyxel.btn(pyxel.KEY_UP):
        y = y - 1
    elif pyxel.btn(pyxel.KEY_DOWN):
        y = y + 1

    return x, y


# Para usar pyxel necesitamos definir dos funciones, una hará todos
# los cálculos necesarios para cada frame, y la otra pintará los objetos en
# la pantalla. Pueden tener cualquier nombre, pero lo estándar es update and
# draw
def update():
    ''' Esta función se ejecuta cada frame. Llama a la función move
     que actualiza la x e y del círculo'''
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    else:
        position[0], position[1] = move(position[0], position[1])


def draw():
    ''' Esta función dibuja figuras geométricas cada turno.'''
    # Fijamos el color de fondo, cualquier cosa que haya en la pantalla se
    # borra. Puedes mirar la documentación de pyxel para ver los colores
    # disponibles (16). El 0 es el negro.
    global x, y
    pyxel.cls(1)
    pyxel.circ(position[0], position[1], 10, 10)


################## main program ##################

# Creamos constantes, así es más fácil modificar valores
# El máximo ancho y alto son 256
WIDTH = 160
HEIGHT = 120
CAPTION = "Este es un ejemplo para mover cosas en pyxel"

# Lo primero que hay que hacer es crear la pantalla, puedes ver la API de
# pyxel si deseas ver más parámetros
pyxel.init(WIDTH, HEIGHT, title=CAPTION)
# Para iniciar el juego invocamos el método run con las funciones update y draw
pyxel.run(update, draw)
