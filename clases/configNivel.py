import time

# Contiene los datos de la configuración del nivel. No hace nada más, es solo un contenedor
class ConfigNivel:
    def __init__(self, controles_mario, controles_luigi, vel_cinta_0, 
                 vel_cintas_pares, vel_cintas_impares, num_cintas, 
                 anadir_paquetes_cada, elimina_fallos, numPaqCinta,
        sepEntreCintas,
        anchoPaq,
        altoPaq):
        # Parámetros relaccioandos con la dificultad del nivel
        self.controlesMario = controles_mario
        self.controlesLuigi = controles_luigi
        self.velCinta0 = vel_cinta_0
        self.velCintasPares = vel_cintas_pares
        self.velCintasImpares = vel_cintas_impares
        self.numCintas = num_cintas
        self.anadirPaquetesCada = anadir_paquetes_cada
        self.eliminaFallos = elimina_fallos

        # Parámetros externos a la dificultad del nivel
        self.numPaqCinta = numPaqCinta
        self.sepEntreCintas = sepEntreCintas
        self.anchoPaq = anchoPaq
        self.altoPaq = altoPaq
        self.anchoCinta = 140
        self.altoCinta = 4
        # Cuando se empieza a ejecutar el juego
        self.tiempoInicial = time.time()