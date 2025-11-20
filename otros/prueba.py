import pyxel

def update():
    ''' Esta función se ejecuta cada frame. Ahora solo comprueba si
    la tecla Escape o Q se presionan para finalizar el programa'''
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(1)
    banco = 0
    pyxel.text(50, 90, "Banco de imagen 0", 7, )
    # --- Dibujando el banco de imagen ---
    # Cargamos el archivo
    pyxel.load("assets/resources.pyxres")
    # pyxel.blt(x:int, y:int, banco:int, u:int, v:int, w:int, h:int)
    # Dibujamos el banco
    pyxel.blt(50, 100, banco, 0, 0, 256, 256)


WIDTH, HEIGHT = 512, 512
CAPTION = "Código de prueba de Pyxel"

# Lo primero que hay que hacer es crear la pantalla, puedes ver la API de
# pyxel si deseas ver más parámetros
pyxel.init(WIDTH, HEIGHT, title=CAPTION)

# Para iniciar el juego invocamos el método run con las funciones update y draw
pyxel.run(update, draw)
