import pyxel

from utils.config import WIDTH, HEIGHT, scl, COLORES, asignarDificultad
from clases.fabrica import Fabrica

from clases.pantallaInicio import PantallaInicio

# Creamos la variable global sin asignarle ningún objeto, no sabemos la dificultad todavía
fabrica = None
pantallaInicio = PantallaInicio()
juegoIniciado = False


def main():
    pyxel.init(int(WIDTH), int(HEIGHT),
               title="Proyecto final - Mario Bros", display_scale=scl)

    # Cargamos los archivos de música e imágenes
    pyxel.load("assets/musicas_y_sonidos.pyxres")

    # DEBUG
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
        # Funcionamiento .bltm -> Dibuja un mapa de mosaicos (tilemap) en la pantalla.
        # Los parámetros son:
        # x, y: Coordenadas en la pantalla donde se dibuja el mapa.
        # tm: Índice del tilemap a usar (en este caso, 2).
        # u, v: Coordenadas en el tilemap desde donde se empieza a dibujar.
        # w, h: Ancho y alto del área a dibujar en mosaicos (tiles).
        # pyxel.bltm(0, 0, tm=0, u=0, v=0, w=WIDTH, h=HEIGHT)
        fabrica.draw()

    # DEBUG: Posicion del ratón
    txt = f"({pyxel.mouse_x}, {pyxel.mouse_y})"
    pyxel.text(5, 120, txt, 2)



if __name__ == "__main__":
    main()
