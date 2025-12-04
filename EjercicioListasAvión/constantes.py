# -*- coding: utf-8 -*-
"""
Módulo que agrupa las constantes que se van a usar en el juego. Generalmente
es conveniente tener todas las constantes agrupadas en un sitio por si hay que
hacer cambios en ellas.
"""
ANCHO = 224
ALTO = 256

#Avión
AVION_INICIAL = (ANCHO/2, 200)
AVION_SPRITE = (1, 0, 0, 25, 16)

#Enemigos
SPRITE_REGULAR = (0, 16, 0, 16, 16)
SPRITE_ROJO = (0, 32, 0, 16, 16)
SPRITE_SUPERBOMBARDERO = (0, 48, 0, 16, 16)
SPRITE_BOMBARDERO = (0, 0, 16, 16, 16)
ENEMIGOS_INICIAL= ((20, 0, "REGULAR"), (50, 0, "ROJO"),
                    (100, 0, "SUPERBOMBARDERO"), (200, 0, "BOMBARDERO"),
                    (100, 80, "BOMBARDERO"),(100,  20, "ROJO"))
