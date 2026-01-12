import heapq
import random

CAMINO_LIBRE = 0
EDIFICIO = 1
AGUA = 2

prob_edificio = 0.18
prob_agua = 0.12

MOVIMIENTOS = [(-1,0), (1,0), (0,-1), (0,1)]

COSTOS = {
    CAMINO_LIBRE: 1,
    AGUA: 3
}

def crear_mapa():
    filas = int(input('ingrese la cantidad de filas que tendra el mapa'))
    columnas = int(input('ingrese la cantidad de columnas que tendra el mapa'))
    mapa = [[CAMINO_LIBRE for _ in range(columnas)] for _ in range(filas)] # tiene que estar al reves tu Fila y columna
    return mapa

def agregar_obstaculos(mapa, prob_edificio, prob_agua):
    filas = len(mapa)
    columnas = len(mapa[0])
    for i in range(filas):
        for j in range(columnas):
            rand = random.random()

            if rand < prob_edificio:
                mapa[i][j] = EDIFICIO
            elif rand < prob_edificio + prob_agua:
                mapa[i][j] = AGUA

def mostrar_mapa(mapa, ruta=None):
    filas = len(mapa)
    columnas = len(mapa[0])
    print('  ', end='')
    for j in range(columnas):
        print(f'{j:2}', end='')
    print()
    print('  ' + '#' * (columnas * 3 + 1))
    for i in range(filas):
        print(f'{i:2} #', end=' ')
        for j in range(columnas):
            if ruta and (i, j) in ruta:
                print('*', end=' ')
            elif mapa[i][j] == CAMINO_LIBRE:
                print('.', end=' ')
            elif mapa[i][j] == AGUA:
                print('~', end=' ')
            elif mapa[i][j] == EDIFICIO:
                print('X', end=' ')
        print('#')
    print(' ' + '#' * (columnas *3 + 1))

def pedir_coordenadas(nombre, mapa):
    filas = len(mapa)
    columnas = len(mapa[0])
    while True:
        print(f'\nIngrese la coordenada de {nombre}')
        x = int(input('fila: '))
        y = int(input('columna: '))
        if x < 0 or x >= filas or y < 0 or y >= columnas:
            print('la coordenada es invalida, intente de nuevo')
            continue
        if mapa[x][y] == EDIFICIO:
            print('no se puede usar un edificio, intente de nuevo')
            continue
        return (x, y)
def dijkstra(mapa, inicio, destino):
    filas = len(mapa)
    columnas = len(mapa[0])
    if not (0 <= inicio[0] < filas and 0 <= inicio[1] < columnas):
        return None, float('inf')
    if not (0 <= destino[0] < filas and 0 <= destino[1] < columnas):
        return None, float('inf')
    dist = [[float('inf')] * columnas for _ in range (filas)]
    padre = [[None] * columnas for _ in range (filas)]
    visitados = set()

    pq = []
    heapq.heappush(pq, (0, inicio))
    dist[inicio[0]][inicio[1]] = 0

    while pq:
        costo, (x, y) = heapq.heappop(pq)
        if (x, y) in visitados:
            continue
        visitados.add((x, y))
        if (x, y) == destino:
            return reconstruir_camino(padre, inicio, destino), costo
        if costo > dist[x][y]:
            continue
        for dx, dy in MOVIMIENTOS:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < filas and 0 <= ny < columnas):
                continue
        if (nx, ny) in visitados:
            continue
        if mapa[nx][ny] == EDIFICIO:
            continue
        nuevo_costo = costo + COSTOS.get(mapa[nx][ny], 1)
        if nuevo_costo < dist[nx][ny]:
            dist[nx][ny] = nuevo_costo
            padre[nx][ny] = (x, y)
            heapq.heappush(pq, (nuevo_costo, (nx, ny)))
    return None, float('inf')
def reconstruir_camino(padre, inicio, destino):
    if padre[destino[0]][destino[1]] is None and destino != inicio:
        return None
    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        actual = padre[actual[0]][actual[1]]
    camino.reverse()
    return camino

def agregar_obstaculos_usuario(mapa):
    n = int(input('cuantos obstaculos quiere agregar al mapa?: '))
    for _ in range(n):
        x = int(input('Fila: '))
        y = int(input('Columna: '))
        tipo = input('Tipo: X (edificio) o ~ (agua):')
        if 0 <= x < len(mapa) and 0 <= y < len(mapa[0]):
            if tipo == "X":
                mapa[x][y] = EDIFICIO
            elif tipo == "~":
                mapa[x][y] = AGUA

def main():
    mapa = crear_mapa()
    mostrar_mapa(mapa)
    inicio = pedir_coordenadas('inicio', mapa)
    destino = pedir_coordenadas('destino', mapa)
    agregar_obstaculos(mapa, prob_edificio, prob_agua)

    while True:
        ruta = dijkstra(mapa, inicio, destino)
        mostrar_mapa(mapa, ruta)
        opcion = input('desea agregar mas obstaculos? (s/n):').lower()
        if opcion != "s":
            break
        agregar_obstaculos_usuario(mapa)
main()