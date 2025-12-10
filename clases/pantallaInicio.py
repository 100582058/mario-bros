import pyxel
import random
from utils.config import COLORES

class PantallaInicio:
    def __init__(self):
        self.opciones = ["Facil", "Normal", "Dificil", "Crazy"]
        self.colores = {
            "Facil": COLORES["azulCeleste"],
            "Normal": COLORES["amarillo"],
            "Dificil": COLORES["naranja"],
            "Crazy": COLORES["magenta"]
}
        self.seleccion = 0
        self.activa = True
        self.cancionJuego = True
        self.dificultadSeleccionada = None
        self.timerUp = 0
        self.timerDown = 0
        self.comparador = 4 #Esto hace variar cuan rapido se activa el btn (que es para mantener el botón presionado)
                            #Tócalo para cambiar los fps del Btn (por debajo de 3 el jugador pierde precisión)(5 está bien)
        self.parpadeoCol = 1
        self.conpCancion = 0
        self.contadorMusica = 0

    def btnCheck(self):
        if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
            self.timerDown += 1
            if self.timerDown > self.comparador:
                self.timerDown = 0 #Aqui lo reinicia
                return 1
        elif pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP):
            self.timerUp += 1
            if self.timerUp > self.comparador:
                self.timerUp = 0
                return 2
        else:
            self.timerDown = 0

        if self.activa == True and self.conpCancion == 0:
            self.conpCancion += 1
            pyxel.playm(2, loop=True)
        # Si no devuelve 1 o 2
        return -1

    def update(self):
        # Mute a la M




        #seleccion por flechas y wasd

        if pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.KEY_DOWN):
            if self.seleccion != 3:
                self.seleccion += 1
            else:
                self.seleccion = 0 # El mínimo
            self.timerDown = 0

        elif pyxel.btnp(pyxel.KEY_W) or pyxel.btnp(pyxel.KEY_UP):
            if self.seleccion != 0:
                self.seleccion -= 1
            else:
                self.seleccion = 3 # El máximo
            self.timerUp = 0

        else:
            # para que no halla problemas al llamar varias veces a la funcion en un solo frame
            unoOdos = self.btnCheck()
            if unoOdos == 1:
                    if self.seleccion != 3:
                        self.seleccion += 1
                    else:
                        self.seleccion = 0  # El mínimo
            elif unoOdos == 2:
                    if self.seleccion != 0:
                        self.seleccion -= 1
                    else:
                        self.seleccion = 3  # El máximo



        #confirmación con ENTER
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE) or False:
            # Por ahora TODAS van a la dificultad fácil
            self.activa = False
            self.dificultadSeleccionada = self.opciones[self.seleccion]
            # self.dificultadSeleccionada = self.opciones[2]
            pyxel.playm(0, loop=True)

        return self.dificultadSeleccionada

    def draw(self):
        # --Dibujar marco--
        x = 0
        y = 0
        w = pyxel.width
        h = pyxel.height
        color = COLORES["azulMarino"]
        for i in range(5): #Con esto se varía el grosor del rectángulo
            if i >= 3:
                color = COLORES["gris"]
            pyxel.rectb(x, y, w, h, color)
            x += 1
            y += 1
            w -= 2
            h -= 2

        # -- Título --
        if pyxel.frame_count % 3 == 0: #Para no dañar epilepticos (cambia de color cada 3 frames)
            self.parpadeoCol = random.randint(1, 15)
        x = 0
        y = -20
        pyxel.text(80+x, 20+y, """
        
M     M   AAAA   RRRR   III   OOOO        
MM   MM   A  A   R  R    I   O    O      
M M M M   A  A   R  R    I   O    O     
M  M  M   AAAA   RRRR    I   O    O     
M     M   A  A   R R     I   O    O    
M     M   A  A   R  R    I   O    O  
M     M   A  A   R   R  III   OOOO    
""", self.parpadeoCol)
        pyxel.text(80 +x, 80+y, """
        
BBBB   RRRR    OOOO   SSSS
B   B  R  R   O    O  S
B   B  R  R   O    O  S
BBBB   RRRR   O    O   SSS
B   B  R R    O    O      S
B   B  R  R   O    O      S
BBBB   R   R   OOOO   SSSS
""", self.parpadeoCol)

        # Para dibujar los botones
        x = 12
        y = 25

        i = 0  # REFACTOR: Es un contador, pero no me gustaba llamarlo contador
        for nombre in self.opciones:     #Así hacemos que "nombre" represente el nombre de las dificultades en función de su posicion en la lista
            color = self.colores[nombre] #utilizamos el diccionario para decidir el color del rectángulo

            #Si está seleccionado...
            if i == self.seleccion:
                colorRect = 5  # para resaltar
                borde = 10  #borde
            else:
                colorRect = color
                borde = 0 #para que parezca que se elimina el borde, aunque solo se vuelve del color del fondo

            pyxel.rect(x - 2, y - 2, 44, 18, borde)  # Rectángulo del borde (simplemente es un rectángulo más grande)
            pyxel.rect(x, y, 40, 14, colorRect)  # Rectángulo del botón


            #Texto del botón
            pyxel.text(x + 6, y + 5, nombre, COLORES["negro"])

            y += 22  # Separación de los rectángulos
            i += 1  # Incrementamos el contador

