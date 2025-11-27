import pyxel

from utils.config import WIDTH, HEIGHT, NUM_CINTAS, POS_PAQ_CIN, DIFICULTAD, TIEMPO, VIDAS, scl
from clases.fabrica import Fabrica

from clases.pantallaInicio import PantallaInicio

# CLASE: Pantalla de Inicio


fabrica = Fabrica(VIDAS, POS_PAQ_CIN, NUM_CINTAS)
pantalla_inicio = PantallaInicio()
juego_iniciado = False


def main():
    pyxel.init(int(WIDTH), int(HEIGHT), title="Proyecto final - Mario Bros", display_scale=scl)

    pyxel.load("assets/PyxelPersonajes.pyxres")

    pyxel.mouse(True)
    pyxel.run(update, draw)


def update():
    # global?
    global juego_iniciado

    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    # Si todavía estamos en la pantalla inicial
    if pantalla_inicio.activa:
        dificultad = pantalla_inicio.update()
        if dificultad is not None:
            # Inicializamos el juego real cuando se confirme
            # fabrica.start(POS_PAQ_CIN, NUM_CINTAS) # Ese método no existe
            juego_iniciado = True

    # Lógica normal del juego
    fallo = False
    if juego_iniciado and not fallo:
        fabrica.run()


def draw():
    # Pantalla inicial
    if pantalla_inicio.activa:
        pantalla_inicio.draw()
        return

    # Pantalla del juego
    pyxel.cls(7)
    fabrica.draw(WIDTH, HEIGHT)

    # Posicion del ratón
    txt = f"({pyxel.mouse_x}, {pyxel.mouse_y})"
    pyxel.text(40, 50, txt, 0)


if __name__ == "__main__":
    main()
