from soko import *

def inmutar(grilla):
    desc = ""
    for i, fila in enumerate(grilla):
        renglon = ""
        for j in range(len(fila)):
            renglon += grilla[i][j]
        desc += renglon
        if i != len(grilla)-1:
            desc += "\n"
    return desc

def buscar_solucion(estado_inicial):
    " Wrapper de la función backtrack. "
    return backtrack(estado_inicial, visitados = set())

def backtrack(estado, visitados):
    """ Busca la solución del nivel por el método backtracking,
        en el caso de que exista una solución al nivel 
        devuelve las acciones para ganar el nivel (de atras hacia adelante). """

    visitados.add(inmutar(estado))

    if juego_ganado(estado):
        return True, []
    
    for mov in MOVIMIENTOS:
        nuevo_estado = mover(estado, MOVIMIENTOS[mov])
    
        if inmutar(nuevo_estado) in visitados:
            continue

        solucion_encontrada, acciones = backtrack(nuevo_estado, visitados)

        if solucion_encontrada:
            return True, acciones + [mov]
        
    return False, None



