import pyxel

from utils.config import WIDTH, HEIGHT,scl, COLORES, asignarDificultad
from clases.fabrica import Fabrica

from clases.pantallaInicio import PantallaInicio

# Creamos la variable global sin asignarle ningún objeto, no sabemos la dificultad todavía
fabrica = None
pantallaInicio = PantallaInicio()
juegoIniciado = False


def main():
    pyxel.init(int(WIDTH), int(HEIGHT), title="Proyecto final - Mario Bros", display_scale=scl)

    # pyxel.load("assets/my_resource.pyxres") # DEBUG Assets de Alejandro
    # pyxel.load("assets/PyxelPersonajes.pyxres")
    #pyxel.load("assets/musicaFondo.pyxres")
    pyxel.load("assets/musicas_y_sonidos.pyxres")

    pyxel.mouse(True)
    pyxel.run(update, draw)



def update():
    # Necesario para usar variables globales dentro de una función
    global fabrica

    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    # -- Fase 1: Pantallad de inicio --
    if pantallaInicio.activa:
        dificultad = pantallaInicio.update()
        # Inicializamos el juego real cuando se confirme
        if dificultad:
            # Conseguimos la información de ese nivel
            configDificultad = asignarDificultad(dificultad.lower())
            # Instanciamos la Fábrica con esa configuración
            fabrica = Fabrica(configDificultad)
            print("Dificultad", dificultad.lower(), "Iniciamos el juego!")


    # -- Fase 2: Juego --
    if not pantallaInicio.activa:
        fabrica.juegoRun()


def draw():
    # -- Fase 1: Pantallad de inicio --
    if pantallaInicio.activa:
        # Fondo negro para la pantalla de inicio
        pyxel.cls(COLORES["negro"])
        pantallaInicio.draw()
    else:
        # -- Fase 2: Juego --
        pyxel.cls(COLORES["carne"])
        fabrica.draw(WIDTH, HEIGHT)


    # DEBUG: Posicion del ratón
    txt = f"({pyxel.mouse_x}, {pyxel.mouse_y})"
    pyxel.text(5, 120, txt, 2)




if __name__ == "__main__":
    main()
