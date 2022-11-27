from soko import *
import gamelib
from pila import Pila
from parseo_de_archivos import cargar_niveles, cargar_teclas
from backtracking import buscar_solucion

TAMAÑO_CELDA = 61
archivo_niveles = "niveles.txt"
archivo_teclas = "teclas.txt"

def juego_mostrar(nivel, tamaño_celda, titulo, col, fil):
    
    rutas = {
            "pared" : "img/wall.gif",
            "piso" :"img/ground.gif",
            "objetivo" : "img/goal.gif",
            "caja" : "img/box.gif",
            "jugador" :"img/player.gif"
            }

    gamelib.draw_begin()
    elementos_a_dibujar = []

    for f, fila in enumerate(nivel):

        for c in range(len(fila)):

            if hay_pared(nivel, c, f): elementos_a_dibujar.append(rutas["pared"])

            if hay_suelo(nivel, c, f) or hay_jugador(nivel, c, f) or hay_objetivo(nivel, c, f): elementos_a_dibujar.append(rutas["piso"])

            if hay_caja(nivel, c, f): elementos_a_dibujar.append(rutas["caja"])

            if hay_objetivo(nivel, c, f): elementos_a_dibujar.append(rutas["objetivo"])

            if hay_jugador(nivel, c, f): elementos_a_dibujar.append(rutas["jugador"])

            for objeto in elementos_a_dibujar:
                gamelib.draw_image(objeto, c * tamaño_celda, f * tamaño_celda)

    gamelib.draw_text(f"{titulo}", (col * tamaño_celda)/2, fil * tamaño_celda + tamaño_celda/2, size = 14)
    gamelib.draw_end()

def tamaño_ajuste(juego):

    """Determina el tamaño de la grilla para ajustar la ventana de juego. """

    max_col, max_fila = 0, len(juego)
    for fila in juego:
        if len(fila) > max_col: max_col = len(fila)
    return max_col, max_fila

def main():

    "Inicializa el juego Sokoban. "

    gamelib.title("Sokoban")

    try:
        archivo = archivo_niveles
        niveles, max_nivel = cargar_niveles(archivo_niveles)
        archivo = archivo_teclas
        teclas = cargar_teclas(archivo_teclas)
    except IOError:
        print(f"Error al abrir el archivo: {archivo}")
        return



    escape = False
    nro_nivel = 0

    while escape != True and nro_nivel < max_nivel:
        nro_nivel += 1
        titulo = f"Level {nro_nivel}"
        nivel = crear_grilla(niveles[titulo])
        col, fil = tamaño_ajuste(nivel)
        estado_act = {titulo:nivel, "deshacer":Pila(), "hacer":Pila(), "pistas":Pila(), "hay_solucion":True}

        # Ajustar el tamaño de la ventana
        gamelib.resize(col * TAMAÑO_CELDA, fil * TAMAÑO_CELDA + TAMAÑO_CELDA)

        while gamelib.is_alive():

            # Dibujar la pantalla
            juego_mostrar(nivel, TAMAÑO_CELDA, titulo, col, fil)

            ev = gamelib.wait(gamelib.EventType.KeyPress)
            if not ev:
                # El usuario cerró la ventana.
                break

            tecla = ev.key
            # Actualizar el estado del juego, según la `tecla` presionada
            
            if tecla not in teclas: continue

            if teclas[tecla] in MOVIMIENTOS:
                direccion = teclas[tecla]
                movimiento = MOVIMIENTOS[direccion]
                nivel_act = mover(nivel, movimiento)
                if nivel_act != nivel:
                    estado_act[titulo] = nivel_act
                    hacia_atras = (-MOVIMIENTOS[direccion][0], -MOVIMIENTOS[direccion][1])
                    estado_act["deshacer"].apilar(hacia_atras)
                    estado_act["hacer"] = Pila()
                    estado_act["pistas"] = Pila()
                nivel = estado_act[titulo]

            if tecla == "p":
                if estado_act["pistas"].esta_vacia() and estado_act["hay_solucion"] == True:
                    hay_solucion, acciones = buscar_solucion(nivel)
                    if hay_solucion:
                        for accion in acciones: estado_act["pistas"].apilar(MOVIMIENTOS[accion])
                    else:
                        estado_act["hay_solucion"] = False
                    
                if not estado_act["pistas"].esta_vacia():
                    movimiento = estado_act["pistas"].desapilar()
                    nivel = mover(nivel, movimiento)
                    hacia_atras = (-movimiento[0], -movimiento[1])
                    estado_act["deshacer"].apilar(hacia_atras)
                    estado_act["hacer"] = Pila()

            if tecla == "z":
                if not estado_act["deshacer"].esta_vacia():
                    movimiento = estado_act["deshacer"].desapilar()
                    nivel = mover(nivel, movimiento)
                    hacia_adelante = (-movimiento[0], -movimiento[1])
                    estado_act["hacer"].apilar(hacia_adelante)                         
                    
            if tecla == "x" and not estado_act["hacer"].esta_vacia():
                movimiento = estado_act["hacer"].desapilar()
                nivel = mover(nivel, movimiento)
                hacia_atras = (-movimiento[0], -movimiento[1])
                estado_act["deshacer"].apilar(hacia_atras)

            if tecla == "Escape": 
                escape = True
                break
            
            elif tecla == "r":
                nivel = crear_grilla(niveles[titulo])
                estado_act["deshacer"] = Pila()
                estado_act["hacer"] = Pila()
                
            if juego_ganado(nivel):
                break

gamelib.init(main)