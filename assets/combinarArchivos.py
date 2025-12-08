import zipfile
import shutil
import os

print("=== Combinador de archivos .pyxres ===\n")

# Archivos de entrada
archivo_musica = "musicas_y_sonidos.pyxres"
archivo_imagenes = "PyxelPersonajes.pyxres"
archivo_salida = "my_resources.pyxres"

# Crear carpetas temporales
carpeta_musica = "temp_musica"
carpeta_imagenes = "temp_imagenes"
carpeta_salida = "temp_salida"

# Limpiar carpetas temporales si existen
for carpeta in [carpeta_musica, carpeta_imagenes, carpeta_salida]:
    if os.path.exists(carpeta):
        shutil.rmtree(carpeta)
    os.makedirs(carpeta)

print("1. Extrayendo archivos...")
# Extraer ambos archivos
with zipfile.ZipFile(archivo_musica, 'r') as zip_ref:
    zip_ref.extractall(carpeta_musica)
    print(f"   ✓ {archivo_musica} extraído")

with zipfile.ZipFile(archivo_imagenes, 'r') as zip_ref:
    zip_ref.extractall(carpeta_imagenes)
    print(f"   ✓ {archivo_imagenes} extraído")

print("\n2. Leyendo archivos TOML...")
# Leer los archivos .toml
with open(os.path.join(carpeta_musica, "pyxel_resource.toml"), 'r', encoding='utf-8') as f:
    contenido_musica = f.read()

with open(os.path.join(carpeta_imagenes, "pyxel_resource.toml"), 'r', encoding='utf-8') as f:
    contenido_imagenes = f.read()

print("   ✓ Archivos TOML leídos")

print("\n3. Combinando recursos...")
# Dividir el contenido en secciones


def extraer_seccion(contenido, inicio_marca, fin_marca):
    inicio = contenido.find(inicio_marca)
    if inicio == -1:
        return ""
    fin = contenido.find(fin_marca, inicio)
    if fin == -1:
        return contenido[inicio:]
    return contenido[inicio:fin]


# Extraer las secciones necesarias
# Del archivo de imágenes: images
imagenes_seccion = extraer_seccion(
    contenido_imagenes, "[[images]]", "[[tilemaps]]")

# Del archivo de música: sounds y musics
sounds_inicio = contenido_musica.find("[[sounds]]")
sounds_y_musics = contenido_musica[sounds_inicio:] if sounds_inicio != -1 else ""

# Crear el formato base (header + tilemaps vacíos)
tilemaps_vacios = """
[[tilemaps]]
width = 256
height = 256
imgsrc = 0
data = [[0]]

[[tilemaps]]
width = 256
height = 256
imgsrc = 0
data = [[0]]

[[tilemaps]]
width = 256
height = 256
imgsrc = 0
data = [[0]]

[[tilemaps]]
width = 256
height = 256
imgsrc = 0
data = [[0]]

[[tilemaps]]
width = 256
height = 256
imgsrc = 0
data = [[0]]

[[tilemaps]]
width = 256
height = 256
imgsrc = 0
data = [[0]]

[[tilemaps]]
width = 256
height = 256
imgsrc = 0
data = [[0]]

[[tilemaps]]
width = 256
height = 256
imgsrc = 0
data = [[0]]
"""

# Combinar todo
contenido_combinado = "format_version = 1\n\n" + \
    imagenes_seccion + tilemaps_vacios + "\n" + sounds_y_musics

# Guardar el archivo combinado
ruta_salida = os.path.join(carpeta_salida, "pyxel_resource.toml")
with open(ruta_salida, 'w', encoding='utf-8') as f:
    f.write(contenido_combinado)

print("   ✓ Recursos combinados en TOML")

print("\n4. Creando archivo .pyxres...")
# Comprimir el archivo TOML en un nuevo .pyxres
with zipfile.ZipFile(archivo_salida, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(ruta_salida, "pyxel_resource.toml")

print(f"   ✓ {archivo_salida} creado")

print("\n5. Limpiando archivos temporales...")
# Limpiar carpetas temporales
for carpeta in [carpeta_musica, carpeta_imagenes, carpeta_salida]:
    if os.path.exists(carpeta):
        shutil.rmtree(carpeta)

print("   ✓ Archivos temporales eliminados")

print(f"\n{'='*50}")
print("✓ ¡Proceso completado exitosamente!")
print(f"{'='*50}")
print(f"\nArchivo creado: {archivo_salida}")
print("\nContenido combinado:")
print("  - Imágenes de: PyxelPersonajes.pyxres")
print("  - Música/Sonidos de: musicaFondo.pyxres")
print("\nPuedes abrirlo con: pyxel edit recursos_combinados.pyxres")
