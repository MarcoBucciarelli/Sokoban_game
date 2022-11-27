MOVIMIENTOS = {"OESTE":(-1, 0), "ESTE":(1, 0), "NORTE":(0, -1), "SUR":(0, 1)}

def crear_grilla(desc):

    '''Crea una grilla a partir de la descripción del estado inicial.

    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Los caracteres pueden ser los siguientes:

    Caracter  Contenido de la celda
    --------  ---------------------
           #  Pared
           $  Caja
           @  Jugador
           .  Objetivo
           *  Objetivo + Caja
           +  Objetivo + Jugador

    Ejemplo:

    >>> crear_grilla([
        '#####',
        '#.$ #',
        '#@  #',
        '#####',
    ])
    '''
    grilla = []
    for i in range(len(desc)):
        fila = []
        for j in range(len(desc[i])):
            fila.append(desc[i][j])
        grilla.append(fila)
    return grilla

def dimensiones(grilla):
    '''Devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
    (c, f) = (len(grilla[0]), len(grilla))
    return (c, f)

def hay_pared(grilla, c, f):
    """Devuelve True si hay una pared en la columna y fila (c, f)."""
    return grilla[f][c] == "#"

def hay_objetivo(grilla, c, f):
    '''Devuelve True si hay un objetivo en la columna y fila (c, f).'''
    if grilla[f][c] == "." or grilla[f][c] == "+" or grilla[f][c] == "*":
        return True
    return False

def hay_caja(grilla, c, f):
    '''Devuelve True si hay una caja en la columna y fila (c, f).'''
    if grilla[f][c] == "$" or grilla[f][c] == "*":
        return True
    return False

def hay_jugador(grilla, c, f):
    '''Devuelve True si el jugador está en la columna y fila (c, f).'''
    if grilla[f][c] == "@" or grilla[f][c] == "+":
        return True
    return False

def hay_suelo(nivel, c, f):

    """ Devuelve True si hay una celda vacía en la columna y fila (c,f). """

    return nivel[f][c] == " "

def juego_ganado(grilla):
    '''Devuelve True si el juego está ganado.'''
    for i in range(len(grilla)):
        if "." in grilla[i] or "+" in grilla[i]:
            return False
    return True 

def jugador(grilla):
    """ Devuelve la posición del jugador en la grilla, 
        como una tupla (columna, fila). """
    for i in range(len(grilla)):
        for j in range(len(grilla[i])):
            if hay_jugador(grilla, j, i):
                return (j,i)

def posicion_inicial(grilla, c, f):
    """ Devuelve la celda en donde estaba posicionado el jugador. """
    if hay_objetivo(grilla, c, f):
        return "."
    return " "

def posicion_movimiento(grilla, c, f):
    """ Devuelve la celda hacia donde se mueve el jugador. """
    if hay_objetivo(grilla, c, f):
        return "+"
    return "@"

def mover(grilla, direccion):

    """Mueve el jugador en la dirección indicada.

    La dirección es una tupla con el movimiento horizontal y vertical. Dado que
    no se permite el movimiento diagonal, la dirección puede ser una de cuatro
    posibilidades:

    direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur

    La función debe devolver una grilla representando el estado siguiente al
    movimiento efectuado. La grilla recibida NO se modifica; es decir, en caso
    de que el movimiento sea válido, la función devuelve una nueva grilla.
    """
    
    posicion_jugador = jugador(grilla)
    grilla_n = crear_grilla(grilla)
    movimiento = (posicion_jugador[0] + direccion[0], posicion_jugador[1] + direccion[1])

    if hay_pared(grilla, movimiento[0], movimiento[1]):
        return grilla
            
    elif hay_caja(grilla, movimiento[0], movimiento[1]):

        caja_movimiento = (movimiento[0] + direccion[0], movimiento[1] + direccion[1])

        if hay_pared(grilla, caja_movimiento[0], caja_movimiento[1]) or hay_caja(grilla, caja_movimiento[0], caja_movimiento[1]):
            return grilla
        
        elif hay_objetivo(grilla, caja_movimiento[0], caja_movimiento[1]):
            grilla_n[posicion_jugador[1]][posicion_jugador[0]] = posicion_inicial(grilla_n, posicion_jugador[0], posicion_jugador[1])
            grilla_n[movimiento[1]][movimiento[0]] = posicion_movimiento(grilla, movimiento[0], movimiento[1])
            grilla_n[caja_movimiento[1]][caja_movimiento[0]] = "*"

        else:
            grilla_n[posicion_jugador[1]][posicion_jugador[0]] = posicion_inicial(grilla_n, posicion_jugador[0], posicion_jugador[1])
            grilla_n[movimiento[1]][movimiento[0]] = posicion_movimiento(grilla, movimiento[0], movimiento[1])
            grilla_n[caja_movimiento[1]][caja_movimiento[0]] = "$"

    elif hay_objetivo(grilla, movimiento[0], movimiento[1]):
            grilla_n[movimiento[1]][movimiento[0]] = "+"
            grilla_n[posicion_jugador[1]][posicion_jugador[0]] = posicion_inicial(grilla_n, posicion_jugador[0], posicion_jugador[1])
            
    else:
        grilla_n[movimiento[1]][movimiento[0]] = "@"
        grilla_n[posicion_jugador[1]][posicion_jugador[0]] = posicion_inicial(grilla_n, posicion_jugador[0], posicion_jugador[1])
    
    return grilla_n








