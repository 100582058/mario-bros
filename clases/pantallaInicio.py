import pyxel
from utils.config import WIDTH

class PantallaInicio:
    def __init__(self):
        self.opciones = ["Facil", "Normal", "Dificil", "Crazy"]
        self.colores = {
            "Facil": 11,    # verde
            "Normal": 10,   # amarillo
            "Dificil": 8,   # rojo
            "Crazy": 13     # gris
}
        self.seleccion = 0
        self.activa = True
        self.dificultadSeleccionada = None
        self.timer = 0
        self.comparador = 5 #Esto hace variar cuan rapido se activa el btn (que es para mantener el botón presionado)
                            #Tócalo para cambiar los fps del Btn (por debajo de 3 el jugador pierde precisión)(5 está bien)
    def btnCheck(self):
        if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):
            self.timer += 1
            if self.timer > self.comparador:
                self.timer = 0 #Aqui lo reinicia
                return 1
        elif pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP):
            self.timer += 1
            if self.timer > self.comparador:
                self.timer = 0
                return 2
        else:
            self.timer = 0


    def update(self):

        #seleccion por flechas y wasd
        if pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.KEY_DOWN):
            if self.seleccion != 3:
                self.seleccion += 1
            else:
                self.seleccion = 0 # El mínimo
            self.timer = 0

        elif pyxel.btnp(pyxel.KEY_W) or pyxel.btnp(pyxel.KEY_UP):
            if self.seleccion != 0:
                self.seleccion -= 1
            else:
                self.seleccion = 3 # El máximo
            self.timer = 0

        else:
            unoOdos = self.btnCheck()  # para que no halla problemas al llamar varias veces a la funcion en un solo frame
            if unoOdos == 1:           # como dato curioso al presionar a la vez arriba y abajo el programa tiene preferencia con
                                       # el hacia abajo por estar antes en el condicional. Pero no supone problema porque el usuario no debería tocar ambos botones a la vez, y aunque lo haga no va a ser terrible
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
        if pyxel.btnp(pyxel.KEY_RETURN): #Return es el enter
            # Por ahora TODAS van a la dificultad fácil
            self.activa = False
            self.dificultadSeleccionada = "facil"
            return "facil"

        return self.dificultadSeleccionada

    def draw(self):
        #Título
        pyxel.text(WIDTH//2 - 45, 10, "BIENVENIDO A MARIO BROS", pyxel.frame_count % 8)

        # Para dibujar los botones
        x = 12
        y = 30

        i = 0  #Es un contador, pero no me gustaba llamarlo contador
        for nombre in self.opciones:     #Así hacemos que "nombre" represente el nombre de las dificultades en función de su posicion en la lista
            color = self.colores[nombre] #utilizamos el diccionario para decidir el color del rectángulo

            #Si está seleccionado...
            if i == self.seleccion:
                color_rect = 3  # para resaltar
                borde = 10  #borde
            else:
                color_rect = color
                borde = 0 #para que parezca que se elimina el borde, aunque solo se vuelve del color del fondo

            pyxel.rect(x - 2, y - 2, 44, 18, borde)  # Rectángulo del borde (simplemente es un rectángulo más grande)
            pyxel.rect(x, y, 40, 14, color_rect)  # Rectángulo del botón


            #Texto del botón
            pyxel.text(x + 6, y + 5, nombre, 0)

            y += 22  # Separación de los rectángulos
            i += 1  # Incrementamos el contador

