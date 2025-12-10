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
    pyxel.load("assets/my_resources.pyxres")

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
    if not pantallaInicio.activa and fabrica.activa:
        fabrica.juegoRun()

    # Mute a la M
    if pyxel.btnp(pyxel.KEY_M) and not pantallaInicio.activa:
        pantallaInicio.contadorMusica += 1
        if pantallaInicio.contadorMusica == 2:
            pantallaInicio.contadorMusica = 0

        if pantallaInicio.contadorMusica == 1:
            pyxel.stop()
            print("se para la musica")

        else:
            pyxel.stop()
            pyxel.playm(0, loop=True)



def draw():
    # -- Fase 1: Pantallad de inicio --
    if pantallaInicio.activa:
        # Fondo negro para la pantalla de inicio
        pyxel.cls(COLORES["negro"])
        pantallaInicio.draw()
    elif fabrica.activa:
        # -- Fase 2: Juego --
        pyxel.cls(COLORES["carne"])
        fabrica.draw()




if __name__ == "__main__":
    main()
