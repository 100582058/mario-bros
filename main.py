import pyxel

from utils.config import WIDTH, HEIGHT, NUM_CINTAS, NUM_PAQ_CIN, DIFICULTAD, TIEMPO, scl
from clases.fabrica import Fabrica

from clases.pantallaInicio import PantallaInicio


# REFACTOR: Fabrica debería tener algunos parámetros
fabrica = Fabrica()
pantallaInicio = PantallaInicio()


def main():
    print("JUEGO INICIADO!")

    pyxel.init(int(WIDTH), int(HEIGHT), title="Proyecto final - Mario Bros", display_scale=scl)

    pyxel.load("assets/PyxelPersonajes.pyxres")

    pyxel.mouse(True)
    pyxel.run(update, draw)



def update():
    # global?
    juegoIniciado = False

    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    # Si todavía estamos en la pantalla inicial
    # if pantallaInicio.activa:
    dificultad = pantallaInicio.update()
    if dificultad:
        # Inicializamos el juego real cuando se confirme
        juegoIniciado = True

    # Lógica normal del juego
    if juegoIniciado:
        fabrica.juegoRun()


def draw():
    # Pantalla del juego
    # Fondo negro para la pantalla de inicio, blanco para el juego
    if pantallaInicio.activa:
        pyxel.cls(0)
    else:
        pyxel.cls(15)
    # Posicion del ratón
    txt = f"({pyxel.mouse_x}, {pyxel.mouse_y})"
    pyxel.text(5, 120, txt, 2)

    # Pantalla inicial
    if pantallaInicio.activa:
        pantallaInicio.draw()
        return

    fabrica.draw(WIDTH, HEIGHT)



if __name__ == "__main__":
    main()
