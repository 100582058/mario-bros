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

    def update(self):
        #seleccion por flechas y wasd
        if pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.KEY_DOWN):
            self.seleccion = (self.seleccion + 1) % len(self.opciones) #len(self.opciones sirve para que al bajar más de crazy vuelva a easy), es decir, lo reinicia en 4 

        if pyxel.btnp(pyxel.KEY_W) or pyxel.btnp(pyxel.KEY_UP):
            self.seleccion = (self.seleccion - 1) % len(self.opciones)

        #confirmación con ENTER
        if pyxel.btnp(pyxel.KEY_RETURN): #Return es el enter
            # Por ahora TODAS van a la dificultad fácil
            self.activa = False
            return "facil"

        return None

    def draw(self):
        pyxel.cls(0)

        #Título
        pyxel.text(WIDTH//2 - 50, 30, "BIENVENIDO A MARIO BROS", pyxel.frame_count % 8)

        # Para dibujar los botones
        x = 40
        y = 100

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

            pyxel.rect(x - 3, y - 3, 62, 22, borde)  # Rectángulo del borde (simplemente es un rectángulo más grande)
            pyxel.rect(x, y, 56, 16, color_rect)  # Rectángulo del botón


            #Texto del botón
            pyxel.text(x + 15, y + 5, nombre, 0)

            y += 30  # Separación de los rectángulos
            i += 1  # Incrementamos el contador

