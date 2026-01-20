import heapq    # Permite usar colas de prioridad 
import random   # Se utiliza para generar numeros aleatorios

# ---------- Representacion del terreno del Mapa ----------
CAMINO_LIBRE = 0  # Camino libre sin costo de circulacion
EDIFICIO = 1      # Edificio (intransitable)
AGUA = 2          # Agua (Transitable con mayor costo)

prob_edificio = 0.18  # Probabilidad del 18% de de que una celda sea edificio
prob_agua = 0.12      # Probabilidad del 12% de de que una celda sea agua 

MOVIMIENTOS = [(-1,0), (1,0), (0,-1), (0,1)]

COSTOS = {            # Se define cuanto cuesta pasar cada tipo de terreno
    CAMINO_LIBRE: 1,
    AGUA: 3
}
# ---------- Creacion del Mapa ----------
def crear_mapa():
    filas = int(input(f'\ningrese la cantidad de filas que tendra el mapa: '))             # Ingreso de datos del usuario para filas
    columnas = int(input(f'\ningrese la cantidad de columnas que tendra el mapa: '))       # Ingreso de datos del usuario para columnas
    mapa = [[CAMINO_LIBRE for _ in range(filas)] for _ in range(columnas)]                 # Se crea una matriz vacia (llena de 0)
    return mapa                                                                            # Se retorna el mapa 

def agregar_obstaculos(mapa, prob_edificio, prob_agua):
    filas = len(mapa)                                        
    columnas = len(mapa[0])                            # Obtiene el tamanho del mapa
    for i in range(filas):
        for j in range(columnas):                      # Recorre cada celda del mapa (filas y columnas)
            rand = random.random()                     # Genera un numero aleatorio entre 0 y 1

            if rand < prob_edificio:                   
                mapa[i][j] = EDIFICIO                  # Si el numero cae dentro de la probabilidad, coloca un edificio
            elif rand < prob_edificio + prob_agua:
                mapa[i][j] = AGUA                      # Si no es edificio pero esta dentro del rango, coloca agua

def mostrar_mapa(mapa, ruta=None):                # Muestra el mapa en pantalla
    filas = len(mapa)
    columnas = len(mapa[0])                       # Obtiene dimensiones
    print('  ', end='')                           # Imprime espacio para los numeros de columnas y filas
    for j in range(columnas):                     
        print(f'{j:2}', end='')                   # Imprime los numeros o indices de columnas
    print()                                       # Realiza un salto de linea
    print('  ' + '#' * (columnas * 3 + 1))        # Dibuja una linea superior del marco
    for i in range(filas):
        print(f'{i:2} #', end=' ')                # Imprime numero o indice de filas y el marco
        for j in range(columnas):
            if ruta and (i, j) in ruta:
                print('*', end=' ')               # Si la celda pertenece a ruta muestra *
            elif mapa[i][j] == CAMINO_LIBRE:
                print('.', end=' ')               # Si la celda es camino libre muestra .
            elif mapa[i][j] == AGUA:
                print('~', end=' ')               # Si la celda es agua muestra ~ 
            elif mapa[i][j] == EDIFICIO:
                print('X', end=' ')               # Si la celda es edificio muestra X                  
    print(' ' + '#' * (columnas *3 + 1))          # Cierra el mapa

# ---------- Coordenadas ----------
def pedir_coordenadas(nombre, mapa):                                      
    filas = len(mapa)
    columnas = len(mapa[0])                                              # Obtiene el tamaño del mapa
    while True:
        print(f'\nIngrese la coordenada de {nombre}')
        x = int(input('fila: '))
        y = int(input('columna: '))                                      # Lee filas y columnas
        if x < 0 or x >= filas or y < 0 or y >= columnas:                # Verifica que esté dentro del mapa
            print(f'\nla coordenada es invalida, intente de nuevo')      # Si las coordenadas no estan dentro del mapa, imprime un mensaje de invalidez
            continue
        if mapa[x][y] == EDIFICIO:                                       
            print(f'\nno se puede usar un edificio, intente de nuevo')   # Si coincide con un edificio no permite utilizar la coordenada
            continue
        return (x, y)                                                    # Devuelve la coordenada válida

# ---------- Funcion Dijkstra ----------
def dijkstra(mapa, inicio, destino):
    filas = len(mapa)
    columnas = len(mapa[0])
    if not (0 <= inicio[0] < filas and 0 <= inicio[1] < columnas):         # Verifica que la coordenada de inicio este dentro del mapa
        return None, float('inf')                                          # Si no es valida devuelve None
    if not (0 <= destino[0] < filas and 0 <= destino[1] < columnas):       # Se realiza lo mismo para el destino
        return None, float('inf')                                          # Si el destino no es valido termina la funcion
    dist = [[float('inf')] * columnas for _ in range (filas)]              # Crea una matriz que guarda la distancia minima desde el inicio a cada celda, todas empiezan en infinito
    padre = [[None] * columnas for _ in range (filas)]                     # Luego una matriz que guarda las celdas que ya fueron procesadas o visitadas
    visitados = set()                                                      # Conjunto para guardar las celdas que ya fueron procesadas

    pq = []                                                                # Crea una cola de prioridad vacia
    heapq.heappush(pq, (0, inicio))                                        # Agrega el punto de inicio a la cola con costo 0
    dist[inicio[0]][inicio[1]] = 0                                         # La distancia del inicio hasta si mismo es de 0

    while pq:                                                              # Mientras haya nodos por explorar en la cola
        costo, (x, y) = heapq.heappop(pq)                                  # Saca de la cola la celda con menor costo acumulado
        if (x, y) in visitados:                                            
            continue                                                       # Si ya fue visitada, se salta y pasa a la siguiente
        visitados.add((x, y))                                              # Se marca la celda actual como visitada 
        if (x, y) == destino:
            return reconstruir_camino(padre, inicio, destino), costo       # Si se llego al destino se reconstruye el camino y devuelve la ruta y su costo total
        if costo > dist[x][y]:
            continue                                                       # Si este camino es peor que uno ya conocido, se ignora
        for dx, dy in MOVIMIENTOS:                                         # Recorre todos los movimientos posibles
            nx, ny = x + dx, y + dy                                        # Calcula la posicion del vecino 
            if not (0 <= nx < filas and 0 <= ny < columnas):
                continue                                                   # Si esta fuera del mapa lo ignora
            if (nx, ny) in visitados:
                continue                                                   # Si ya fue visitado lo ignora
            if mapa[nx][ny] == EDIFICIO:
                continue                                                   # Mismo caso al no poder atravesar edificios
            nuevo_costo = costo + COSTOS.get(mapa[nx][ny], 1)              # Calcula el nuevo costo sumando el costo del terreno
            if nuevo_costo < dist[nx][ny]:
                dist[nx][ny] = nuevo_costo                                 # Se acutualiza la mejor distancia si el nuevo camino es mejor que el anterior
                padre[nx][ny] = (x, y)                                     # Guarda desde donde se llego a esa celda
                heapq.heappush(pq, (nuevo_costo, (nx, ny)))                # Agrega el vecino a la cola de prioridad
    return None, float('inf')                                              # Si se vacia la cola y no se llego al destino, no hay camino posible

# ---------- Recontruccion de Caminos ---------- 
def reconstruir_camino(padre, inicio, destino):                            # Reconstruye la ruta desde el destino hasta el inicio
    if padre[destino[0]][destino[1]] is None and destino != inicio:
        return None                                                        # Si nunca se llegó al destino, no hay camino y se dedvuelve None
    camino = []                                                            # La lista se guarda donde se guarda el camino
    actual = destino                                                       # Empieza desde el destino
    while actual is not None:
        camino.append(actual)                                              # Mientras haya una celda anterior esta se agrega al camino
        actual = padre[actual[0]][actual[1]]                               # Se meueve a la celda anterior
    camino.reverse()                                                       # Invierte la l.ista para que vaya de inicio a destino
    return camino                                                          # Devuelve la ruta completa

# ---------- Obstaculos Adicionales ----------
def agregar_obstaculos_usuario(mapa):
    n = int(input('cuantos obstaculos quiere agregar al mapa?: '))           # Ingreso de datos, pide al usuario cantidad de obstaculos a agregar
    for _ in range(n):                                                       # Repite ese numero ded veces
        x = int(input('Fila: '))
        y = int(input('Columna: '))                                          # Pide posicion (Fila y columna)
        tipo = input('Tipo: X (edificio) o ~ (agua): ')                      # Pide tipo de obstaculo
        if 0 <= x < len(mapa) and 0 <= y < len(mapa[0]):                     # Verifica que este dentro del mapa
            if tipo == "X":
                mapa[x][y] = EDIFICIO                                        # Coloca edificio
            elif tipo == "~":
                mapa[x][y] = AGUA                                            # Coloca agua

# ---------- Loop Principal ----------
def main():
    mapa = crear_mapa()
    agregar_obstaculos(mapa, prob_edificio, prob_agua)
    mostrar_mapa(mapa)
    inicio = pedir_coordenadas('inicio', mapa)
    destino = pedir_coordenadas('destino', mapa)

    while True:
        ruta, costo = dijkstra(mapa, inicio, destino)
        if ruta:
            print(f'\nCamino encontrado con costo: {costo}')
            mostrar_mapa(mapa, ruta)
        else: 
            print(f'\nNo se encontraron caminos validos')
            mostrar_mapa(mapa, ruta)
        opcion = input('desea agregar mas obstaculos? (s/n):').lower()
        if opcion != "s":
            break
        agregar_obstaculos_usuario(mapa)
main()
#fin