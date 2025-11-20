"""
-- FORMATO DEL CÓDIGO --
Variables y funciones: Camelcase en español
Variables constantes/fijas: Mayúsculas y CON_GUIONES
Métodos privados: self.__metodo
"""

# Hay parámetros que serán asignados según la dificultad de juego elegida
num_cintas = 5
# Valor fijo: Número de posiciones en las que puede estar un paquete
posiciones_cinta = 8



# Añadir contador de puntos y fallos en el camión? En la máquina? O en main()?
# Meter funciones en vez de bloques de código de más de 4-5 líneas
# Hace falta añadir propiedades y setters a atributos asignados en innit?
# Hacen falta setters para valores no mutables? Hace falta validar/comprobar errores?
# Deberían ser atributos privados?
# Valores fijos en mayúsculas como constantes?

# CLASES (Fernando):
# Jefe?: visible (no, regañando_a_Mario, regañando_a_Luigi),

# Paquete: indice_cinta, pos_en_cinta, estado (en personaje, en cinta, en camion...), carga/nivel/num_botellas (1 botella, 2 botellas...)
## Si está en una cinta, se puede mover en forma de matriz (num_cintas, long_cinta)
# -----> Matriz grande perteneciente a Juego con [[0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 1]] (o trabajar con paquetes: [[paq, 0, 0, 0], ...])
# Quizá añadir una columna a cada lado para representar cuando el paquete está en el aire/jugador
#### def mover():
####    mover_par()
####    mover_impar()
#### def subir(): # Llamada si el jugador se encuentra en el piso. (Llamada dentro de mover)?
####    subir_par()
####    subir_impar()
#### def sacar():
#### def pintarMatriz():

"""
def update():
    cada X tiempo:
        mover_paquete() # Se mueven los que ya estaban añadidos (para que no de la sensación de que se añade el paquete inicial en la pos 2)
        añadir_paquete()

def draw():


"""

# Mario, Luigi, (Jefe) -> Personaje (Heredan)
# Juego/Fábrica: estado del juego (vidas, tiempo, estado...)

# Velocidad = fps (No funcionaría para cintas pares e impares a la vez?)