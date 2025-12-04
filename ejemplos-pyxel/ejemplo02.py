# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 20:05:18 2019

@author: Angel Garcia Olaya PLG-UC3M
@author: Traducido al español por Ana Blanco Benito
@version: 1.1
Muestra cómo dibujar figuras en pyxel
"""
import pyxel

# Para usar pyxel necesitamos definir dos funciones, una hará todos
# los cálculos necesarios para cada frame, y la otra pintará los objetos en
# la pantalla. Pueden tener cualquier nombre, pero lo estándar es update and
# draw


def update():
    ''' Esta función se ejecuta cada frame. Ahora solo comprueba si
    la tecla Escape o Q se presionan para finalizar el programa'''
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()


def draw():
    ''' Esta función dibuja figuras geométricas cada turno.'''
    # Fijamos el color de fondo, cualquier cosa que haya en la pantalla se
    # borra. Puedes mirar la documentación de pyxel para ver los colores
    # disponibles (16). El 0 es el negro.
    pyxel.cls(1)
    # Para dibujar una línea: .line(x1: int, y1: int, x2: int, y2: int, color:
    # int)
    pyxel.line(0, 0, 20, 20, 3)
    # Para dibujar un rectángulo: .rect(x: int, y: int, w: int, h: int,
    # col: int)
    pyxel.rect(20, 20, 10, 30, 4)
    # Para el "marco" de un rectángulo
    pyxel.rectb(30, 50, 20, 10, 5)
    # Para un círculo  circ(x: int, y: int, r: int, col: int)
    pyxel.circ(50, 80, 10, 6)
    # Par el "marco" de un círculo
    pyxel.circb(100, 30, 15, 7)
    # Para un pyxel pset(x: int, y: int, col: int)
    pyxel.pset(120, 100, 8)

    # Rectángulo hecho con píxeles
    x, y, w, h = 20 + pyxel.frame_count % pyxel.width, 150, 50, 5
    for x_pos in range(w):
        for y_pos in range(h):
            pyxel.pset(x + x_pos, y + y_pos, 2)
        


################## main program ##################

# Creamos constantes, así es más fácil modificar valores
# El máximo ancho y alto son 256
WIDTH = 160
HEIGHT = 120
CAPTION = "Este es un ejemplo para dibujar figuras en pyxel"

# Lo primero que hay que hacer es crear la pantalla, puedes ver la API de
# pyxel si deseas ver más parámetros
pyxel.init(WIDTH, HEIGHT, title=CAPTION)

# Para iniciar el juego invocamos el método run con las funciones update y draw
pyxel.run(update, draw)
