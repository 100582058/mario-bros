import pyxel

from utils.config import WIDTH, HEIGHT, NUM_CINTAS, NUM_PAQ_CIN, DIFICULTAD, COLORES, TIEMPO, scl
from clases.fabrica import Fabrica

from clases.pantallaInicio import PantallaInicio


# REFACTOR: Fabrica debería tener algunos parámetros
fabrica = Fabrica()
pantallaInicio = PantallaInicio()


def main():
    print("JUEGO INICIADO!")

    pyxel.init(int(WIDTH), int(HEIGHT), title="Proyecto final - Mario Bros", display_scale=scl)

    # pyxel.load("assets/my_resource.pyxres") # DEBUG Assets de Alejandro
    # pyxel.load("assets/PyxelPersonajes.pyxres")
    pyxel.load("assets/musicaFondo.pyxres")

    pyxel.mouse(True)
    pyxel.run(update, draw)



def update():
    juegoIniciado = False

    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    # Si todavía estamos en la pantalla inicial
    # if pantallaInicio.activa:
    dificultad = pantallaInicio.update()
    if dificultad:
        # Inicializamos el juego real cuando se confirme
        print("Dificultad", dificultad.lower(), "// se 'selecciona' la dificultad cada frame")
        # fabrica.seleccionarDificultad(dificultad.lower())
        juegoIniciado = True


    # Lógica normal del juego
    if juegoIniciado:
        fabrica.juegoRun()


def draw():
    # --- Dibujamos el contenido del juego ---
    if pantallaInicio.activa:
        # Fondo negro para la pantalla de inicio
        pyxel.cls(COLORES["negro"])
        pantallaInicio.draw()
    else:
        # Fondo claro para el juego
        pyxel.cls(COLORES["carne"])
        fabrica.draw(WIDTH, HEIGHT)



    # Posicion del ratón
    txt = f"({pyxel.mouse_x}, {pyxel.mouse_y})"
    pyxel.text(5, 120, txt, 2)




if __name__ == "__main__":
    main()
