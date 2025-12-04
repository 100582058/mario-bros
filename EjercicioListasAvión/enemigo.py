# -*- coding: utf-8 -*-
"""
Created on Sunday Nov 14 11:59:42 2021

@author: Ana Blanco Benito
@version: 1.0

Módulo con la clase Enemigo
"""
'''Esta clase representa un enemigo'''
'''Hya que repensarla cuando trabajéis la herencia'''
"""Aunque no se han implementado las property y los setters en este 
 ejemplo, sí deberéis hacerlo para el proyecto"""
import constantes
class Enemigo:

    def __init__(self, x: int, y: int, tipo: str):
        ''' Método init, crea los atributos iniciales del bloque'''
        self.x = x
        self.y = y
        self.tipo = tipo

        # Para el sprite leemos los datos del módulo de constantes, será una
        # tupla compuesta por (banco,x,y,ancho,alto)
        if self.tipo=="ROJO":
            self.sprite = constantes.SPRITE_ROJO
        elif self.tipo=="REGULAR":
            self.sprite = constantes.SPRITE_REGULAR
        elif self.tipo == "BOMBARDERO":
            self.sprite = constantes.SPRITE_BOMBARDERO
        elif self.tipo == "SUPERBOMBARDERO":
            self.sprite = constantes.SPRITE_SUPERBOMBARDERO
