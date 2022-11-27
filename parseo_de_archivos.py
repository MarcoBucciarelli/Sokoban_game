def cargar_teclas(archivo):

    """ Carga las teclas del juego a partir de un archivo txt de origen.
        
        Devuelve un diccionario donde las claves son las teclas,
        que se utilizaran y los valores asociados la dirección de movimiento
        correspondiente.
    
      """
      
    with open(archivo) as f:
        direcciones = {}
        for linea in f:
            linea = linea.rstrip()
            if linea != "":
                linea = linea.split()
                direcciones[linea[0]] = linea[2]
    return direcciones

def cargar_niveles(archivo):

    """ Carga los niveles del juego Sokoban a partir de un archivo txt.

        Devuelve los niveles del juego sokoban en un diccionario.
        Donde las claves corresponden al título del nivel, y los valores a el
        nivel correspondiente. """

    with open(archivo) as lvl:
        niveles = {}
        max_nivel = 0
        desc = []
        for linea in lvl:
            linea = linea.rstrip()
            centinela = True
            if len(linea) == 0:
                niveles[titulo] = desc
                max_nivel += 1
                desc = []
                centinela = False
            if "Level" in linea:
                titulo = linea
            for caracter in linea:
                if caracter.isalpha() or caracter.isdigit():
                    centinela = False
            if centinela != False:
                desc.append(linea)
        niveles[titulo] = desc
        max_nivel += 1
    return niveles, max_nivel


    