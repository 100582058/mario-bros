import pyxel

# DEBUG: Hay que dibujar una parte especifica del banco de imágenes
def dibujar(obj, id=None):
    if id == "mario":
        # MUESTRA A MARIO
        x = obj.posicion[0]
        y = obj.posicion[1]
        tamanoImg, banco = 16, 0
        # USAR bltm
        """bltm(x, y, tm, u, v, w, h, [colkey], [rotate], [scale])
Copy the region of size (w, h) from (u, v) of the tilemap tm(0-7) to (x, y). If a negative value is assigned to w and/or h,
the region will be flipped horizontally and/or vertically. If colkey is specified, it will be treated as a transparent color.
If rotate(in degrees), scale(1.0 = 100%), or both are specified, the corresponding transformations will be applied.
The size of a tile is 8x8 pixels and is stored in a tilemap as a tuple of (image_tx, image_ty)."""
        pyxel.blt(x + 40, y, banco, 0, 0, tamanoImg, tamanoImg, scale=2)


    # Dibujamos el banco
    # banco = 0
    # pyxel.blt(x:int, y:int, banco:int, u:int, v:int, w:int, h:int)
    # x, y, w, h: Variables del banco
    # pyxel.blt(5, 5, banco, 0, 0, 256, 256)