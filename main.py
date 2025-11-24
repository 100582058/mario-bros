import pyxel

from utils.config import WIDTH, HEIGHT, scl
# POS_PAQ_CIN --> Las posiciones en las que puede estar un paquete en la cinta (columnas de la matriz)
from utils.config import NUM_CINTAS, POS_PAQ_CIN, DIFICULTAD, TIEMPO, VIDAS
from clases.fabrica import Fabrica

# EN CONFIG
# WIDTH, HEIGHT = 256, 256

# DIFICULTAD = "facil"
# # NUM_CINTAS, TIEMPO, VIDAS = asignarValores(DIFICULTAD)

# MARCO (Sprint 2)
# Vidas, fallos, tiempo
# Dibujar paquetes y cintas

# fabrica = None # ERROR??????? Se inicializa fuera del bucle????
fabrica = Fabrica(TIEMPO, VIDAS, POS_PAQ_CIN, NUM_CINTAS)


def main():
    # Se inicia el entorno de Pyxel
    pyxel.init(int(WIDTH), int(HEIGHT), title="Proyecto final - Mario Bros", display_scale=scl)

    # Cargamos el banco de imágenes
    pyxel.load("assets/PyxelPersonajes.pyxres")

    # Inicializamos el juego
    # NO, en __init__()
    # fabrica.start()

    # DEBUG: Para no ocultar el ratón
    pyxel.mouse(True)
    # Tiene que ir el ultimo, si no no se imprime nada
    pyxel.run(update, draw)


def update():
    """Esta función se ejecuta cada frame. Ahora solo comprueba si
    la tecla Escape o Q se presionan para finalizar el programa"""
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    # --- Bucle del juego ---
    # Bucle principal del juego, controlado por la fábrica
    fabrica.run()

    """
    Puede haber "lógica pequeña" en updaet/draw, como esto
    if (pantalla_inicio.seleccionado == "--"):
        pantalla_inicio.subir_foco()
    ...
    pantalla_inicio.bajar_foco()
    """


def draw():
    """Esta función pone objetos en la pantalla en cada turno"""
    # Fijamos el color de fondo, cualquier cosa que haya en la pantalla se borra
    pyxel.cls(7)
    # usamos pyxel.frame_count para realizar acciones cada frame
    # -----------------------------------------------------------------------
    # -----------------------------------------------------------------------
    # ERROR: Que argumentos pasarle?
    fabrica.draw()

    """
    
    """
    pyxel.text(WIDTH - 90, HEIGHT - 10, f"Mouse: ({pyxel.mouse_x}, {pyxel.mouse_y})", 3)


if __name__ == "__main__":
    main()
