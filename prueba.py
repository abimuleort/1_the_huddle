   # FUNCION crear_matriz(filas, columnas)
    #    // TODO: Crear y retornar una matriz de tamaño filas x columnas
     #   // Inicializar todas las posiciones con un valor por defecto
    #FIN FUNCION

    #FUNCION establecer_puntos(matriz, inicio, fin)
     #   // TODO: Recibir dos tuplas con coordenadas (fila, columna)
      #  // Desempaquetar las tuplas para obtener las posiciones
       # // Marcar en la matriz la entrada con "E" y la salida con "S"
        #// Retornar la matriz modificada
    #FIN FUNCION

    #FUNCION mostrar_laberinto(matriz)
     #   // TODO: Recorrer la matriz completa
      #  // Imprimir cada fila mostrando ".", "E" o "S" según corresponda
       # // Dar formato visual agradable (espacios entre elementos)
    #FIN FUNCION

    #FUNCION menu_principal()
     #   // TODO: Solicitar al usuario el tamaño del laberinto (filas y columnas)
      #  // Llamar a crear_matriz con los valores ingresados
       # // Solicitar coordenadas para entrada (tupla: fila, columna)
      #  // Solicitar coordenadas para salida (tupla: fila, columna)
       # // Llamar a establecer_puntos pasando las tuplas
       # // Llamar a mostrar_laberinto para visualizar el resultado
    #FIN FUNCION

def crear_matriz(filas, columnas):
    matriz = [[0 for _ in range (columnas)] for _ in range (filas)]
    return matriz
 
def establecer_puntos(matriz, inicio, fin):
    filas = len(matriz)
    columnas = len(matriz[0])
    fila_inicio, columna_inicio = inicio
    fila_fin, columna_fin = fin
    return matriz

def mostrar_laberinto(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    for filas in matriz:
        print(' '.join(filas))
    return matriz

def menu_principal():
    filas = int(input("Cuantas filas tendra el mapa?"))
    columnas = int(input("Cuantas columnas tendra el mapa?"))
    matriz = crear_matriz(filas, columnas)
    inicio = (int(input("Fila entrada: ")), int(input("Columna entrada: ")))
    fin = (int(input("Fila salida: ")), int(input("Columna salida: ")))
    matriz = establecer_puntos(matriz, inicio, fin)
    mostrar_laberinto(matriz)
if __name__ == "__main__":
    menu_principal()