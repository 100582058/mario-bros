# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 16:39:31 2019

@author: Angel Garcia Olaya PLG-UC3M
@author: Traducido al español por Ana Blanco Benito
@version: 1.1
Ejemplo sencillo de uso de pyxel. Muestra como escribir texto, como cambiar su
color y como moverlo
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
    ''' Esta función pone objetos en la pantalla en cada turno. En este
    momento texto'''
    # Fijamos el color de fondo, cualquier cosa que haya en la pantalla se
    # borra. Puedes mirar la documentación de pyxel para ver los colores
    # disponibles (16). El 0 es el negro.
    pyxel.cls(0)
    # con .text(x:int,y:int,text:str,color:int) dibujamos un texto en la
    # pantalla
    pyxel.text(0, 0, "Hola, bienvenidos a pyxel", 2)
    # usamos pyxel.frame_count para realizar acciones cada frame (aquí
    # cambiamos de color)
    pyxel.text(0, 10, "Cambio de color cada frame", pyxel.frame_count % 16)
    # esto se hace cada frame... mover un texto hasta que llega el final.
    # Podemos conocer el ancho y el alto de la pantalla usando pyxel.width o
    # pyxel.height
    x = pyxel.frame_count % pyxel.width
    pyxel.text(x, 20, "Moviendo el texto", 3)



################## main program ##################


# Creamos constantes, así es más fácil modificar valores
# El máximo ancho y alto son 256
WIDTH = 256
HEIGHT = 256
CAPTION = "Este es el primer ejemplo de pyxel"

# Lo primero que hay que hacer es crear la pantalla, puedes ver la API de
# pyxel si deseas ver más parámetros
pyxel.init(WIDTH, HEIGHT, title=CAPTION)

# Para iniciar el juego invocamos el método run con las funciones update y draw
pyxel.run(update, draw)
